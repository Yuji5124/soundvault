"""Render the orchestral test themes: one sfizz pass per part, then mix.

Usage: render_orch.py <vsco2_dir> <sfizz_render> <out_dir> [piece_id ...]
- Each part is rendered alone, one pass, as sample-exact note events (patched
  sfizz_render --events, float32). Everything that rings past the loop end
  (releases, tails, notes pulled early before the start) is folded back onto
  the loop, so the file is exactly one period of the music played forever:
  the seam is continuous by construction, even with round-robin samples.
- Parts are panned to orchestral seating, summed, and sent to a synthetic
  hall (3-band decay + early reflections) applied by circular convolution,
  so the reverb tail also wraps into the loop start.
- Loudness: -16 LUFS target, -1 dBTP ceiling, gain only (no limiter).
"""
import json
import resource
import subprocess
import sys
import time
from pathlib import Path

import mido
import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.signal import resample_poly

sys.path.insert(0, str(Path(__file__).parent))
from orchestrate import INSTR, arrange  # noqa: E402
from catalog import PIECES  # noqa: E402
from scipy.signal import fftconvolve  # noqa: E402

SR = 48000
TPB = 1200  # one tick = whole samples at 48 kHz for 80/96/100/120/150 BPM
TARGET_LUFS, CEILING_DBTP = -16.0, -1.0

# instrument seating: (pan -1..1, reverb send, seconds to pull notes earlier for slow attacks)
SEAT = {
    'vln1': (-0.55, 0.30, 0.06), 'vln1_q': (-0.55, 0.32, 0.06), 'vln2': (-0.25, 0.30, 0.06), 'vln_trem': (-0.4, 0.35, 0.03),
    'vln2_spic': (-0.25, 0.25, 0.0), 'vln2_pizz': (-0.25, 0.28, 0.0),
    'vla': (0.15, 0.30, 0.06), 'vla_spic': (0.15, 0.25, 0.0), 'vla_pizz': (0.15, 0.28, 0.0), 'vla_trem': (0.15, 0.35, 0.03),
    'vc': (0.45, 0.28, 0.06), 'vc_spic': (0.45, 0.22, 0.0), 'vc_pizz': (0.45, 0.26, 0.0),
    'cb': (0.6, 0.25, 0.06), 'cb_spic': (0.6, 0.2, 0.0), 'cb_pizz': (0.6, 0.24, 0.0),
    'fl': (-0.15, 0.40, 0.03), 'ob': (0.1, 0.40, 0.03), 'cl': (-0.1, 0.40, 0.03), 'bn': (0.2, 0.40, 0.03),
    'hn': (-0.35, 0.50, 0.04), 'hn_stac': (-0.35, 0.45, 0.0), 'tpt': (0.1, 0.42, 0.02), 'tpt_stac': (0.1, 0.42, 0.0),
    'tbn': (0.35, 0.45, 0.03), 'tbn_stac': (0.35, 0.42, 0.0), 'tba': (0.45, 0.40, 0.03),
    'harp': (-0.7, 0.38, 0.0), 'glock': (0.3, 0.45, 0.0),
    'svln': (-0.3, 0.38, 0.05), 'org': (0.0, 0.55, 0.0), 'bells': (0.35, 0.5, 0.0), 'xylo': (0.25, 0.35, 0.0), 'hn_mute': (-0.35, 0.5, 0.04),
    'timp': (-0.1, 0.40, 0.0), 'timp_roll': (-0.1, 0.40, 0.0), 'perc': (0.05, 0.40, 0.0),
}
# measured loudness of each instrument at the same note/velocity (calibrate.py); perc is set by ear-free default
CAL = json.loads((Path(__file__).parent / 'calibration.json').read_text())
CAL_REF = -32.0
# role level relative to a calibrated instrument (velocity already shapes dynamics)
ROLE_DB = {'mel': 3, 'ctr': -1, 'pad': -1, 'bass': 0, 'arp': -1, 'ost': 0, 'stab': -6, 'spk': -2, 'perc': 0}
PERC_DB = {'perc': 0, 'timp': 6, 'timp_roll': 0}


def part_mix(part):
    inst, role = part.split('#')
    pan, send, shift = SEAT[inst]
    gain = PERC_DB[inst] if inst in PERC_DB else CAL_REF - CAL[inst] + ROLE_DB[role]
    return pan, gain, send, shift


def tempo_us(bpm):
    us = 60_000_000 / bpm
    assert us.is_integer(), f'{bpm} BPM is not a whole number of microseconds per beat'
    return int(us)


PAD = SR  # 1 s lead-in so notes pulled earlier than the loop start still fit


def write_part_events(notes, bpm, shift_s, path, seed):
    """Sample-exact note events (frame on note vel) for one pass, offset by PAD."""
    rng = np.random.default_rng(seed)
    beat_frames = SR * 60 / bpm
    lines = []
    for start, beats, pitch, vel in notes:
        on = round(start * beat_frames + (rng.normal(0, 0.006) - shift_s) * SR)
        off = round((start + beats) * beat_frames - shift_s * SR)
        lines.append(f'{PAD + on} 1 {pitch} {vel}')
        lines.append(f'{PAD + max(off, on + 1)} 0 {pitch} 0')
    Path(path).write_text('\n'.join(lines) + '\n')


def write_score_midi(parts, bpm, path):
    """One editable multi-track MIDI of the loop (for DAW / notation use)."""
    mid = mido.MidiFile(type=1, ticks_per_beat=TPB)
    meta = mido.MidiTrack([mido.MetaMessage('set_tempo', tempo=tempo_us(bpm), time=0)])
    mid.tracks.append(meta)
    for ch, (part, notes) in enumerate(sorted(parts.items())):
        ev = []
        for start, beats, pitch, vel in notes:
            ev += [(round(start * TPB), 1, pitch, vel), (round((start + beats) * TPB), 0, pitch, 0)]
        ev.sort(key=lambda e: (e[0], e[1]))
        tr = mido.MidiTrack([mido.MetaMessage('track_name', name=part, time=0)])
        prev, c = 0, 9 if part in ('perc',) else ch % 15 + (1 if ch % 15 >= 9 else 0)
        for t, on, pitch, vel in ev:
            tr.append(mido.Message('note_on' if on else 'note_off', channel=c, note=pitch, velocity=vel, time=t - prev))
            prev = t
        mid.tracks.append(tr)
    mid.save(path)


def hall_ir(sr, seed=11):
    """Stereo hall: early reflections + diffuse tail with band-dependent decay."""
    rng = np.random.default_rng(seed)
    n = int(3.4 * sr)
    t = np.arange(n) / sr
    freqs = np.fft.rfftfreq(n, 1 / sr)
    ir = np.zeros((n, 2))
    for ch in range(2):
        tail = np.zeros(n)
        for lo, hi, rt in ((0, 300, 2.5), (300, 3000, 2.1), (3000, sr / 2, 1.2)):
            noise = np.fft.rfft(rng.standard_normal(n))
            noise[(freqs < lo) | (freqs >= hi)] = 0
            band = np.fft.irfft(noise, n)
            tail += band * np.exp(-6.91 * t / rt)
        tail *= np.clip((t - 0.022) / 0.05, 0, 1)  # diffuse onset after early reflections
        ir[:, ch] = tail / np.sqrt(np.sum(tail ** 2))
        for _ in range(10):  # early reflections 8-70 ms
            d = int(rng.uniform(0.008, 0.07) * sr)
            ir[d, ch] += rng.uniform(0.15, 0.4) * (1 if rng.random() > 0.5 else -1)
    return ir / np.sqrt(np.sum(ir ** 2, axis=0, keepdims=True))


def circular_convolve(x, ir):
    size = len(x)
    k = np.zeros((size, 2))
    k[: min(len(ir), size)] = ir[:size]
    if len(ir) > size:  # fold a long IR onto the loop
        for i in range(size, len(ir), size):
            seg = ir[i:i + size]
            k[: len(seg)] += seg
    return np.fft.irfft(np.fft.rfft(x, axis=0) * np.fft.rfft(k, axis=0), n=size, axis=0)


def highpass_circular(x, sr, fc=32):
    X = np.fft.rfft(x, axis=0)
    f = np.fft.rfftfreq(len(x), 1 / sr)
    X *= (1 / np.sqrt(1 + (fc / np.maximum(f, 1e-3)) ** 8))[:, None]
    return np.fft.irfft(X, n=len(x), axis=0)


def pan_gain(pan):
    a = (pan + 1) * np.pi / 4
    return np.array([np.cos(a), np.sin(a)]) * np.sqrt(2)


def render_piece(pid, vsco, sfizz, out):
    piece = PIECES[pid]
    arr = arrange(piece)
    bpm, loop_beats = piece['bpm'], arr.total_beats
    n = int(round(loop_beats * 60 / bpm * SR))
    looping = piece.get('loop', True)
    if looping:
        assert n % 64 == 0, f'{pid}: loop must be a multiple of 64 samples'
    else:  # jingle: play once, keep the ring-out
        n_once = n
        n = n + int(4.0 * SR)
    pre_roll = 0 if looping else int(0.08 * SR)
    work = out / f'{pid}_parts'
    work.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()
    dry = np.zeros((n, 2))
    wet_in = np.zeros((n, 2))
    stems = {}
    for i, (part, notes) in enumerate(sorted(arr.parts.items())):
        pan, gain_db, send, shift = part_mix(part)
        ev_path, wav_path = work / f"{part.replace('#', '__')}.txt", work / f"{part.replace('#', '__')}.wav"
        write_part_events(notes, bpm, shift, ev_path, seed=i + 1)
        subprocess.run([sfizz, '--sfz', str(vsco / INSTR[part.split('#')[0]][0]), '--events', str(ev_path), '--wav', str(wav_path),
                        '-s', str(SR), '-b', '64', '-p', '256'], capture_output=True, check=True)
        audio, sr = sf.read(str(wav_path), always_2d=True)
        assert sr == SR
        if audio.shape[1] == 1:
            audio = np.repeat(audio, 2, axis=1)
        assert not np.any(np.abs(audio[:PAD - int(0.2 * SR)]) > 1e-6), f'{part}: sound before the lead-in'
        folded = np.zeros((n, 2))
        if looping:
            body = audio[PAD:]
            for k in range(0, len(body), n):  # releases past the end wrap to the start
                chunk = body[k:k + n]
                folded[: len(chunk)] += chunk
            pre = audio[:PAD][-n:]  # notes pulled before beat 0 belong to the end of the previous period
            folded[n - len(pre):] += pre
        else:
            body = audio[PAD - pre_roll:PAD - pre_roll + n]
            folded[: len(body)] = body
        g = 10 ** (gain_db / 20) * pan_gain(pan)
        seg = folded * g
        dry += seg
        wet_in += seg * send
        stems[part] = seg
        wav_path.unlink()
    write_score_midi(arr.parts, bpm, out / f'{pid}.mid')
    if looping:
        wet = circular_convolve(wet_in, hall_ir(SR))
    else:
        wet = fftconvolve(wet_in, hall_ir(SR), axes=0)[:n]
    mix = highpass_circular(dry * 0.82 + wet * 0.9, SR)
    if not looping:
        mix *= np.clip((n - np.arange(n)) / (0.6 * SR), 0, 1)[:, None]  # gentle fade at the very end
    elapsed = time.perf_counter() - t0
    meter = pyln.Meter(SR)
    lufs_raw = meter.integrated_loudness(mix)
    gain = TARGET_LUFS - lufs_raw
    tp = 20 * np.log10(np.max(np.abs(resample_poly(mix, 4, 1, axis=0))) + 1e-12) + gain
    if tp > CEILING_DBTP:
        gain -= tp - CEILING_DBTP
    mix *= 10 ** (gain / 20)
    sf.write(str(out / f'{pid}.wav'), mix.astype(np.float32), SR, subtype='PCM_24')
    # seam sanity: sample step at the wrap vs the loop's own 99th-percentile step
    step99 = np.percentile(np.abs(np.diff(mix, axis=0)), 99)
    jump = float(np.max(np.abs(mix[0] - mix[-1])) / (step99 + 1e-12)) if looping else None
    # balance: loudness share of each part per section (dB relative to the dry sum)
    bar_frames = int(round(arr.bpb * 60 / bpm * SR))
    balance = {}
    for name, *_ in piece['sections']:
        bars = [b['bar'] for b in arr.bars if b['section'] == name]
        a0, a1 = pre_roll + bars[0] * bar_frames, pre_roll + (bars[-1] + 1) * bar_frames
        total = np.sqrt(np.mean(dry[a0:a1] ** 2)) + 1e-12
        lvl = {p: 20 * np.log10(np.sqrt(np.mean(x[a0:a1] ** 2)) / total + 1e-12) for p, x in stems.items()}
        balance[name] = {p: round(v, 1) for p, v in sorted(lvl.items(), key=lambda kv: -kv[1]) if v > -60}
    info = dict(id=pid, title=piece['title'], key=piece['key'], bpm=bpm, meter=arr.bpb, bars=len(arr.bars), loop=looping,
                group=piece.get('group', ''), usage=piece.get('usage', ''), motifs=piece.get('motifs', []), form=piece.get('form', ''),
                loop_seconds=n / SR, loop_end_samples=n if looping else None, sample_rate=SR, parts=sorted(arr.parts), notes=sum(len(v) for v in arr.parts.values()),
                render_seconds=round(elapsed, 1), child_peak_rss_mb=round(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024),
                lufs=round(meter.integrated_loudness(mix), 2), gain_db=round(gain, 2), seam_jump_ratio=None if jump is None else round(jump, 3),
                range_warnings=arr.warnings, balance=balance)
    print(json.dumps({k: v for k, v in info.items() if k not in ('parts',)}, ensure_ascii=False))
    return info


if __name__ == '__main__':
    vsco, sfizz, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    ids = sys.argv[4:] or list(PIECES)
    report = out / 'render.json'
    old = {r['id']: r for r in json.loads(report.read_text())} if report.exists() else {}
    for pid in ids:
        old[pid] = render_piece(pid, vsco, sfizz, out)
        report.write_text(json.dumps([old[k] for k in PIECES if k in old], ensure_ascii=False, indent=2))

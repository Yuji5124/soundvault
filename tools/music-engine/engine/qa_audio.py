"""Automatic QA for generated BGM.

Usage: qa_audio.py <out.json> --gen <wav...> --ref <wav...> [--gen-midi <mid...>] [--ref-midi <mid...>]
Checks: silence, clipping, peak / true peak, integrated loudness, loop seam,
audio similarity (key-invariant chroma), melody similarity (interval n-grams).
"""
import argparse
import itertools
import json
from pathlib import Path

import librosa
import numpy as np
import pretty_midi as pm
import pyloudnorm as pyln
import soundfile as sf
from scipy.signal import resample_poly

ap = argparse.ArgumentParser()
ap.add_argument('out')
ap.add_argument('--gen', nargs='+', required=True)
ap.add_argument('--ref', nargs='*', default=[])
ap.add_argument('--gen-midi', nargs='*', default=[])
ap.add_argument('--ref-midi', nargs='*', default=[])
args = ap.parse_args()


def db(x):
    return 20 * np.log10(np.maximum(x, 1e-12))


def basic(path):
    audio, sr = sf.read(path, always_2d=True)
    mono = audio.mean(axis=1)
    hop = int(sr * 0.05)
    frames = mono[: len(mono) // hop * hop].reshape(-1, hop)
    rms_db = db(np.sqrt((frames ** 2).mean(axis=1)))
    loud = np.where(rms_db > -60)[0]
    peak = np.max(np.abs(audio))
    true_peak = np.max(np.abs(resample_poly(audio, 4, 1, axis=0)))
    clipped = int((np.abs(audio) >= 0.999).sum())
    meter = pyln.Meter(sr)
    lufs = meter.integrated_loudness(audio)
    # short-term loudness (3 s windows, 1 s hop) spread ~ dynamics
    st = [meter.integrated_loudness(audio[i:i + 3 * sr]) for i in range(0, max(1, len(audio) - 3 * sr), sr)]
    st = np.array([v for v in st if np.isfinite(v)])
    # loop seam: compare the wrap boundary with ordinary internal boundaries
    win = int(sr * 0.1)
    mel = lambda seg: np.log1p(librosa.feature.melspectrogram(y=seg, sr=sr, n_fft=2048, hop_length=512, n_mels=64).mean(axis=1))
    starts = np.arange(0, len(mono) - 2 * win, win)
    internal = np.array([np.linalg.norm(mel(mono[s:s + win]) - mel(mono[s + win:s + 2 * win])) for s in starts[:: max(1, len(starts) // 200)]])
    seam = np.linalg.norm(mel(mono[-win:]) - mel(mono[:win]))
    jump = abs(mono[0] - mono[-1])
    step99 = np.percentile(np.abs(np.diff(mono)), 99)
    return dict(
        file=Path(path).name, seconds=round(len(mono) / sr, 2), sample_rate=sr, channels=audio.shape[1],
        silent_frame_pct=round(100 * float((rms_db < -50).mean()), 1),
        lead_silence_ms=int(loud[0] * 50) if len(loud) else None,
        tail_silence_ms=int((len(rms_db) - 1 - loud[-1]) * 50) if len(loud) else None,
        peak_dbfs=round(float(db(peak)), 2), true_peak_dbtp=round(float(db(true_peak)), 2),
        clipped_samples=clipped, lufs=round(float(lufs), 2),
        short_term_range_lu=round(float(np.percentile(st, 95) - np.percentile(st, 10)), 1) if len(st) > 2 else None,
        seam_ratio=round(float(seam / (np.median(internal) + 1e-9)), 2),
        seam_percentile=round(float((internal < seam).mean() * 100), 1),
        seam_sample_jump_ratio=round(float(jump / (step99 + 1e-9)), 2),
    )


def chroma(path):
    y, sr = librosa.load(path, sr=22050, mono=True)
    return librosa.feature.chroma_cens(y=y, sr=sr, hop_length=2048)  # ~0.09 s/frame


def chroma_similarity(a, b, seg=44):
    """Best cosine match of any ~4 s chroma segment of a inside b, over 12 key shifts."""
    best = 0.0
    segs = [a[:, i:i + seg] for i in range(0, a.shape[1] - seg, seg // 2)]
    for shift in range(12):
        bs = np.roll(b, shift, axis=0)
        windows = np.lib.stride_tricks.sliding_window_view(bs, seg, axis=1)  # 12 x n x seg
        wn = windows / (np.linalg.norm(windows, axis=(0, 2), keepdims=True) + 1e-9)
        for s in segs:
            sn = s / (np.linalg.norm(s) + 1e-9)
            score = np.einsum('kns,ks->n', wn, sn).max()
            best = max(best, float(score))
    return round(best, 3)


def melody_intervals(path):
    midi = pm.PrettyMIDI(path)
    cands = [i for i in midi.instruments if not i.is_drum and i.notes]
    lead = next((i for i in cands if i.name == 'lead'), None) or max(cands, key=lambda i: np.mean([n.pitch for n in i.notes]))
    notes = sorted(lead.notes, key=lambda n: (n.start, -n.pitch))
    top = []
    for n in notes:  # keep highest note per onset
        if top and abs(top[-1].start - n.start) < 1e-3:
            continue
        top.append(n)
    return [b.pitch - a.pitch for a, b in zip(top, top[1:])]


def ngram_overlap(a, b, n=6):
    ga = {tuple(a[i:i + n]) for i in range(len(a) - n + 1)}
    gb = {tuple(b[i:i + n]) for i in range(len(b) - n + 1)}
    return round(len(ga & gb) / max(1, len(ga)), 3)


report = dict(basic=[basic(p) for p in args.gen], reference_basic=[basic(p) for p in args.ref])
chg = {Path(p).name: chroma(p) for p in args.gen}
chr_ = {Path(p).name: chroma(p) for p in args.ref}
sim_gen = {f'{a}|{b}': chroma_similarity(chg[a], chg[b]) for a, b in itertools.combinations(chg, 2)}
sim_ref = {}
for a in chg:
    scores = {r: chroma_similarity(chg[a], chr_[r]) for r in chr_}
    if scores:
        top = max(scores, key=scores.get)
        sim_ref[a] = dict(max=scores[top], closest=top)
report['chroma_similarity_between_generated'] = sim_gen
report['chroma_baseline_unrelated_references'] = {f'{a}|{b}': chroma_similarity(chr_[a], chr_[b]) for a, b in list(itertools.combinations(chr_, 2))[:12]}
report['chroma_similarity_vs_reference'] = sim_ref
if args.gen_midi:
    mg = {Path(p).name: melody_intervals(p) for p in args.gen_midi}
    mr = {Path(p).name: melody_intervals(p) for p in args.ref_midi}
    report['melody_6gram_overlap_vs_reference'] = {
        a: max(((ngram_overlap(mg[a], mr[r]), r) for r in mr), default=(0, None)) for a in mg}
    report['melody_6gram_overlap_between_generated'] = {
        f'{a}|{b}': ngram_overlap(mg[a], mg[b]) for a, b in itertools.combinations(mg, 2)}
Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2))
print(json.dumps(report, ensure_ascii=False, indent=1))

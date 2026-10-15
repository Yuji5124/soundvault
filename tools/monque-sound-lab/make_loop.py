"""Turn a generated (non-looping) clip into a bar-aligned game loop.

Usage: make_loop.py <in.wav> <out.wav> --bpm 100 [--bars 8] [--xfade-ms 60]
Searches loop starts on the beat grid and picks the one whose lead-in best
matches the audio just before the loop end, then crossfades that lead-in
into the loop tail so playback wraps without a click. Prints loop metadata.
"""
import argparse
import json

import librosa
import numpy as np
import soundfile as sf

ap = argparse.ArgumentParser()
ap.add_argument('src')
ap.add_argument('dst')
ap.add_argument('--bpm', type=float, required=True)
ap.add_argument('--bars', type=int, default=0, help='0 = longest whole power-of-two bar count that fits')
ap.add_argument('--xfade-ms', type=float, default=60)
a = ap.parse_args()

audio, sr = sf.read(a.src, always_2d=True)
mono = audio.mean(axis=1)
beat = 60 / a.bpm
_, beats = librosa.beat.beat_track(y=mono, sr=sr, bpm=a.bpm, units='samples', tightness=400)
if len(beats) < 8:
    beats = np.arange(0, len(mono), int(beat * sr))
bar_len = int(round(4 * beat * sr))
usable = len(mono) - int(1.0 * sr) - beats[0]
bars = a.bars or 2 ** int(np.log2(max(1, usable // bar_len)))
loop_len = bars * bar_len
xf = int(a.xfade_ms / 1000 * sr)
ctx = int(0.5 * sr)


def feat(seg):
    return np.log1p(np.abs(librosa.stft(seg, n_fft=2048, hop_length=512))).mean(axis=1)


best = None
for s in beats:
    e = s + loop_len
    if s < ctx or e > len(mono):
        continue
    d = np.linalg.norm(feat(mono[s - ctx:s]) - feat(mono[e - ctx:e]))
    if best is None or d < best[0]:
        best = (d, s)
if best is None:
    raise SystemExit(f'clip too short for {bars} bars at {a.bpm} BPM')
s = int(best[1])
e = s + loop_len
loop = audio[s:e].copy()
fade = np.sqrt(np.linspace(0, 1, xf))[:, None]
loop[-xf:] = loop[-xf:] * fade[::-1] + audio[s - xf:s] * fade  # tail flows into what precedes the loop start
sf.write(a.dst, loop.astype(np.float32), sr, subtype='PCM_16')
info = dict(src=a.src, dst=a.dst, bpm=a.bpm, bars=bars, loop_start_in_src_s=round(s / sr, 3),
            loop_seconds=round(loop_len / sr, 3), match_distance=round(float(best[0]), 3), xfade_ms=a.xfade_ms)
print(json.dumps(info, ensure_ascii=False))

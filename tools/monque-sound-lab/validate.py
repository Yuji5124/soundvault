"""Static checks for every piece before rendering: bar lengths, harmony on strong beats, ranges, loop arithmetic."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from catalog import PIECES  # noqa: E402
from orchestrate import NOTE, arrange, parse_chord  # noqa: E402

SR = 48000
bad = 0
for pid, p in PIECES.items():
    bpb = p.get('meter', 4)
    strong = ok = 0
    errs = []
    for sec in p['sections']:
        name, chords, mel = sec[:3]
        for i, (sym, bar) in enumerate(zip(chords.split(), mel)):
            halves = [parse_chord(h) for h in sym.split('|')]
            t = 0.0
            for tok in bar.split():
                n, d = tok.split(':')
                d = float(d)
                if n != 'r' and abs(t - round(t)) < 1e-9 and (t == 0 or (bpb == 4 and t == 2)):
                    ch = halves[min(int(t // (bpb / len(halves))), len(halves) - 1)]
                    strong += 1
                    ok += NOTE(n) % 12 in ch['pcs']
                t += d
            if abs(t - bpb) > 1e-6:
                errs.append(f'{name} bar {i + 1}: {t} beats')
        for k, lines in (sec[3] if len(sec) > 3 else {}).items():
            for i, bar in enumerate(lines):
                t = sum(float(tok.split(':')[1]) for tok in bar.split())
                if abs(t - bpb) > 1e-6:
                    errs.append(f'{name} {k} bar {i + 1}: {t} beats')
    a = arrange(p)
    us = 60_000_000 / p['bpm']
    n = a.total_beats * 60 / p['bpm'] * SR
    if not us.is_integer():
        errs.append(f'tempo {p["bpm"]} is not whole microseconds')
    if p.get('loop', True) and (abs(n - round(n)) > 1e-6 or round(n) % 64):
        errs.append(f'loop {n} samples is not a multiple of 64')
    pct = 100 * ok / max(1, strong)
    flag = 'OK ' if not errs and not a.warnings and pct >= 85 else 'CHK'
    bad += flag != 'OK '
    print(f'{flag} {pid:22s} {p["bpm"]:>3} BPM {bpb}/4 {len(a.bars):>2} bars {a.total_beats * 60 / p["bpm"]:5.1f}s  strong-beat chord tones {pct:5.1f}%  parts {len(a.parts):>2}  notes {sum(len(v) for v in a.parts.values()):>5}',
          *(errs[:4] + a.warnings[:4]), sep='\n    ')
print('pieces needing attention:', bad)

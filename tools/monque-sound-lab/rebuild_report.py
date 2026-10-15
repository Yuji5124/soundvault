"""Rebuild render.json from the catalog and the rendered WAVs (no re-render)."""
import json, sys
from pathlib import Path
import numpy as np, soundfile as sf
sys.path.insert(0, str(Path(__file__).parent))
from catalog import PIECES
from orchestrate import arrange
out = Path(sys.argv[1]); SR = 48000; rows = []
for pid, p in PIECES.items():
    a = arrange(p); loop = p.get('loop', True)
    n = int(round(a.total_beats * 60 / p['bpm'] * SR))
    mix, sr = sf.read(str(out / f'{pid}.wav'), always_2d=True)
    jump = None
    if loop:
        assert len(mix) == n, (pid, len(mix), n)
        step99 = np.percentile(np.abs(np.diff(mix, axis=0)), 99)
        jump = round(float(np.max(np.abs(mix[0] - mix[-1])) / (step99 + 1e-12)), 3)
    rows.append(dict(id=pid, title=p['title'], key=p['key'], bpm=p['bpm'], meter=a.bpb, bars=len(a.bars), loop=loop,
                     group=p.get('group', ''), usage=p.get('usage', ''), motifs=p.get('motifs', []), form=p.get('form', ''),
                     loop_seconds=len(mix) / SR, loop_end_samples=n if loop else None, sample_rate=SR, parts=sorted(a.parts),
                     notes=sum(len(v) for v in a.parts.values()), seam_jump_ratio=jump, range_warnings=a.warnings))
(out / 'render.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2))
print(len(rows), 'rows')

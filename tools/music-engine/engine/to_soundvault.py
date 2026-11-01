"""Export rendered pieces into SOUNDVAULT: OGG + M4A files, metadata, and the project record.

Usage: to_soundvault.py <render_dir> <soundvault_repo> [piece_id ...]  (default: every rendered piece)
Writes public/sounds/bgm/<file_prefix><name>.{ogg,m4a}, adds/updates their records in data/sounds.json
(the scanner keeps these fields) and the project in data/projects.json, using the selected
project's project.json (MSL_PROJECT). Run `npm run scan` afterwards.
"""
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

src, repo = Path(sys.argv[1]), Path(sys.argv[2])
render = {r['id']: r for r in json.loads((src / 'render.json').read_text())}
if sys.argv[3:]:
    render = {k: v for k, v in render.items() if k in sys.argv[3:]}
bgm = repo / 'public/sounds/bgm'
bgm.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(Path(__file__).parent))
from project import settings  # noqa: E402

CFG = settings()  # projects/<name>/project.json of the selected MSL_PROJECT
PROJECT = {'id': CFG['id'], 'name': CFG['name'], 'type': CFG.get('type', 'ゲーム'), 'archived': False}
FILE_PREFIX, ID_STRIP = CFG['file_prefix'], CFG['id_strip']
NAME_PREFIX, TAG, COLLECTION = CFG['name_prefix'], CFG['tag'], CFG['collection']
SOURCE = 'SOUNDVAULT music engine: original score rendered with VSCO 2 Community Edition (CC0) via sfizz; Claude Code'

sounds_path = repo / 'data/sounds.json'
sounds = json.loads(sounds_path.read_text())
by_file = {s['file']: s for s in sounds}
now = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')

for pid, r in render.items():
    stem = FILE_PREFIX + pid.removeprefix(ID_STRIP).replace('_', '-')
    wav = src / f'{pid}.wav'
    for ext, codec in (('ogg', ['-c:a', 'libvorbis', '-q:a', '6']), ('m4a', ['-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart'])):
        out = bgm / f'{stem}.{ext}'
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(wav), *codec, str(out)], check=True)
        file = f'/sounds/bgm/{stem}.{ext}'
        loop_note = (f"ループ: 0〜{r['loop_end_samples']} サンプル（48kHz、{r['loop_seconds']:.3f}秒）。" if r['loop'] else '1回再生のジングル。')
        record = {
            'id': f"{stem.replace('-', '_')}_{ext}",
            'name': f"{NAME_PREFIX}{r['title']}",
            'file': file,
            'category': 'BGM',
            'tags': ['bgm', TAG, 'orchestral', r['group'], r['key']] + r['motifs'],
            'duration': round(r['loop_seconds'], 3),
            'loop': bool(r['loop']),
            'loopStart': 0 if r['loop'] else None,
            'loopEnd': r['loop_end_samples'],
            'sampleRate': 48000,
            # quieter masters (dynamic pieces held back by the -1 dBTP ceiling) get a higher playback volume
            'volume': min(1.0, round(0.8 * 10 ** ((-16 - r.get('lufs', -16)) / 20), 2)),
            'license': 'Original',
            'source': SOURCE,
            'author': 'Claude Code (MONQUE SOUND LAB) for Yuji5124',
            'favorite': False,
            'notes': f"{r['usage']}。{r['key']}・{r['bpm']} BPM・{r['meter']}/4・{r['bars']}小節。{r['form']}。{loop_note}"
                     f"{'M4A(AAC)はエンコーダの遅延で継ぎ目に隙間が出る場合あり。ループにはOGG推奨、iPhone Safariは実機確認が必要。' if ext == 'm4a' else ''}",
            'collections': [COLLECTION],
            'projectIds': [PROJECT['id']],
        }
        old = by_file.get(file, {})
        merged = {**old, **record, 'createdAt': old.get('createdAt', now)}
        by_file[file] = merged
sounds = sorted(by_file.values(), key=lambda s: s['name'])
sounds_path.write_text(json.dumps(sounds, ensure_ascii=False, indent=2) + '\n')

projects_path = repo / 'data/projects.json'
projects = json.loads(projects_path.read_text())
projects = [p for p in projects if p['id'] != PROJECT['id']] + [PROJECT]
projects_path.write_text(json.dumps(projects, ensure_ascii=False, indent=2) + '\n')
print(f"{len(render)} pieces -> {len(render) * 2} files in {bgm}")

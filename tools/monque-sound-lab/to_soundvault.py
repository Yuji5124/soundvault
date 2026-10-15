"""Export rendered pieces into SOUNDVAULT: OGG + M4A files, metadata, and the Monster Quest 0 project.

Usage: to_soundvault.py <render_dir> <soundvault_repo>
Writes public/sounds/bgm/monque-<name>.{ogg,m4a}, adds/updates their records in data/sounds.json
(the scanner keeps these fields) and the project in data/projects.json. Run `npm run scan` afterwards.
"""
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

src, repo = Path(sys.argv[1]), Path(sys.argv[2])
render = {r['id']: r for r in json.loads((src / 'render.json').read_text())}
bgm = repo / 'public/sounds/bgm'
bgm.mkdir(parents=True, exist_ok=True)
PROJECT = {'id': 'monque', 'name': 'モンスタークエスト0', 'type': 'ゲーム', 'archived': False}
SOURCE = 'MONQUE SOUND LAB: original score (MIDI) rendered with VSCO 2 Community Edition (CC0) via sfizz; Claude Code, 2026-10-15'

sounds_path = repo / 'data/sounds.json'
sounds = json.loads(sounds_path.read_text())
by_file = {s['file']: s for s in sounds}
now = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')

for pid, r in render.items():
    stem = 'monque-' + pid.removeprefix('mq_orch_').replace('_', '-')
    wav = src / f'{pid}.wav'
    for ext, codec in (('ogg', ['-c:a', 'libvorbis', '-q:a', '6']), ('m4a', ['-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart'])):
        out = bgm / f'{stem}.{ext}'
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(wav), *codec, str(out)], check=True)
        file = f'/sounds/bgm/{stem}.{ext}'
        loop_note = (f"ループ: 0〜{r['loop_end_samples']} サンプル（48kHz、{r['loop_seconds']:.3f}秒）。" if r['loop'] else '1回再生のジングル。')
        record = {
            'id': f"{stem.replace('-', '_')}_{ext}",
            'name': f"モンクエ {r['title']}",
            'file': file,
            'category': 'BGM',
            'tags': ['bgm', 'monque', 'orchestral', r['group'], r['key']] + r['motifs'],
            'duration': round(r['loop_seconds'], 3),
            'loop': bool(r['loop']),
            'loopStart': 0 if r['loop'] else None,
            'loopEnd': r['loop_end_samples'],
            'sampleRate': 48000,
            'volume': 0.8,
            'license': 'Original',
            'source': SOURCE,
            'author': 'Claude Code (MONQUE SOUND LAB) for Yuji5124',
            'favorite': False,
            'notes': f"{r['usage']}。{r['key']}・{r['bpm']} BPM・{r['meter']}/4・{r['bars']}小節。{r['form']}。{loop_note}"
                     f"{'M4A(AAC)はエンコーダの遅延で継ぎ目に隙間が出る場合あり。ループにはOGG推奨、iPhone Safariは実機確認が必要。' if ext == 'm4a' else ''}",
            'collections': ['MONQUE BGM 30'],
            'projectIds': ['monque'],
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

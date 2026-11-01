"""Assemble the MONQUE BGM 30 listening page: data JSON + OGG/M4A copies.

Usage: build_page30.py <render_dir> <qa.json> <page_dir> <soundvault_items_json>
"""
import json
import subprocess
import sys
from pathlib import Path

src, qa_path, page = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sv_items = json.loads(Path(sys.argv[4]).read_text())
render = json.loads((src / 'render.json').read_text())
qa = json.loads(qa_path.read_text())
qb = {b['file'][:-4]: b for b in qa['basic']}
mel = {k[:-4]: v for k, v in qa['melody_6gram_overlap_vs_reference'].items()}
audio = page / 'audio'
audio.mkdir(parents=True, exist_ok=True)
tracks = []
for r in render:
    b = qb[r['id']]
    loop = r['loop']
    passed = (b['clipped_samples'] == 0 and (b['silent_frame_pct'] < 5 or not loop) and b['true_peak_dbtp'] <= -0.9
              and abs(b['lufs'] - (-16)) <= 1.0 and (not loop or b['seam_sample_jump_ratio'] < 1) and mel[r['id']][0] < 0.1)
    tracks.append(dict(
        id=r['id'], title=r['title'], usage=r['usage'], group=r['group'], key=r['key'], bpm=r['bpm'], meter=r['meter'],
        bars=r['bars'], seconds=r['loop_seconds'] if loop else b['seconds'], loop=loop, motifs=r['motifs'], form=r['form'],
        parts=len(r['parts']), notes=r['notes'], lufs=b['lufs'], tp=b['true_peak_dbtp'], clip=b['clipped_samples'],
        silent=b['silent_frame_pct'], dyn=b['short_term_range_lu'], jump=b['seam_sample_jump_ratio'] if loop else None,
        mel=mel[r['id']][0], pass_=passed))
    for ext, codec in (('ogg', ['-c:a', 'libvorbis', '-q:a', '5']), ('m4a', ['-c:a', 'aac', '-b:a', '160k'])):
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(src / f"{r['id']}.wav"), *codec, str(audio / f"{r['id']}.{ext}")], check=True)
for t in tracks:
    t['pass'] = t.pop('pass_')
note = ('合格条件：クリップ0、無音5%未満、トゥルーピーク −0.9 dBTP以下、ラウドネス −16±1 LUFS、継ぎ目の段差が1未満（ループ曲）、'
        '既存モンクエMIDI 13曲との旋律の一致（音程6つの並び）10%未満。ジングルは末尾の余韻が消える部分を無音から除外。音量の起伏は3秒ごとのラウドネスの幅。'
        '旋律の一致率は既存モンクエ曲との比較で、有名曲との照合はしていません。')
(page / 'data30.json').write_text(json.dumps(dict(tracks=tracks, qaNote=note, soundvault=sv_items), ensure_ascii=False))
print(sum(t['pass'] for t in tracks), 'of', len(tracks), 'pass')

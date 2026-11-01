#!/usr/bin/env python3
"""SOUNDVAULT music engine command line.

  python msl.py list                         projects and their pieces
  python msl.py validate <project>           bar lengths, harmony, ranges, loop arithmetic
  python msl.py render <project> [id ...]    render WAVs to .out/<project>/
  python msl.py qa <project>                 loudness, peaks, seams, silence, melody similarity
  python msl.py export <project> <soundvault_repo> [id ...]
                                             OGG + M4A + records into SOUNDVAULT (then: npm run scan)
  python msl.py selftest                     render a reference piece and compare with the stored result

Run setup.sh once first. Paths can be overridden with MSL_VSCO (VSCO 2 CE, SFZ branch) and
MSL_SFIZZ (patched sfizz_render). <project> is a directory name under projects/.
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENGINE = ROOT / 'engine'
VSCO = Path(os.environ.get('MSL_VSCO', ROOT / '.cache' / 'VSCO-2-CE'))
SFIZZ = Path(os.environ.get('MSL_SFIZZ', ROOT / '.cache' / 'sfizz' / 'build' / 'library' / 'bin' / 'sfizz_render'))
PY = sys.executable


def project_env(name):
    pdir = ROOT / 'projects' / name
    if not (pdir / 'catalog.py').exists():
        sys.exit(f'unknown project "{name}" (expected {pdir}/catalog.py)')
    return {**os.environ, 'MSL_PROJECT': str(pdir)}, pdir


def out_dir(name):
    path = ROOT / '.out' / name
    path.mkdir(parents=True, exist_ok=True)
    return path


def run(args, env):
    return subprocess.run([PY, '-I', *map(str, args)], env=env, check=True)


def need_tools():
    missing = [str(p) for p in (VSCO / 'Harp.sfz', SFIZZ) if not p.exists()]
    if missing:
        sys.exit('missing: ' + ', '.join(missing) + '\nrun ./setup.sh (or set MSL_VSCO / MSL_SFIZZ)')


def load(name):
    env, _ = project_env(name)
    os.environ['MSL_PROJECT'] = env['MSL_PROJECT']
    sys.path.insert(0, str(ENGINE))
    from project import load_catalog
    return load_catalog()


def cmd_list(_):
    for pdir in sorted((ROOT / 'projects').iterdir()):
        if (pdir / 'catalog.py').exists():
            out = subprocess.run([PY, '-I', '-c', 'import sys; sys.path.insert(0, sys.argv[1]); from project import load_catalog; '
                                  '[print(f"  {k:24s} {v[\'title\']}") for k, v in load_catalog().items()]', str(ENGINE)],
                                 env={**os.environ, 'MSL_PROJECT': str(pdir)}, capture_output=True, text=True, check=True)
            print(pdir.name)
            print(out.stdout, end='')


def cmd_validate(args):
    env, _ = project_env(args[0])
    run([ENGINE / 'validate.py'], env)


def cmd_render(args):
    need_tools()
    env, _ = project_env(args[0])
    run([ENGINE / 'render_orch.py', VSCO, SFIZZ, out_dir(args[0]), *args[1:]], env)


def cmd_qa(args):
    name = args[0]
    pieces = load(name)
    out = out_dir(name)
    from melody import write_melodies
    mids = write_melodies(pieces, out / 'melody')
    wavs = [out / f'{pid}.wav' for pid in pieces if (out / f'{pid}.wav').exists()]
    if not wavs:
        sys.exit(f'no rendered WAVs in {out}; run: python msl.py render {name}')
    env, _ = project_env(name)
    run([ENGINE / 'qa_audio.py', out / 'qa.json', '--gen', *wavs, '--gen-midi', *mids], env)


def cmd_export(args):
    name, repo, ids = args[0], Path(args[1]).resolve(), args[2:]
    env, _ = project_env(name)
    run([ENGINE / 'to_soundvault.py', out_dir(name), repo, *ids], env)
    print('next: cd', repo, '&& npm run scan && npm run build')


def cmd_selftest(_):
    """Render the 14 s victory jingle and compare with engine/selftest.json."""
    need_tools()
    ref = json.loads((ENGINE / 'selftest.json').read_text())
    env, _ = project_env(ref['project'])
    out = ROOT / '.out' / 'selftest'
    out.mkdir(parents=True, exist_ok=True)
    run([ENGINE / 'render_orch.py', VSCO, SFIZZ, out, ref['piece']], env)
    import numpy as np
    import soundfile as sf
    wav = out / f"{ref['piece']}.wav"
    audio, sr = sf.read(str(wav), always_2d=True)
    stats = fingerprint(audio, sr)
    digest = hashlib.sha256(wav.read_bytes()).hexdigest()
    env_diff = float(np.max(np.abs(np.array(stats['envelope_db']) - np.array(ref['stats']['envelope_db']))))
    ok = (stats['frames'] == ref['stats']['frames'] and abs(stats['lufs'] - ref['stats']['lufs']) < 0.3
          and abs(stats['peak_db'] - ref['stats']['peak_db']) < 0.5 and env_diff < 1.0)
    print(json.dumps(dict(identical=digest == ref['sha256'], frames=stats['frames'], lufs=stats['lufs'],
                          peak_db=stats['peak_db'], max_envelope_diff_db=round(env_diff, 3)), ensure_ascii=False))
    print('SELFTEST', 'PASS' if ok else 'FAIL', '(bit-identical)' if digest == ref['sha256'] else '(within tolerance)' if ok else '')
    sys.exit(0 if ok else 1)


def fingerprint(audio, sr):
    import numpy as np
    import pyloudnorm as pyln
    mono = audio.mean(axis=1)
    hop = sr // 2
    env = [round(float(20 * np.log10(np.sqrt(np.mean(mono[i:i + hop] ** 2)) + 1e-9)), 2) for i in range(0, len(mono) - hop + 1, hop)]
    return dict(frames=len(audio), lufs=round(float(pyln.Meter(sr).integrated_loudness(audio)), 2),
                peak_db=round(float(20 * np.log10(np.max(np.abs(audio)) + 1e-12)), 2), envelope_db=env)


COMMANDS = {'list': cmd_list, 'validate': cmd_validate, 'render': cmd_render, 'qa': cmd_qa,
            'export': cmd_export, 'selftest': cmd_selftest}

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        sys.exit(__doc__)
    if sys.argv[1] in ('validate', 'render', 'qa', 'export') and len(sys.argv) < 3:
        sys.exit(__doc__)
    COMMANDS[sys.argv[1]](sys.argv[2:])

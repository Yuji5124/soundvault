# MONQUE SOUND LAB

Tools that produced `public/sounds/bgm/monque-*` (MONQUE BGM 30, orchestral BGM for Monster Quest 0).

- Scores: `score.py` (first 5 themes) and `pieces_*.py` (25 more); `catalog.py` lists all 30.
- `orchestrate.py` turns melody + chords into orchestral parts; `render_orch.py` renders each part with
  [sfizz](https://github.com/sfztools/sfizz) (apply `sfizz_render_events.patch` for sample-exact, deterministic,
  float32 renders) and [VSCO 2 Community Edition](https://github.com/sgossner/VSCO-2-CE) (CC0, `SFZ` branch),
  then mixes, adds hall reverb and folds the ring-out back so every loop is seamless.
- Checks: `validate.py` (bar lengths, harmony, ranges, loop arithmetic), `qa_audio.py` (clipping, loudness,
  true peak, seam, melody similarity).
- `to_soundvault.py` writes the OGG/M4A files and their records into `data/sounds.json` and `data/projects.json`.
- `windows/` holds the scripts for trying ACE-Step 1.5 / Stable Audio 3 on a local GPU PC (not run here).

```bash
python validate.py
python render_orch.py <vsco2_dir> <sfizz_render> <out_dir> [piece_id ...]
python qa_audio.py out/qa.json --gen out/*.wav
python to_soundvault.py <out_dir> <soundvault_repo> && npm run scan
```

Loops: 48 kHz, `loopStart` 0, `loopEnd` in samples. Use the OGG files for gapless loops; AAC (M4A) can add a
small gap at the loop point. All melodies are original; the sample library is CC0.

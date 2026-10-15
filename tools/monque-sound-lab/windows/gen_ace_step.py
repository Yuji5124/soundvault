"""Generate the MONQUE SOUND LAB test themes with ACE-Step 1.5 (local only).

Run from inside the ACE-Step-1.5 checkout, in its own uv environment:
  text only (method D):
    uv run python ..\\kit\\gen_ace_step.py ..\\kit\\themes.json ..\\out\\ace_text
  cover of our orchestral mock-ups (method E), keeps their melody and form:
    uv run python ..\\kit\\gen_ace_step.py ..\\kit\\themes.json ..\\out\\ace_cover ..\\orch_wav
  (orch_wav holds mq_orch_<theme>.wav from the listening page)
Writes FLAC files and metrics.json (time, peak VRAM, RAM).
Untested here: written against docs/en/INFERENCE.md of ace-step/ACE-Step-1.5.
"""
import json
import os
import sys
import time
from pathlib import Path

import psutil
import torch
from acestep.handler import AceStepHandler
from acestep.inference import GenerationConfig, GenerationParams, generate_music
from acestep.llm_inference import LLMHandler

themes = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
out = Path(sys.argv[2])
cover_dir = Path(sys.argv[3]) if len(sys.argv) > 3 else None
out.mkdir(parents=True, exist_ok=True)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
vram_gb = torch.cuda.get_device_properties(0).total_memory / 1e9 if device == 'cuda' else 0
use_lm = vram_gb >= 6 and cover_dir is None  # README: <=6GB -> DiT only; LM thinking is ignored for cover

proc = psutil.Process()
t_load = time.perf_counter()
dit = AceStepHandler()
dit.initialize_service(project_root=os.getcwd(), config_path='acestep-v15-turbo', device=device)
llm = None
if use_lm:
    llm = LLMHandler()
    llm.initialize(checkpoint_dir=os.path.join(os.getcwd(), 'checkpoints'), lm_model_path='acestep-5Hz-lm-0.6B',
                   backend='pt', device=device)
metrics = dict(model='acestep-v15-turbo', mode='cover' if cover_dir else 'text2music', device=device,
               gpu=torch.cuda.get_device_name(0) if device == 'cuda' else None,
               load_seconds=round(time.perf_counter() - t_load, 1), runs=[])

jobs = []
for theme in themes['themes']:
    for seed in themes['seeds']:
        if cover_dir:
            for strength in themes['cover_strengths']:
                jobs.append((theme, seed, strength))
        else:
            jobs.append((theme, seed, None))

for theme, seed, strength in jobs:
    if device == 'cuda':
        torch.cuda.reset_peak_memory_stats()
    common = dict(caption=theme['prompt'], lyrics='[Instrumental]', instrumental=True, seed=seed)
    if strength is None:
        params = GenerationParams(**common, bpm=theme['bpm'], keyscale=theme['key'], duration=themes['duration'], thinking=use_lm)
        tag = f"{theme['id']}_s{seed}"
    else:
        src = cover_dir / f"{theme['id']}.wav"
        params = GenerationParams(**common, task_type='cover', src_audio=str(src), audio_cover_strength=strength)
        tag = f"{theme['id']}_cover{int(strength * 100)}_s{seed}"
    config = GenerationConfig(batch_size=1, audio_format='flac', use_random_seed=False, seeds=[seed])
    t = time.perf_counter()
    result = generate_music(dit, llm, params, config, save_dir=str(out / tag))
    run = dict(tag=tag, id=theme['id'], seed=seed, cover_strength=strength, success=bool(result.success),
               seconds=round(time.perf_counter() - t, 1),
               peak_vram_gb=round(torch.cuda.max_memory_allocated() / 1e9, 2) if device == 'cuda' else None,
               rss_gb=round(proc.memory_info().rss / 1e9, 2),
               files=[a['path'] for a in result.audios] if result.success else [],
               error=None if result.success else str(getattr(result, 'error', '')))
    metrics['runs'].append(run)
    print(run, flush=True)
    (out / 'metrics.json').write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding='utf-8')

"""Generate the MONQUE SOUND LAB test themes with Stable Audio 3 (local only).

Run from inside the stable-audio-3 checkout, in its own uv environment:
    uv run python ..\\kit\\gen_stable_audio_3.py ..\\kit\\themes.json ..\\out\\stable_audio_3 [small-music|medium]
small-music runs on CPU; medium needs an NVIDIA GPU with Flash Attention 2.
Untested here: written against README.md and docs/workflows/inference.md of Stability-AI/stable-audio-3.
"""
import json
import sys
import time
from pathlib import Path

import psutil
import soundfile as sf
import torch
from stable_audio_3 import StableAudioModel

themes = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
model_id = sys.argv[3] if len(sys.argv) > 3 else 'small-music'
device = 'cuda' if torch.cuda.is_available() else 'cpu'

proc = psutil.Process()
t_load = time.perf_counter()
model = StableAudioModel.from_pretrained(model_id, device=device)
metrics = dict(model=model_id, device=device, gpu=torch.cuda.get_device_name(0) if device == 'cuda' else None,
               load_seconds=round(time.perf_counter() - t_load, 1), runs=[])


def to_array(audio):
    """generate() return type is not pinned in the docs: accept tensor, (sr, tensor) or list."""
    sr = 44100  # SAME autoencoder: stereo 44.1 kHz
    if isinstance(audio, tuple):
        sr, audio = audio
    if isinstance(audio, list):
        audio = audio[0]
    audio = audio.detach().float().cpu()
    if audio.dim() == 3:
        audio = audio[0]
    return sr, audio.T.numpy()  # (samples, channels)


for theme in themes['themes']:
    for seed in themes['seeds']:
        if device == 'cuda':
            torch.cuda.reset_peak_memory_stats()
        t = time.perf_counter()
        audio = model.generate(prompt=theme['prompt'], negative_prompt=themes['negative'],
                               duration=themes['duration'], seed=seed)
        elapsed = time.perf_counter() - t
        sr, data = to_array(audio)
        path = out / f"{theme['id']}_s{seed}.wav"
        sf.write(str(path), data, sr, subtype='PCM_16')
        run = dict(id=theme['id'], seed=seed, seconds=round(elapsed, 1), file=str(path),
                   peak_vram_gb=round(torch.cuda.max_memory_allocated() / 1e9, 2) if device == 'cuda' else None,
                   rss_gb=round(proc.memory_info().rss / 1e9, 2))
        metrics['runs'].append(run)
        print(run, flush=True)
        (out / 'metrics.json').write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding='utf-8')

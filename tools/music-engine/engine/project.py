"""Find the engine and the selected project; load the project's catalog and settings.

The project is chosen with the MSL_PROJECT environment variable (a directory under projects/,
default: projects/monque). A project directory holds catalog.py (PIECES), its score modules,
and project.json (how its tracks are named and grouped in SOUNDVAULT).
"""
import importlib
import json
import os
import sys
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parent
ROOT = ENGINE_DIR.parent


def project_dir():
    return Path(os.environ.get('MSL_PROJECT', ROOT / 'projects' / 'monque')).resolve()


def load_catalog():
    for path in (str(ENGINE_DIR), str(project_dir())):
        if path not in sys.path:
            sys.path.insert(0, path)
    return importlib.import_module('catalog').PIECES


def settings():
    return json.loads((project_dir() / 'project.json').read_text(encoding='utf-8'))

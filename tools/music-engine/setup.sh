#!/usr/bin/env bash
# SOUNDVAULT music engine setup: pinned sample library, patched sfizz renderer, Python env.
# Usage: ./setup.sh            (everything goes into .cache/ and .venv/ next to this script)
# Needs: git, cmake, a C++17 compiler, ffmpeg, python3 (3.11+). On Ubuntu/Debian:
#   sudo apt-get install -y git cmake g++ pkg-config ffmpeg python3-venv
set -euo pipefail
cd "$(dirname "$0")"
ROOT=$(pwd)
VSCO_REPO=https://github.com/sgossner/VSCO-2-CE
VSCO_COMMIT=6dd651d55dde97fd4028699be9d4481f26917891   # branch SFZ (CC0 1.0, ~5 GB)
SFIZZ_REPO=https://github.com/sfztools/sfizz
SFIZZ_COMMIT=f5c6e29f23b8057867c08e88f5f6ac6738baa30b  # branch develop (BSD-2-Clause)
mkdir -p .cache

checkout() {  # checkout <repo> <commit> <dir> [extra clone args]
  local repo=$1 commit=$2 dir=$3; shift 3
  if [ ! -d "$dir/.git" ]; then
    git init -q "$dir"
    git -C "$dir" remote add origin "$repo"
  fi
  if [ "$(git -C "$dir" rev-parse HEAD 2>/dev/null)" != "$commit" ]; then
    git -C "$dir" fetch -q --depth 1 origin "$commit"
    git -C "$dir" checkout -q FETCH_HEAD
  fi
}

if [ -n "${MSL_VSCO:-}" ] && [ -f "$MSL_VSCO/Harp.sfz" ]; then
  echo "== VSCO 2 CE: using MSL_VSCO=$MSL_VSCO"
else
  echo "== VSCO 2 CE @ ${VSCO_COMMIT:0:7} (large download)"
  GIT_LFS_SKIP_SMUDGE=1 checkout "$VSCO_REPO" "$VSCO_COMMIT" .cache/VSCO-2-CE
fi

echo "== sfizz @ ${SFIZZ_COMMIT:0:7} + third_party/sfizz_render_events.patch"
checkout "$SFIZZ_REPO" "$SFIZZ_COMMIT" .cache/sfizz
git -C .cache/sfizz submodule update -q --init --recursive --depth 1
if ! grep -q 'MONQUE SOUND LAB' .cache/sfizz/clients/sfizz_render.cpp; then
  git -C .cache/sfizz apply "$ROOT/third_party/sfizz_render_events.patch"
fi
cmake -S .cache/sfizz -B .cache/sfizz/build -DCMAKE_BUILD_TYPE=Release -DSFIZZ_JACK=OFF -DSFIZZ_RENDER=ON \
      -DENABLE_LTO=OFF -DSFIZZ_SHARED=OFF > .cache/sfizz-cmake.log
cmake --build .cache/sfizz/build -j"$(nproc 2>/dev/null || echo 4)" --target sfizz_render > .cache/sfizz-build.log
test -x .cache/sfizz/build/library/bin/sfizz_render

echo "== Python env (.venv)"
python3 -m venv .venv
.venv/bin/pip install -q -r requirements.txt

command -v ffmpeg > /dev/null || echo "warning: ffmpeg not found (needed by export)"
echo "done. Try: .venv/bin/python msl.py selftest"

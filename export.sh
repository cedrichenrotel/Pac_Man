#!/usr/bin/env bash
set -e

echo "==> Installing/Updating the virtual environment with uv..."
uv sync

echo "==> Removing previous builds..."
rm -rf build dist build_hooks

echo "==> Generating the runtime hook (default config injection)..."
mkdir -p build_hooks
cat > build_hooks/runtime_hook.py << 'EOF'
import sys
import os

if len(sys.argv) == 1:
    base = sys._MEIPASS if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
    sys.argv.append(os.path.join(base, "config.json"))
EOF

echo "==> Packaging with PyInstaller..."
uv run pyinstaller --onefile --name "pacman" \
  --paths . \
  --add-data "assets:assets" \
  --add-data "config.json:." \
  --collect-all mlx \
  --runtime-hook build_hooks/runtime_hook.py \
  src/__main__.py

echo "==> Making the executable executable..."
chmod +x dist/pacman

echo "==> Build completed successfully in the dist/ directory."
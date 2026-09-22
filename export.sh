#!/usr/bin/env bash
set -e

echo "==> Installation/Mise à jour de l'environnement virtuel avec uv..."
uv sync

echo "==> Suppression des anciens builds..."
rm -rf build dist build_hooks

echo "==> Génération du runtime hook (injection config par défaut)..."
mkdir -p build_hooks
cat > build_hooks/runtime_hook.py << 'EOF'
import sys
import os

if len(sys.argv) == 1:
    base = sys._MEIPASS if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
    sys.argv.append(os.path.join(base, "config.json"))
EOF

echo "==> Packaging PyInstaller..."
uv run pyinstaller --onefile --name "pacman" \
  --paths . \
  --add-data "assets:assets" \
  --add-data "config.json:." \
  --collect-all mlx \
  --runtime-hook build_hooks/runtime_hook.py \
  src/__main__.py

echo "==> Rendre l'exécutable exécutable..."
chmod +x dist/pacman

echo "==> Build terminé avec succès dans le dossier dist/"
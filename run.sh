#!/usr/bin/env bash
set -e

echo "==> Installation/Mise à jour de l'environnement virtuel avec uv..."
uv sync

echo "==> Suppression des anciens builds..."
rm -rf build dist

echo "==> Lancement du packaging PyInstaller..."
uv run pyinstaller --noconfirm PacMan.spec

echo "==> Build terminé avec succès dans le dossier dist/"
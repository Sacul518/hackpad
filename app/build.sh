#!/usr/bin/env bash
# Baut die Hackpad-Konfigurator-App als Doppelklick-Programm.
#   macOS  -> dist/Hackpad Konfigurator.app
#   Windows-> dist\Hackpad Konfigurator\Hackpad Konfigurator.exe
#   Linux  -> dist/Hackpad Konfigurator/Hackpad Konfigurator
#
# Voraussetzung: venv mit Abhaengigkeiten + pyinstaller.
#   python3 -m venv .venv
#   .venv/bin/pip install -r requirements.txt pyinstaller
#
# Aufruf (aus dem app/-Ordner):  ./build.sh
set -e
cd "$(dirname "$0")"

PY=.venv/bin/python
[ -x "$PY" ] || PY=python3

"$PY" -m PyInstaller \
  --noconfirm --clean --windowed \
  --name "Hackpad Konfigurator" \
  --collect-all customtkinter \
  main.py

echo
echo "Fertig. Ergebnis liegt in: dist/"

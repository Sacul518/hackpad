# Hackpad Konfigurator (Desktop-App)

GUI zum Konfigurieren des Hackpad: Profile anlegen, jede der 9 Tasten über eine
echte virtuelle Tastatur (QWERTZ, Layout pro Ziel-OS) oder per Custom-Script
belegen, Media-Tasten, und alles als `config.json` aufs Gerät schreiben.

## Starten (aus Quelltext)

```bash
cd app
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python main.py
```

> Hinweis macOS: CustomTkinter braucht Tk 8.6+. Mit Homebrew-Python ggf.
> `brew install python-tk@<version>` installieren.

## Als Doppelklick-App bauen

```bash
cd app
.venv/bin/pip install pyinstaller
./build.sh
```

Ergebnis in `dist/`:
- **macOS:** `Hackpad Konfigurator.app`
- **Windows:** `Hackpad Konfigurator\Hackpad Konfigurator.exe`
- **Linux:** `Hackpad Konfigurator/Hackpad Konfigurator`

Pro Betriebssystem muss einmal auf dem jeweiligen System gebaut werden.

## Aufbau

```
main.py                Einstiegspunkt
hackpad_app/
  ui.py                Fenster/Layout (CustomTkinter)
  keyboard_layouts.py  100%-Tastatur (Windows/Mac, QWERTZ) als Daten
  keynames.py          Tastennamen -> kanonische HID-Codes (Spiegel der Firmware)
  script_parser.py     Custom-Script-Syntax -> Aktions-JSON
  osmap.py             OS-bewusste Modifier/Shortcuts (Cmd vs. Ctrl)
  device.py            CIRCUITPY-Laufwerk erkennen
  config_io.py         config.json laden/speichern
```

Config-Format: siehe [`../docs/config-schema.md`](../docs/config-schema.md).

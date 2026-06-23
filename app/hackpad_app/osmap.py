"""OS-bewusste Tasten-Logik.

Die Firmware ist OS-neutral und fuehrt rohe HID-Codes aus. Die OS-Unterschiede
(Cmd vs. Ctrl, Anzeige-Labels, gaengige Shortcuts) leben hier in der App, damit
man von jedem Rechner aus Profile fuer jedes OS bauen kann.
"""

OSES = ("mac", "windows", "linux")

# Primaer-Modifier je OS (das, was auf dem Mac "Cmd" ist).
_PRIMARY = {"mac": "GUI", "windows": "CONTROL", "linux": "CONTROL"}

# Anzeige-Labels fuer Modifier je OS.
_LABELS = {
    "mac":     {"GUI": "Cmd", "CONTROL": "Ctrl", "ALT": "Opt", "SHIFT": "Shift"},
    "windows": {"GUI": "Win", "CONTROL": "Ctrl", "ALT": "Alt", "SHIFT": "Shift"},
    "linux":   {"GUI": "Super", "CONTROL": "Ctrl", "ALT": "Alt", "SHIFT": "Shift"},
}

# Semantische Shortcuts -> (Primaer-Modifier?, weitere Tasten).
# "PRIMARY" wird je OS zu GUI bzw. CONTROL aufgeloest.
_SHORTCUTS = {
    "Copy":  ["PRIMARY", "C"],
    "Paste": ["PRIMARY", "V"],
    "Cut":   ["PRIMARY", "X"],
    "Undo":  ["PRIMARY", "Z"],
    "Redo":  ["PRIMARY", "SHIFT", "Z"],
    "Save":  ["PRIMARY", "S"],
    "Find":  ["PRIMARY", "F"],
    "SelectAll": ["PRIMARY", "A"],
}


def primary_mod(os_name):
    return _PRIMARY.get(os_name, "CONTROL")


def modifier_label(name, os_name):
    return _LABELS.get(os_name, _LABELS["windows"]).get(name, name)


def resolve(keys, os_name):
    """Ersetzt das Platzhalter-Token 'PRIMARY' durch den OS-Modifier."""
    mod = primary_mod(os_name)
    return [mod if k == "PRIMARY" else k for k in keys]


def shortcut_combo(name, os_name):
    """Semantischer Shortcut -> aufgeloeste Tastenliste fuer eine combo-Aktion."""
    template = _SHORTCUTS.get(name)
    if template is None:
        return None
    return resolve(template, os_name)


def shortcut_names():
    return list(_SHORTCUTS.keys())

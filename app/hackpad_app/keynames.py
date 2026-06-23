"""Tastennamen-Wortschatz der App (Spiegel von firmware/hackpad/keymap.py).

Loest freundliche Namen ("Return", "Cmd", "Left arrow", "1") in die kanonischen
Keycode-Namen auf, die in die config.json geschrieben werden ("ENTER", "GUI",
"LEFT_ARROW", "ONE"). Validiert ausserdem gegen die bekannten Tasten, damit die
App schon Feedback geben kann, bevor etwas aufs Geraet geht.
"""


class KeyNameError(Exception):
    pass


# Freundliche Aliase -> kanonischer Name (muss zu firmware/keymap.py passen).
_ALIASES = {
    "RETURN": "ENTER", "CMD": "GUI", "COMMAND": "GUI", "WIN": "GUI",
    "WINDOWS": "GUI", "SUPER": "GUI", "META": "GUI", "CTRL": "CONTROL",
    "OPT": "ALT", "OPTION": "ALT", "ESC": "ESCAPE", "DEL": "DELETE",
    "LEFT": "LEFT_ARROW", "RIGHT": "RIGHT_ARROW", "UP": "UP_ARROW",
    "DOWN": "DOWN_ARROW", "SPACE": "SPACEBAR", "PAGEUP": "PAGE_UP",
    "PAGEDOWN": "PAGE_DOWN",
    "1": "ONE", "2": "TWO", "3": "THREE", "4": "FOUR", "5": "FIVE",
    "6": "SIX", "7": "SEVEN", "8": "EIGHT", "9": "NINE", "0": "ZERO",
}

_DIGITS = ["ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN",
           "EIGHT", "NINE"]

# Kanonische, gueltige Tastennamen.
CANONICAL = set()
CANONICAL.update(chr(c) for c in range(ord("A"), ord("Z") + 1))   # A..Z
CANONICAL.update(_DIGITS)                                          # ONE..ZERO
CANONICAL.update("F%d" % i for i in range(1, 13))                  # F1..F12
CANONICAL.update([
    "GUI", "CONTROL", "SHIFT", "ALT", "RIGHT_ALT",
    "ENTER", "ESCAPE", "TAB", "SPACEBAR", "BACKSPACE", "DELETE",
    "LEFT_ARROW", "RIGHT_ARROW", "UP_ARROW", "DOWN_ARROW",
    "HOME", "END", "PAGE_UP", "PAGE_DOWN", "INSERT",
    "CAPS_LOCK", "PRINT_SCREEN", "SCROLL_LOCK",
    "MINUS", "EQUALS", "LEFT_BRACKET", "RIGHT_BRACKET", "BACKSLASH",
    "SEMICOLON", "QUOTE", "GRAVE_ACCENT", "COMMA", "PERIOD", "FORWARD_SLASH",
    # Nummernblock
    "KEYPAD_NUMLOCK", "KEYPAD_FORWARD_SLASH", "KEYPAD_ASTERISK",
    "KEYPAD_MINUS", "KEYPAD_PLUS", "KEYPAD_ENTER", "KEYPAD_PERIOD",
    "KEYPAD_ZERO", "KEYPAD_ONE", "KEYPAD_TWO", "KEYPAD_THREE", "KEYPAD_FOUR",
    "KEYPAD_FIVE", "KEYPAD_SIX", "KEYPAD_SEVEN", "KEYPAD_EIGHT", "KEYPAD_NINE",
])

MEDIA = {
    "PLAY_PAUSE", "MUTE", "VOLUME_UP", "VOLUME_DOWN",
    "NEXT_TRACK", "PREV_TRACK", "STOP",
}


def _normalize(name):
    return name.strip().upper().replace(" ", "_").replace("-", "_")


def resolve_name(name):
    """Freundlicher Name -> kanonischer Tastenname. Wirft KeyNameError."""
    key = _normalize(name)
    key = _ALIASES.get(key, key)
    if key not in CANONICAL:
        raise KeyNameError("Unbekannte Taste: %r" % name)
    return key


def is_media(name):
    return _normalize(name) in MEDIA

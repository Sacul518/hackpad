"""Vollstaendige 100%-Tastatur-Layouts (deutsch, QWERTZ) als Daten.

Jede Taste ist ein dict:
  x, y   Position in "Tasteneinheiten" (1u = Standardtaste), oben links = (0,0)
  w, h   Breite/Hoehe in Einheiten
  label  Beschriftung (deutsche Zeichen)
  name   kanonischer HID-Keycode-Name (siehe keynames.py) ODER None = Deko/inaktiv
  mod    True = Modifier (umschaltbar), False = normale Taste

WICHTIG (deutsche Positionen): Die HID-Codes sind positionsbasiert wie eine
US-Tastatur. Auf der deutschen QWERTZ sitzt das "Z" an der US-"Y"-Position und
umgekehrt -> deshalb label "Z" / name "Y" usw. Sonderzeichen (ü ö ä ß) zeigen
auf den US-Code ihrer physischen Position.

Linux nutzt das Windows-Layout.
"""

# Spaltenoffsets der Cluster
NAV_X = 15.5     # Nav-Cluster (Ins/Home/... + Pfeile)
NUM_X = 19.0     # Nummernblock
TOTAL_W = 23.0   # Gesamtbreite in Einheiten
TOTAL_H = 6.4    # Gesamthoehe in Einheiten

# y-Positionen der Reihen (Funktionsreihe oben, dann Luecke)
Y_FN = 0.0
Y_NUM = 1.4
Y_Q = 2.4
Y_A = 3.4
Y_Z = 4.4
Y_SP = 5.4


def _k(x, y, w, label, name, mod=False, h=1.0):
    return {"x": x, "y": y, "w": w, "h": h, "label": label,
            "name": name, "mod": mod}


def _function_row(with_syskeys):
    keys = [_k(0, Y_FN, 1, "Esc", "ESCAPE")]
    cols = [2, 3, 4, 5, 6.5, 7.5, 8.5, 9.5, 11, 12, 13, 14]
    for i, x in enumerate(cols):
        keys.append(_k(x, Y_FN, 1, "F%d" % (i + 1), "F%d" % (i + 1)))
    if with_syskeys:
        keys.append(_k(15.5, Y_FN, 1, "PrtSc", "PRINT_SCREEN"))
        keys.append(_k(16.5, Y_FN, 1, "ScrLk", "SCROLL_LOCK"))
        keys.append(_k(17.5, Y_FN, 1, "Pause", None))
    return keys


def _main_block():
    keys = []
    # Zahlenreihe
    keys.append(_k(0, Y_NUM, 1, "^", "GRAVE_ACCENT"))
    for i in range(1, 10):
        keys.append(_k(i, Y_NUM, 1, str(i), str(i)))
    keys.append(_k(10, Y_NUM, 1, "0", "0"))
    keys.append(_k(11, Y_NUM, 1, "ß", "MINUS"))
    keys.append(_k(12, Y_NUM, 1, "´", "EQUALS"))
    keys.append(_k(13, Y_NUM, 2, "Backspace", "BACKSPACE"))
    # Q-Reihe (QWERTZ)
    keys.append(_k(0, Y_Q, 1.5, "Tab", "TAB"))
    qrow = [("Q", "Q"), ("W", "W"), ("E", "E"), ("R", "R"), ("T", "T"),
            ("Z", "Y"), ("U", "U"), ("I", "I"), ("O", "O"), ("P", "P")]
    for i, (lab, nm) in enumerate(qrow):
        keys.append(_k(1.5 + i, Y_Q, 1, lab, nm))
    keys.append(_k(11.5, Y_Q, 1, "Ü", "LEFT_BRACKET"))
    keys.append(_k(12.5, Y_Q, 1, "+", "RIGHT_BRACKET"))
    # ISO-Enter (hoch, ueber Q- und A-Reihe)
    keys.append(_k(13.75, Y_Q, 1.25, "Enter", "ENTER", h=2))
    # A-Reihe
    keys.append(_k(0, Y_A, 1.75, "Caps", "CAPS_LOCK"))
    arow = list("ASDFGHJKL")
    for i, c in enumerate(arow):
        keys.append(_k(1.75 + i, Y_A, 1, c, c))
    keys.append(_k(10.75, Y_A, 1, "Ö", "SEMICOLON"))
    keys.append(_k(11.75, Y_A, 1, "Ä", "QUOTE"))
    keys.append(_k(12.75, Y_A, 1, "#", "BACKSLASH"))
    # Z-Reihe (QWERTZ: Y an US-Z-Position)
    keys.append(_k(0, Y_Z, 1.25, "Shift", "SHIFT", mod=True))
    keys.append(_k(1.25, Y_Z, 1, "<", None))
    zrow = [("Y", "Z"), ("X", "X"), ("C", "C"), ("V", "V"), ("B", "B"),
            ("N", "N"), ("M", "M")]
    for i, (lab, nm) in enumerate(zrow):
        keys.append(_k(2.25 + i, Y_Z, 1, lab, nm))
    keys.append(_k(9.25, Y_Z, 1, ",", "COMMA"))
    keys.append(_k(10.25, Y_Z, 1, ".", "PERIOD"))
    keys.append(_k(11.25, Y_Z, 1, "-", "FORWARD_SLASH"))
    keys.append(_k(12.25, Y_Z, 2.75, "Shift", "SHIFT", mod=True))
    return keys


def _nav_cluster():
    return [
        _k(15.5, Y_NUM, 1, "Ins", "INSERT"),
        _k(16.5, Y_NUM, 1, "Home", "HOME"),
        _k(17.5, Y_NUM, 1, "PgUp", "PAGE_UP"),
        _k(15.5, Y_Q, 1, "Del", "DELETE"),
        _k(16.5, Y_Q, 1, "End", "END"),
        _k(17.5, Y_Q, 1, "PgDn", "PAGE_DOWN"),
        _k(16.5, Y_Z, 1, "↑", "UP_ARROW"),
        _k(15.5, Y_SP, 1, "←", "LEFT_ARROW"),
        _k(16.5, Y_SP, 1, "↓", "DOWN_ARROW"),
        _k(17.5, Y_SP, 1, "→", "RIGHT_ARROW"),
    ]


def _numpad():
    return [
        _k(19, Y_NUM, 1, "Num", "KEYPAD_NUMLOCK"),
        _k(20, Y_NUM, 1, "/", "KEYPAD_FORWARD_SLASH"),
        _k(21, Y_NUM, 1, "*", "KEYPAD_ASTERISK"),
        _k(22, Y_NUM, 1, "-", "KEYPAD_MINUS"),
        _k(19, Y_Q, 1, "7", "KEYPAD_SEVEN"),
        _k(20, Y_Q, 1, "8", "KEYPAD_EIGHT"),
        _k(21, Y_Q, 1, "9", "KEYPAD_NINE"),
        _k(22, Y_Q, 1, "+", "KEYPAD_PLUS", h=2),
        _k(19, Y_A, 1, "4", "KEYPAD_FOUR"),
        _k(20, Y_A, 1, "5", "KEYPAD_FIVE"),
        _k(21, Y_A, 1, "6", "KEYPAD_SIX"),
        _k(19, Y_Z, 1, "1", "KEYPAD_ONE"),
        _k(20, Y_Z, 1, "2", "KEYPAD_TWO"),
        _k(21, Y_Z, 1, "3", "KEYPAD_THREE"),
        _k(22, Y_Z, 1, "Ent", "KEYPAD_ENTER", h=2),
        _k(19, Y_SP, 2, "0", "KEYPAD_ZERO"),
        _k(21, Y_SP, 1, ",", "KEYPAD_PERIOD"),
    ]


def _bottom_windows():
    return [
        _k(0, Y_SP, 1.25, "Ctrl", "CONTROL", mod=True),
        _k(1.25, Y_SP, 1.25, "Win", "GUI", mod=True),
        _k(2.5, Y_SP, 1.25, "Alt", "ALT", mod=True),
        _k(3.75, Y_SP, 6.25, "", "SPACEBAR"),
        _k(10, Y_SP, 1.25, "AltGr", "RIGHT_ALT", mod=True),
        _k(11.25, Y_SP, 1.25, "Win", "GUI", mod=True),
        _k(12.5, Y_SP, 1.25, "Menu", None),
        _k(13.75, Y_SP, 1.25, "Ctrl", "CONTROL", mod=True),
    ]


def _bottom_mac():
    return [
        _k(0, Y_SP, 1.25, "fn", None),
        _k(1.25, Y_SP, 1.25, "control", "CONTROL", mod=True),
        _k(2.5, Y_SP, 1.25, "option", "ALT", mod=True),
        _k(3.75, Y_SP, 1.5, "command", "GUI", mod=True),
        _k(5.25, Y_SP, 5, "", "SPACEBAR"),
        _k(10.25, Y_SP, 1.5, "command", "GUI", mod=True),
        _k(11.75, Y_SP, 1.25, "option", "ALT", mod=True),
        _k(13.0, Y_SP, 2.0, "control", "CONTROL", mod=True),
    ]


def build(os_name):
    """Liefert die Tastenliste fuer 'windows' | 'linux' | 'mac'."""
    is_mac = os_name == "mac"
    keys = []
    keys += _function_row(with_syskeys=not is_mac)
    keys += _main_block()
    keys += _nav_cluster()
    keys += _numpad()
    keys += _bottom_mac() if is_mac else _bottom_windows()
    return keys

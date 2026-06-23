"""Parser fuer die Custom-Script-Syntax (laeuft nur in der App).

Syntax (siehe docs/config-schema.md):
  (Return) (Left arrow)   -> einzelne Tastendruecke nacheinander  (key)
  (Cmd+C)                 -> Tastenkombi gleichzeitig            (combo)
  "text"                  -> Zeichen fuer Zeichen tippen          (string)
  'text'                  -> "auf einmal einfuegen" (v1: tippen)  (string)

parse() liefert eine fertige, strukturierte Aktion (das, was in die config.json
kommt). Die Firmware parst diesen Text NIE selbst.
"""

import re

from .keynames import resolve_name, KeyNameError


class ParseError(Exception):
    pass


# Token-Reihenfolge ist wichtig: Strings vor allem anderen.
_TOKEN_RE = re.compile(
    r"""
      "(?P<dq>[^"]*)"          # "..."  -> string (schnell tippen)
    | '(?P<sq>[^']*)'          # '...'  -> string (einfuegen)
    | \((?P<paren>[^)]*)\)     # (...)  -> key oder combo
    | (?P<ws>\s+)              # Leerraum
    | (?P<bad>\S)              # alles andere = Fehler
    """,
    re.VERBOSE,
)


def _parse_paren(content):
    content = content.strip()
    if not content:
        raise ParseError("Leere Klammer ()")
    parts = [p.strip() for p in content.split("+") if p.strip()]
    try:
        keys = [resolve_name(p) for p in parts]
    except KeyNameError as e:
        raise ParseError(str(e))
    if len(keys) == 1:
        return {"type": "key", "key": keys[0]}
    return {"type": "combo", "keys": keys}


def parse(text):
    """Script-Text -> Aktion (dict) oder None bei leerem Text."""
    steps = []
    pos = 0
    for m in _TOKEN_RE.finditer(text):
        if m.start() != pos:
            raise ParseError("Unerwartetes Zeichen bei Position %d" % pos)
        pos = m.end()
        if m.group("ws") is not None:
            continue
        if m.group("dq") is not None:
            steps.append({"type": "string", "text": m.group("dq")})
        elif m.group("sq") is not None:
            steps.append({"type": "string", "text": m.group("sq")})
        elif m.group("paren") is not None:
            steps.append(_parse_paren(m.group("paren")))
        else:  # bad
            raise ParseError(
                "Unerwartetes Zeichen %r bei Position %d"
                % (m.group("bad"), m.start())
            )
    if not steps:
        return None
    if len(steps) == 1:
        return steps[0]
    return {"type": "sequence", "steps": steps}

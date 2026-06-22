# Hackpad config.json — Schema & Script-Syntax

Dies ist der **Vertrag zwischen der Konfigurator-App und der Firmware**. Die App
schreibt die `config.json` auf das CIRCUITPY-Laufwerk; die Firmware liest sie nur
und führt rohe HID-Codes aus. **Die ganze OS-Logik liegt in der App** — die
Firmware ist OS-neutral.

## Struktur

```jsonc
{
  "version": 1,
  "active_profile": 0,          // Start-Profil-Index (Firmware nutzt NVM als Override)
  "profiles": [
    {
      "name": "Coding",          // wird auf dem OLED angezeigt
      "target_os": "mac",        // "mac" | "windows" | "linux" — nur Info; Codes sind schon aufgelöst
      "keys": [                  // genau 9 Einträge, Index 0..8 = physische Tasten 1..9
        { "label": "Copy", "action": { ... } }
      ]
    }
  ]
}
```

## Action-Typen

| type       | Felder                | Wirkung |
|------------|-----------------------|---------|
| `combo`    | `keys: [name, ...]`   | Alle Tasten gleichzeitig drücken + loslassen (z. B. `["GUI","C"]` = Cmd+C) |
| `key`      | `key: name`           | Eine einzelne Taste |
| `string`   | `text: "..."`         | Text Zeichen für Zeichen tippen (super schnell) |
| `media`    | `code: name`          | Eine Media-/Consumer-Taste (z. B. `PLAY_PAUSE`) |
| `sequence` | `steps: [action, ...]`| Schritte nacheinander; jeder Schritt ist `key`/`combo`/`string`/`media` |
| `null`     | —                     | Taste tut nichts |

## Tastennamen

Entsprechen den `adafruit_hid.Keycode`-Attributen: `A`–`Z`, `ZERO`–`NINE`,
`F1`–`F12`, `ENTER`, `ESCAPE`, `TAB`, `SPACEBAR`, `BACKSPACE`, `DELETE`,
`LEFT_ARROW`/`RIGHT_ARROW`/`UP_ARROW`/`DOWN_ARROW`, `HOME`/`END`/`PAGE_UP`/`PAGE_DOWN`.

Modifier: `GUI` (= Cmd/Win/Super), `CONTROL`, `SHIFT`, `ALT`.

Freundliche Aliase (von der Firmware akzeptiert): `Return`→`ENTER`, `Cmd`/`Win`→`GUI`,
`Ctrl`→`CONTROL`, `Opt`/`Option`→`ALT`, `Esc`, `Left`/`Right`/`Up`/`Down`, `Space`.

Media-Namen: `PLAY_PAUSE`, `MUTE`, `VOLUME_UP`, `VOLUME_DOWN`, `NEXT_TRACK`,
`PREV_TRACK`, `STOP`.

## Script-Syntax (nur in der App)

Im Custom-Script-Editor tippt man Aktionen kompakt; **die App parst das** und
schreibt daraus die strukturierte JSON oben. Die Firmware sieht nie diesen Text.

| Eingabe                       | wird zu |
|-------------------------------|---------|
| `(Return)` `(Left arrow)`     | `key`-Schritte (Tastendrücke nacheinander) |
| `"text"` (doppelte Quotes)    | `string` — Zeichen für Zeichen super schnell getippt |
| `'text'` (einfache Quotes)    | `string` — "auf einmal einfügen" (v1: ebenfalls schnell getippt) |

Beispiel: `(Return) "fertig" (Return)` →
```json
{ "type": "sequence", "steps": [
  { "type": "key", "key": "ENTER" },
  { "type": "string", "text": "fertig" },
  { "type": "key", "key": "ENTER" }
]}
```

## OS-Übersetzung (App-Aufgabe)

Die App übersetzt hohe Aktionen je nach `target_os` in rohe Codes, z. B.
„Kopieren": `GUI+C` (mac) bzw. `CONTROL+C` (windows/linux). So kann man von
jedem Rechner aus Profile für jedes OS bauen.

## Persistenz des aktiven Profils

Die Firmware speichert das zuletzt **bestätigte** Profil in
`microcontroller.nvm` (1 Byte). Das überlebt Neustart/Reload, ohne das
USB-Laufwerk für den Host schreibzuschützen.

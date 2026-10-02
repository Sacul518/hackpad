# Profile für Lucas' Mac

`mac-qwertz.json` enthält Media, Code, Alltag, Browser und das bisherige
Profil `test`. Die Konfiguration vor der Erweiterung liegt unter
`backups/2026-10-02-before-mac-profiles.json`.

Die Tasten werden von oben links nach unten rechts nummeriert:

```text
1  2  3
4  5  6
7  8  9
```

| Taste | Media | Code (VS Code) | Alltag | Browser |
|---|---|---|---|---|
| 1 | Vorheriger Titel | Kopieren | Kopieren | Neuer Tab |
| 2 | Play / Pause | Einfügen | Einfügen | Geschlossenen Tab wiederherstellen |
| 3 | Nächster Titel | Ausschneiden | Ausschneiden | Tab schließen |
| 4 | Leiser | Rückgängig | Rückgängig | Vorheriger Tab |
| 5 | Stumm | Wiederholen | Wiederholen | Neu laden |
| 6 | Lauter | Speichern | Alles markieren | Nächster Tab |
| 7 | Pfeil links | Befehlspalette | Spotlight | Adresszeile |
| 8 | Stop | Datei schnell öffnen | Screenshot eines Bereichs | Seite durchsuchen |
| 9 | Pfeil rechts | Dokument formatieren | Emoji-Auswahl | Escape |

Drehknopf drehen → Profil vorschauen. Drücken → Profil bestätigen.
Die Auswahl bleibt nach dem Neustart erhalten. Das Pack startet bei der
Installation mit Media; die Firmware speichert die Auswahl zusätzlich im NVM.

Die Belegungen sind für **macOS mit deutscher QWERTZ-Eingabequelle** ausgelegt.
Rückgängig ist ⌘Z, Wiederholen ⇧⌘Z. Dafür steht in der JSON der rohe HID-Code
`Y`: Diese physische Taste trägt auf dem deutschen Layout ein Z, wie bereits
im Tastaturlayout der Konfigurator-App hinterlegt.

Code benutzt die Standardbelegung von VS Code. Eigene Tastenkürzel können
abweichen. Formatieren braucht einen passenden Formatter für die Datei.
Browser nutzt übliche macOS-Browserkürzel, anhand von Safari geprüft.
Medientasten brauchen einen Player, der die jeweiligen Befehle unterstützt;
die Pfeiltasten bleiben normale Pfeiltasten und ihre Wirkung hängt vom Player ab.

Quellen: [VS Code: Standardkürzel](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-macos.pdf),
[macOS: Tastenkürzel](https://support.apple.com/en-us/102650),
[Safari: Tastenkürzel](https://support.apple.com/en-gb/guide/safari/cpsh003/mac).

## Installationsstand am 02.10.2026

Die JSON, 9 Tasten je Profil und alle verwendeten Tastennamen wurden lokal
geprüft. Die alte Konfiguration ist gesichert. Die Datei wurde auf das
Hackpad kopiert und bytegenau verifiziert. Beide App-Arbeitskopien wurden
aktualisiert; nach dem Neustart zeigt die App die vier neuen Profile und
`Media (1/5)` an.

Der erste serielle Test erreichte vor dem Schreiben noch keinen REPL-Prompt;
die Dateiänderung löste einen automatischen Neustart aus. Anschließend
reagierte die Konsole auch nach explizitem Setzen von DTR/RTS nicht auf die
REPL-Anforderung. Nach einem physischen Reset bestätigte Lucas die Anzeige
`Hackpad / Media`. Der Start und das aktive Media-Profil sind damit auch am
Gerät bestätigt. Die serielle Prüfung der Tastennamen mit den echten
Board-Bibliotheken wurde nicht abgeschlossen. Alle Aktionen in ihren
jeweiligen Mac-Programmen müssen noch mit den physischen Tasten getestet werden.

# Fehler beim ersten Start — 02.10.2026

## Beobachtung und bestätigte Ursache

Das OLED zeigte die CircuitPython-Fehlerkonsole statt der Hackpad-Anzeige.
Ein Neustart über USB reproduzierte auf dem aufgebauten XIAO RP2040:

```text
File "code.py", line 66, in main
RuntimeError: Pins must be sequential GPIO pins
```

Die Firmware verwendete `rotaryio.IncrementalEncoder(board.D8, board.D9)`.
D8/D9 sind auf diesem Board GPIO2/GPIO4. Die RP2040-Implementierung von
`rotaryio` verlangt direkt benachbarte GPIOs. Die Platinenanschlüsse bleiben
unverändert; die Auswertung muss diese Pinbelegung unterstützen.

Quellen: [Seeed: Pinbelegung des XIAO RP2040](https://wiki.seeedstudio.com/XIAO-RP2040/),
[CircuitPython: Erklärung der GPIO-Einschränkung](https://github.com/adafruit/circuitpython/issues/5334)
und [keypad-API für CircuitPython 10.3.1](https://docs.circuitpython.org/en/10.3.1/shared-bindings/keypad/index.html).

## Korrektur

`firmware/hackpad/encoder.py` scannt beide Kontakte über `keypad.Keys` mit
internen Pull-ups alle 1 ms im Hintergrund. Vier gültige Übergänge ergeben
einen Positionsschritt. Rückwärtsbewegungen und Kontaktprellen werden
verrechnet. Gleichzeitige Änderungen beider Kontakte sowie ein voller
Ereignispuffer führen zur Synchronisierung statt zu erfundenen Drehschritten.
Bei sehr schnellem Drehen können Übergänge zwischen zwei Scans verloren gehen.

`code.py` verwendet diese Auswertung. Quellfirmware und Produktionskopie
wurden aktualisiert; `code.py` und `hackpad/encoder.py` wurden auf das
angeschlossene `CIRCUITPY`-Laufwerk kopiert und bytegenau verglichen.
Die bisherige `code.py` ist unter
`/private/tmp/hackpad-before-encoder-fix-20261002/code.py` gesichert.

## Verifikation

- Zwölf lokale Signaltests bestanden: Stillstand, beide Richtungen,
  Teilschritte, Prellen, Richtungswechsel, gleichzeitige Änderungen,
  fehlende Übergänge, alle vier Startzustände, Pufferüberlauf, mehrere
  gepufferte Umdrehungen, Pinfreigabe und identische Produktionskopie.
- Syntax aller neun Python-Dateien je Firmware-Ordner geprüft.
- Echter Start mit CircuitPython 10.3.1 auf dem XIAO RP2040:
  `Hackpad bereit. Profile: 2`; anschließend zwölf Sekunden ohne Traceback
  oder OLED-Initialisierungswarnung.
- Nach dem Aufspielen sendete Lucas `Hallo vom Hackpad!`, genau den für die
  Texttaste konfigurierten Text. Damit ist die Textausgabe am Mac auch im
  Bedienungstest bestätigt.
- Drehknopf, Klick und die übrigen acht Tasten sind noch nicht bestätigt;
  die lokalen Signaltests ersetzen diese physischen Bedienungstests nicht.

## Regel für weitere Änderungen

Bei RP2040-Pinbelegungen die tatsächlichen GPIO-Nummern prüfen, nicht nur
die D-Nummern. Nach jeder Firmware-Änderung den echten Start über USB prüfen;
ein erfolgreicher Dateitransfer oder Syntaxcheck reicht nicht aus.

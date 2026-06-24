# Hackpad

A custom 9-key mechanical macropad with a rotary encoder and OLED display, built around the **Seeed XIAO RP2040**. Designed from scratch in KiCad as part of [Hack Club's Hackpad YSWS](https://hackpad.hackclub.com/).

## Features

- **3×3 mechanical switch matrix** (9× Cherry MX–compatible keys) with per-key 1N4148 diodes for full n-key rollover
- **Rotary encoder** (EC11) with push button — for volume, scrolling, etc.
- **0.96" OLED display** (SSD1306, I²C) for layer/status info
- **Seeed XIAO RP2040** microcontroller (through-hole)
- Custom PCB + 3D-printed case

## Hardware

| Part | Component |
|------|-----------|
| MCU | Seeed XIAO RP2040 (THT) |
| Switches | 9× Cherry MX–compatible (PCB-mount) |
| Diodes | 9× 1N4148 (THT, COL→ROW) |
| Encoder | 1× EC11 rotary encoder with switch |
| Display | 1× SSD1306 0.96" OLED (4-pin I²C) |

### Pin mapping (XIAO RP2040)

| Function | Pin | | Function | Pin |
|----------|-----|---|----------|-----|
| COL0 | D0 | | ROW0 | D3 |
| COL1 | D1 | | ROW1 | D6 |
| COL2 | D2 | | ROW2 | D7 |
| Encoder A | D8 | | OLED SDA | D4 |
| Encoder B | D9 | | OLED SCL | D5 |
| Encoder SW | D10 | | | |

Matrix is wired **COL2ROW**: column → switch → diode anode, diode cathode → row.

## Project status

- [x] Schematic (ERC clean)
- [x] PCB layout — components placed, all nets routed
- [x] Rounded board outline (68 × 99.68 mm — under the 100 × 100 mm limit)
- [x] Mounting holes (4× M2)
- [x] GND copper pour (both layers)
- [x] DRC clean (apart from intentional diode-under-switch placement)
- [x] STEP 3D model exported (for case design)
- [x] Case — bottom tray (Tinkercad: walls, USB cutout, 4× M2 standoffs, PCB anti-flex support grid)
- [x] Case — top frame (open design, XIAO RP2040 exposed, 9× switch openings, encoder cutout, name/branding)
- [x] Case fitted to resized PCB & exported as STL (no-supports, printer-friendly orientation)
- [x] Firmware — CircuitPython base (matrix, encoder profile-browser, OLED, JSON-config macro engine)
- [ ] Firmware — hardware bring-up & test (pending physical board)
- [x] Configurator app — base GUI (Python + CustomTkinter: device detect, profiles, key editor, save to device)
- [x] Configurator app — full 100% virtual keyboard (QWERTZ, per-OS Win/Mac layout), scrollable profiles, double-click build (PyInstaller)
- [ ] Configurator app — cross-OS packaging (Windows .exe / Linux build)

## Repository layout

```
hackpad.kicad_pro    KiCad project
hackpad.kicad_sch    Schematic
hackpad.kicad_pcb    PCB layout
KiCAD-lib/           Project-specific footprints
export/hackpad.step  3D model of the PCB (reference for case design)
case/                3D-printed case model (Tinkercad → STL: tray + open top frame)
firmware/            CircuitPython firmware (config-driven macro engine)
app/                 Configurator GUI (Python + CustomTkinter)
docs/                config.json schema & script-syntax contract
```

## Building

PCB is designed for fabrication at JLCPCB (2-layer). Firmware and assembly
instructions will follow once the hardware is finalized.

## Use of AI in this project

I want to be transparent about how AI (Claude) was used here:

- **PCB design** — done entirely by me, by hand, in KiCad. The AI did **not**
  create the schematic or the board layout. It only made suggestions and
  answered questions when I got stuck (e.g. how to shrink the outline under
  100 mm without moving my mounting holes). Every footprint placement, trace
  and the final layout decisions are mine.
- **3D case** — designed entirely by me in Tinkercad. The AI did **not** model
  the case. It only answered questions about the program's rules (size limits,
  the no-supports requirement, tolerances) and reviewed my exported STL against
  those rules. The geometry, the open design and the support structure are mine.
- **Firmware** — here the AI did the heavy lifting: I set the direction and the
  vision (encoder browses profiles, OLED status screen, each of the 9 keys
  freely assignable, JSON-config-driven macro engine), and the AI implemented
  the CircuitPython code to match that.
- **Configurator app** — built collaboratively from my concept (the layout and
  feature set come from my sketch/PDF), with the AI writing much of the
  CustomTkinter code.

In short: **hardware (PCB + case) is my own work**; the AI assisted mainly on
the software side and as a sounding board for questions.

## Acknowledgements

Built as part of the **Hack Club Hackpad** program. Hardware design and layout
done by hand in KiCad — this was my first PCB. 🎉

## License

To be decided (likely MIT for firmware, CERN-OHL or CC-BY-SA for hardware).

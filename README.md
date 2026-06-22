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
- [x] Rounded board outline (~68 × 105 mm)
- [x] Mounting holes (4× M2)
- [x] GND copper pour (both layers)
- [x] DRC clean (apart from intentional diode-under-switch placement)
- [x] STEP 3D model exported (for case design)
- [x] Case — bottom tray (Tinkercad: walls, USB cutout, 4× M2 standoffs, encoder support boss)
- [x] Case — top plate (open/tray-mount style: large switch opening, OLED window, encoder cutout)
- [ ] Firmware (QMK / KMK — TBD)

## Repository layout

```
hackpad.kicad_pro    KiCad project
hackpad.kicad_sch    Schematic
hackpad.kicad_pcb    PCB layout
KiCAD-lib/           Project-specific footprints
export/hackpad.step  3D model of the PCB (reference for case design)
case/                3D-printed case models (Tinkercad → STL)
```

## Building

PCB is designed for fabrication at JLCPCB (2-layer). Firmware and assembly
instructions will follow once the hardware is finalized.

## Acknowledgements

Built as part of the **Hack Club Hackpad** program. Hardware design and layout
done by hand in KiCad — this was my first PCB. 🎉

## License

To be decided (likely MIT for firmware, CERN-OHL or CC-BY-SA for hardware).

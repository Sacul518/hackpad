# Production files

Everything needed to actually build this Hackpad — PCB fabrication, 3D printing
and flashing — in one folder.

```
gerbers.zip                             PCB fabrication files (JLCPCB-ready)
case/Hackpad-Case-1-Bottom-Tray.stl     3D print part 1 of 2
case/Hackpad-Case-2-Top-Plate.stl       3D print part 2 of 2
firmware/                               Final firmware, ready to drag onto CIRCUITPY
bom.csv                                 Bill of materials
```

## 1. PCB — `gerbers.zip`

2-layer board, **68 × 99.68 mm**, 1.6 mm FR4, HASL. Upload the zip as-is to
JLCPCB (or any fab) — no changes needed. Contents:

| File | Layer |
|------|-------|
| `hackpad-F_Cu.gbr` / `hackpad-B_Cu.gbr` | copper top / bottom |
| `hackpad-F_Mask.gbr` / `hackpad-B_Mask.gbr` | solder mask top / bottom |
| `hackpad-F_Silkscreen.gbr` / `hackpad-B_Silkscreen.gbr` | silkscreen top / bottom |
| `hackpad-Edge_Cuts.gbr` | board outline |
| `hackpad.drl` | drill file |
| `hackpad-job.gbrjob` | Gerber job file |

No paste layer — the board is 100 % through-hole and hand-soldered.

## 2. Case — 2 printed parts

Both parts are separate, watertight STLs, already oriented flat on the build
plate. **No supports needed.**

| Part | File | Size (X × Y × Z) |
|------|------|------------------|
| Bottom tray | `case/Hackpad-Case-1-Bottom-Tray.stl` | 73.0 × 106.5 × 7.0 mm |
| Top plate | `case/Hackpad-Case-2-Top-Plate.stl` | 73.0 × 106.0 × 2.0 mm |

Print settings I used: PLA, 0.2 mm layer height, 3 walls, 20 % infill, no
supports, no brim. The tray contains the 4× M2 standoffs (self-tapping Ø1.7 mm
holes), the encoder support boss and the anti-flex support grid under the PCB —
all printed in one piece with the tray.

Assembly: PCB drops into the tray onto the standoffs, top plate goes on top,
4× M2 screws from the top hold the stack together.

## 3. Firmware — `firmware/`

The Hackpad runs **CircuitPython**, so there is no compiled binary — the `.py`
files *are* the final firmware. This folder is the complete, ready-to-use
`CIRCUITPY` drive content, including the Adafruit libraries.

```
boot.py            enables HID (keyboard + consumer control)
code.py            main program: matrix scan, encoder, OLED, main loop
config.json        default configuration (Media + Coding profile)
hackpad/           macro engine, keymap, config loader, profiles, OLED display
lib/               Adafruit libraries (CircuitPython 10.x, .mpy)
```

### Flashing

1. Plug in the XIAO RP2040, hold **BOOT**, tap **RESET**, release BOOT — the
   drive `RPI-RP2` appears.
2. Drag the **CircuitPython 10.x `.uf2`** for *Seeed XIAO RP2040*
   (from [circuitpython.org](https://circuitpython.org/board/seeeduino_xiao_rp2040/))
   onto `RPI-RP2`. The board reboots as `CIRCUITPY`.
3. Copy **everything inside this `firmware/` folder** (`boot.py`, `code.py`,
   `config.json`, `hackpad/`, `lib/`) onto the `CIRCUITPY` drive.
4. Done — the firmware starts automatically. Editing any file (including
   `config.json`) triggers an auto-reload.

> The bundled `lib/` is the **10.x** `.mpy` build, so use CircuitPython 10.x.
> With CircuitPython 9.x, replace `lib/` with the matching 9.x bundle.

Keys are reconfigured with the desktop app in [`../app/`](../app/), which writes
a new `config.json` straight to the `CIRCUITPY` drive. The config format is
documented in [`../docs/config-schema.md`](../docs/config-schema.md).

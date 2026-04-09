# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
./simpleclock.sh        # preferred: checks dependencies, runs clock.py in background
python3 clock.py        # run directly in foreground
```

`simpleclock.sh` requires `python3` and `tkinter` (OS package `python3-tk` on Debian/Ubuntu). Both files use only Python 3 stdlib — no pip installs.

## Architecture

The entire app is `clock.py`, a single-file tkinter GUI with no external dependencies.

**Rendering pipeline:**
- `SEGMENTS` dict maps digit characters `'0'–'9'` to a 7-tuple of on/off bits `(a, b, c, d, e, f, g)` following standard 7-segment layout.
- `draw_digit(canvas, x, y, ch)` computes absolute pixel rectangles for all 7 segments and draws each as a filled `canvas.create_rectangle` — active segments in `ACTIVE` green, inactive in `DIM` ghost green.
- `draw_colon(canvas, cx, y, visible)` draws two oval dots; visibility drives the per-second blink.
- `ClockApp._update()` redraws the entire canvas on every call (no diffing), scheduled via `root.after(200, self._update)`.

**Layout:**
Digit positions are hardcoded pixel constants on `ClockApp` (`H1_X`, `H2_X`, `COL1_X`, … `S2_X`). Canvas is fixed at 510×150 px. The date is a separate `tk.Label` below the canvas.

**Key behaviors:**
- Clicking the canvas calls `toggle_mode()`, flipping `self.use_24h`.
- AM/PM label is rendered only when `use_24h` is `False`.
- Colons blink by toggling on even/odd seconds (`second % 2 == 0`).
- Date uses `%-d` (Linux only) to strip leading zero from day.

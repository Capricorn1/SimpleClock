import tkinter as tk
from datetime import datetime

BG      = "#111111"
ACTIVE  = "#00FF41"
DIM     = "#0a2010"
DATE_FG = "#449944"
HINT_FG = "#1a3a1a"

# Segment order: a, b, c, d, e, f, g
#  aaa
# f   b
# f   b
#  ggg
# e   c
# e   c
#  ddd
SEGMENTS = {
    '0': (1, 1, 1, 1, 1, 1, 0),
    '1': (0, 1, 1, 0, 0, 0, 0),
    '2': (1, 1, 0, 1, 1, 0, 1),
    '3': (1, 1, 1, 1, 0, 0, 1),
    '4': (0, 1, 1, 0, 0, 1, 1),
    '5': (1, 0, 1, 1, 0, 1, 1),
    '6': (1, 0, 1, 1, 1, 1, 1),
    '7': (1, 1, 1, 0, 0, 0, 0),
    '8': (1, 1, 1, 1, 1, 1, 1),
    '9': (1, 1, 1, 1, 0, 1, 1),
}

DW = 50   # digit width
DH = 90   # digit height
ST = 9    # segment thickness
SG = 3    # gap at segment tips


def draw_digit(canvas, x, y, ch):
    bits = SEGMENTS.get(ch, (0, 0, 0, 0, 0, 0, 0))
    segs = [
        (x + SG,      y,                x + DW - SG,    y + ST),              # a top
        (x + DW - ST, y + SG,           x + DW,         y + DH // 2 - SG),    # b top-right
        (x + DW - ST, y + DH // 2 + SG, x + DW,         y + DH - SG),         # c bot-right
        (x + SG,      y + DH - ST,      x + DW - SG,    y + DH),              # d bottom
        (x,           y + DH // 2 + SG, x + ST,         y + DH - SG),         # e bot-left
        (x,           y + SG,           x + ST,         y + DH // 2 - SG),    # f top-left
        (x + SG,      y + DH // 2 - ST // 2,
                                         x + DW - SG,   y + DH // 2 + ST // 2),  # g middle
    ]
    for i, (x1, y1, x2, y2) in enumerate(segs):
        canvas.create_rectangle(x1, y1, x2, y2,
                                 fill=ACTIVE if bits[i] else DIM,
                                 outline="")


def draw_colon(canvas, cx, y, visible):
    color = ACTIVE if visible else DIM
    r = 5
    q = DH // 3
    canvas.create_oval(cx - r, y + q - r,     cx + r, y + q + r,     fill=color, outline="")
    canvas.create_oval(cx - r, y + 2 * q - r, cx + r, y + 2 * q + r, fill=color, outline="")


class ClockApp:
    # Pixel layout
    Y      = 32     # top of digit row
    H1_X   = 25
    H2_X   = 79     # H1_X + DW + 4
    COL1_X = 146    # H2_X + DW + 17 (6px gap + 11px half-colon)
    M1_X   = 163    # COL1_X + 17
    M2_X   = 217    # M1_X + DW + 4
    COL2_X = 284    # M2_X + DW + 17
    S1_X   = 301    # COL2_X + 17
    S2_X   = 355    # S1_X + DW + 4
    AMPM_X = 425    # centered label past S2
    CW     = 510
    CH     = 150

    def __init__(self):
        self.use_24h = False
        self.root = tk.Tk()
        self.root.title("SimpleClock")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            self.root, width=self.CW, height=self.CH,
            bg=BG, highlightthickness=0,
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", lambda e: self.toggle_mode())

        self.date_label = tk.Label(
            self.root, text="", bg=BG, fg=DATE_FG,
            font=("Courier", 13),
        )
        self.date_label.pack(pady=(0, 14))

        self._update()
        self.root.mainloop()

    def toggle_mode(self):
        self.use_24h = not self.use_24h

    def _update(self):
        now = datetime.now()
        c = self.canvas
        c.delete("all")

        if self.use_24h:
            h, ampm = now.hour, None
        else:
            h = now.hour % 12 or 12
            ampm = "AM" if now.hour < 12 else "PM"

        h_str  = f"{h:02d}"
        m_str  = f"{now.minute:02d}"
        s_str  = f"{now.second:02d}"
        blink  = (now.second % 2 == 0)
        Y      = self.Y

        draw_digit(c, self.H1_X,  Y, h_str[0])
        draw_digit(c, self.H2_X,  Y, h_str[1])
        draw_colon(c, self.COL1_X, Y, blink)
        draw_digit(c, self.M1_X,  Y, m_str[0])
        draw_digit(c, self.M2_X,  Y, m_str[1])
        draw_colon(c, self.COL2_X, Y, blink)
        draw_digit(c, self.S1_X,  Y, s_str[0])
        draw_digit(c, self.S2_X,  Y, s_str[1])

        if ampm:
            c.create_text(
                self.AMPM_X, Y + DH // 2,
                text=ampm, fill=ACTIVE,
                font=("Courier", 20, "bold"),
                anchor="center",
            )

        c.create_text(
            self.CW - 6, self.CH - 6,
            text="click to toggle 12H/24H", fill=HINT_FG,
            font=("Courier", 9), anchor="se",
        )

        self.date_label.config(text=now.strftime("%A, %B %-d %Y"))
        self.root.after(200, self._update)


if __name__ == "__main__":
    ClockApp()

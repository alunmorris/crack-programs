# counter_demo.py — animated counter using monospaced terminal
import time

tft.fill(0x0000)
term = _TFTTerminal(tft, None, font=mono13)

def mprint(*args, **kwargs):
    sep = kwargs.get('sep', ' ')
    end = kwargs.get('end', '\n')
    term.write(sep.join(str(a) for a in args) + end)

mprint("+-------------------+")
mprint("| Counter:          |")
mprint("| Elapsed:          |")
mprint("+-------------------+", end="")

start = time.ticks_ms()
for i in range(200):
    elapsed = time.ticks_diff(time.ticks_ms(), start) // 1000
    mprint(f"\x1b[2A\x1b[2K| Counter: {i:<9}|", end="\n")
    mprint(f"\x1b[2K| Elapsed: {elapsed:<7}s  |", end="\n")
    mprint("\x1b[2K+-------------------+", end="")
    time.sleep_ms(100)

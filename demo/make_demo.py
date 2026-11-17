"""Record the README demo GIF.

    uv run --no-project --with pyte --with pillow python demo/make_demo.py

Plays a scripted session of the real game in a pseudo-terminal (sit down,
tip, bet on 17, a near miss, rebet, a rigged straight-up win), replays the
output through a terminal emulator and writes demo/demo.gif with ffmpeg.

The game runs against a throwaway save file, never your own. Each spin is
reseeded (SPIN_SEEDS) so the near miss and the rigged win happen on cue;
nothing in the game itself is changed.
"""
import fcntl
import importlib.machinery
import importlib.util
import json
import os
import pty
import random
import select
import shutil
import struct
import subprocess
import sys
import tempfile
import termios
import time
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.join(HERE, "..", "roulette")
OUT_GIF = os.path.join(HERE, "demo.gif")
COLS, ROWS = 80, 30
SPIN_SEEDS = [30, 2]          # spin 1: near miss on 17; spin 2: rigged straight-up win
CROUPIER = "Penelope"

# (keys to type, seconds to wait afterwards). Typing is shown one key at a time.
SCRIPT = [
    ("tip 12\n", 2.6),
    ("5 on 17\n", 2.2),
    ("\n", 5.0),               # spin 1
    ("rebet\n", 1.4),
    ("\n", 7.5),               # spin 2
]
TYPE_DELAY = 0.07


# ---------------------------------------------------------------------------
# 1. Driver: runs inside the pseudo-terminal
# ---------------------------------------------------------------------------
def driver(home):
    os.environ["HOME"] = home
    loader = importlib.machinery.SourceFileLoader("roulette_game", GAME)
    spec = importlib.util.spec_from_loader("roulette_game", loader)
    rl = importlib.util.module_from_spec(spec)
    loader.exec_module(rl)
    rl.FLAVOR.seed(1)
    random.seed(1)
    seeds = list(SPIN_SEEDS)
    real_play_round = rl.play_round

    def play_round(*args, **kwargs):
        if seeds and kwargs.get("state") is not None:
            seed = seeds.pop(0)
            random.seed(seed)
            rl.FLAVOR.seed(seed)
        return real_play_round(*args, **kwargs)

    rl.play_round = play_round
    sys.exit(rl.main([]))


def fresh_home():
    home = tempfile.mkdtemp(prefix="roulette-demo-")
    os.makedirs(os.path.join(home, ".roulette"))
    state = {"chips": 100, "croupier": CROUPIER, "seen_help": 1, "fast": 1}
    with open(os.path.join(home, ".roulette", "state.json"), "w") as f:
        json.dump(state, f)
    return home


# ---------------------------------------------------------------------------
# 2. Recorder: drive the game and timestamp its output
# ---------------------------------------------------------------------------
def record():
    home = fresh_home()
    events, start = [], time.time()

    def stamp(data):
        events.append((time.time() - start, data))

    # A fake shell prompt, typed out.
    stamp("\x1b[1;32m$\x1b[0m ")
    for ch in "roulette":
        time.sleep(TYPE_DELAY)
        stamp(ch)
    time.sleep(0.4)
    stamp("\r\n")

    pid, fd = pty.fork()
    if pid == 0:
        os.environ.update(TERM="xterm-256color", COLUMNS=str(COLS), LINES=str(ROWS))
        os.execvp(sys.executable, [sys.executable, os.path.abspath(__file__), "--driver", home])
    fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", ROWS, COLS, 0, 0))

    def pump(seconds):
        end = time.time() + seconds
        while time.time() < end:
            ready, _, _ = select.select([fd], [], [], 0.02)
            if ready:
                try:
                    data = os.read(fd, 65536)
                except OSError:
                    return
                if not data:
                    return
                stamp(data.decode("utf-8", "replace"))

    pump(2.5)
    for keys, wait in SCRIPT:
        for ch in keys:
            os.write(fd, ch.encode())
            pump(TYPE_DELAY)
        pump(wait)
    try:
        os.kill(pid, 9)
    except ProcessLookupError:
        pass
    shutil.rmtree(home, ignore_errors=True)
    return events


# ---------------------------------------------------------------------------
# 3. Renderer: terminal emulator -> frames -> GIF
# ---------------------------------------------------------------------------
PALETTE = {
    "black": (40, 42, 54), "red": (255, 85, 85), "green": (80, 250, 123),
    "brown": (241, 250, 140), "yellow": (241, 250, 140), "blue": (98, 114, 164),
    "magenta": (255, 121, 198), "cyan": (139, 233, 253), "white": (230, 230, 230),
    "default": (230, 230, 230),
}
BRIGHT = {"red": (255, 110, 110), "green": (105, 255, 148), "yellow": (255, 255, 165),
          "brown": (255, 255, 165), "cyan": (164, 255, 255), "white": (255, 255, 255),
          "black": (98, 114, 164), "magenta": (255, 146, 223), "blue": (123, 139, 189)}
BG = (30, 31, 41)
BG_COLORS = {"red": (200, 40, 40), "black": (20, 20, 24), "green": (30, 140, 60)}
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
FONT_SIZE, CELL_W, CELL_H, PAD = 15, 9, 19, 14
FPS = 12


def render(events):
    import pyte
    from PIL import Image, ImageDraw, ImageFont

    font = ImageFont.truetype(FONT, FONT_SIZE)
    bold = ImageFont.truetype(FONT.replace("Mono.ttf", "Mono-Bold.ttf"), FONT_SIZE)
    emoji_font = ImageFont.truetype(EMOJI_FONT, 109)
    emoji_cache = {}

    def emoji(ch):
        if ch not in emoji_cache:
            img = Image.new("RGBA", (136, 128), (0, 0, 0, 0))
            ImageDraw.Draw(img).text((0, 0), ch, font=emoji_font, embedded_color=True)
            box = img.getbbox() or (0, 0, 1, 1)
            img = img.crop(box)
            size = CELL_H - 2
            img.thumbnail((size * 2, size), Image.LANCZOS)
            emoji_cache[ch] = img
        return emoji_cache[ch]

    screen = pyte.Screen(COLS, ROWS)
    stream = pyte.Stream(screen)
    width, height = COLS * CELL_W + 2 * PAD, ROWS * CELL_H + 2 * PAD
    frames_dir = tempfile.mkdtemp(prefix="roulette-frames-")

    def draw_frame(path):
        img = Image.new("RGB", (width, height), BG)
        d = ImageDraw.Draw(img)
        for y in range(ROWS):
            line = screen.buffer[y]
            x = 0
            while x < COLS:
                cell = line[x]
                ch = cell.data or " "
                px, py = PAD + x * CELL_W, PAD + y * CELL_H
                wide = unicodedata.east_asian_width(ch[:1]) in "WF" if ch.strip() else False
                span = 2 if wide else 1
                if cell.bg in BG_COLORS:
                    d.rectangle([px, py, px + span * CELL_W - 1, py + CELL_H - 1],
                                fill=BG_COLORS[cell.bg])
                fg = (BRIGHT if cell.bold else PALETTE).get(cell.fg, PALETTE["default"])
                if cell.fg == "white" and not cell.bold and cell.bg == "default":
                    fg = (150, 152, 165)  # the game's "dim" text
                if wide and ord(ch[0]) > 0x2000:
                    g = emoji(ch)
                    img.paste(g, (px + (span * CELL_W - g.width) // 2,
                                  py + (CELL_H - g.height) // 2), g)
                elif ch.strip():
                    d.text((px, py + 1), ch, font=bold if cell.bold else font, fill=fg)
                x += span
        cur = screen.cursor
        if not screen.cursor.hidden and cur.y < ROWS:
            d.rectangle([PAD + cur.x * CELL_W, PAD + cur.y * CELL_H + CELL_H - 3,
                         PAD + cur.x * CELL_W + CELL_W - 1, PAD + cur.y * CELL_H + CELL_H - 1],
                        fill=(200, 200, 200))
        img.save(path)

    end = events[-1][0] + 2.0
    i, n = 0, 0
    t = 0.0
    while t <= end:
        while i < len(events) and events[i][0] <= t:
            stream.feed(events[i][1])
            i += 1
        draw_frame(os.path.join(frames_dir, f"{n:05d}.png"))
        n += 1
        t += 1.0 / FPS
    palette = os.path.join(frames_dir, "palette.png")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(FPS),
                    "-i", os.path.join(frames_dir, "%05d.png"),
                    "-vf", "palettegen=stats_mode=diff", palette], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(FPS),
                    "-i", os.path.join(frames_dir, "%05d.png"), "-i", palette,
                    "-lavfi", "paletteuse=dither=none:diff_mode=rectangle",
                    "-loop", "0", OUT_GIF], check=True)
    keep = os.environ.get("KEEP_FRAMES")
    if keep:
        print("frames kept in", frames_dir)
    else:
        shutil.rmtree(frames_dir, ignore_errors=True)
    return n


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--driver":
        return driver(sys.argv[2])
    events = record()
    frames = render(events)
    size = os.path.getsize(OUT_GIF)
    print(f"wrote {OUT_GIF}: {frames} frames, {frames / FPS:.1f}s, {size / 1024:.0f} KB")


if __name__ == "__main__":
    main()

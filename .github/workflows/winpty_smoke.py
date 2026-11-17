"""Drive roulette.exe through a Windows pseudo-console (ConPTY, via pywinpty).

Same checks as pty_smoke.py: bet, spin, Enter to skip, stats, a typo, quit.

Usage: python winpty_smoke.py path\\to\\roulette.exe
"""
import re
import sys
import threading
import time

from winpty import PtyProcess

GAME = sys.argv[1]
PROMPT = "bet>"
ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b\][^\x07]*\x07")

proc = PtyProcess.spawn([GAME, "--no-color"], dimensions=(30, 100))
chunks = []


def reader():
    while True:
        try:
            data = proc.read(4096)
        except EOFError:
            return
        except Exception:  # noqa: BLE001
            return
        if data:
            chunks.append(data)


threading.Thread(target=reader, daemon=True).start()


def text():
    return ANSI.sub("", "".join(chunks))


def wait_for(marker, timeout, since):
    end = time.time() + timeout
    while time.time() < end:
        if marker in text()[since:]:
            return True
        time.sleep(0.1)
    return False


def send(keys, wait=PROMPT, timeout=40):
    since = len(text())
    proc.write(keys)
    return wait_for(wait, timeout, since)


wait_for(PROMPT, 40, 0)
send("red 10\r")
since = len(text())
proc.write("\r")              # spin…
time.sleep(0.5)
proc.write("\r")              # …and skip it
wait_for(PROMPT, 40, since)
send("stats\r")
send("spinn\r")
send("quit\r", wait="You leave the table")
time.sleep(1)

out = text()
print(out[-3000:])
checks = {
    "no crash": "Traceback" not in out,
    "spin settled": "PAYOUTS" in out,
    "stats shown": "S T A T S" in out,
    "typo suggestion": "did you mean" in out,
    "left the table": "You leave the table" in out,
}
for name, ok in checks.items():
    print(("PASS " if ok else "FAIL ") + name)
sys.exit(0 if all(checks.values()) else 1)

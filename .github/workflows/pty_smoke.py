"""Drive the interactive table through a real pseudo-terminal (Linux and macOS).

Places a bet, spins, presses Enter mid-spin to skip, checks stats, tries a
typo and quits, then fails if the session crashed or didn't get that far.
Each step waits for the `bet>` prompt rather than a fixed delay, because keys
typed during a spin are deliberately discarded.

Usage: python3 pty_smoke.py [path/to/roulette]
"""
import fcntl
import os
import pty
import select
import struct
import sys
import termios
import time

GAME = sys.argv[1] if len(sys.argv) > 1 else "./roulette"
PROMPT = b"bet> "

pid, fd = pty.fork()
if pid == 0:
    os.execvp(GAME, [GAME, "--no-color"])
fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", 30, 80, 0, 0))

output = b""


def read_until(marker, timeout, since):
    """Read until `marker` appears after offset `since`, or `timeout` passes."""
    global output
    end = time.time() + timeout
    while time.time() < end:
        if marker is not None and marker in output[since:]:
            return True
        ready, _, _ = select.select([fd], [], [], 0.1)
        if ready:
            try:
                chunk = os.read(fd, 65536)
            except OSError:
                return False
            if not chunk:
                return False
            output += chunk
    return marker is None


def send(keys, wait_for=PROMPT, timeout=30):
    since = len(output)
    os.write(fd, keys)
    return read_until(wait_for, timeout, since)


read_until(PROMPT, 30, 0)
send(b"red 10\n")
since = len(output)
os.write(fd, b"\n")                      # spin…
read_until(None, 0.5, since)
os.write(fd, b"\n")                      # …and skip it
read_until(PROMPT, 30, since)
send(b"stats\n")
send(b"spinn\n")
send(b"quit\n", wait_for=b"You leave the table")
read_until(None, 1, len(output))
os.waitpid(pid, 0)

text = output.decode("utf-8", "replace")
print(text[-3000:])
checks = {
    "no crash": "Traceback" not in text,
    "spin settled": "PAYOUTS" in text,
    "stats shown": "S T A T S" in text,
    "typo suggestion": "did you mean" in text,
    "left the table": "You leave the table" in text,
}
for name, ok in checks.items():
    print(("PASS " if ok else "FAIL ") + name)
sys.exit(0 if all(checks.values()) else 1)

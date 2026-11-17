"""Drive the interactive table through a real pseudo-terminal (Linux and macOS).

Places a bet, spins, presses Enter mid-spin to skip, checks stats and quits,
then fails if the session crashed or didn't get that far."""
import os
import pty
import select
import sys
import time

pid, fd = pty.fork()
if pid == 0:
    os.execvp("./roulette", ["./roulette", "--no-color"])

output = b""


def read_for(seconds):
    global output
    end = time.time() + seconds
    while time.time() < end:
        ready, _, _ = select.select([fd], [], [], 0.1)
        if ready:
            try:
                chunk = os.read(fd, 65536)
            except OSError:
                return
            if not chunk:
                return
            output += chunk


read_for(2)
for keys, wait in [(b"red 10\n", 1), (b"\n", 0.5), (b"\n", 8), (b"stats\n", 1),
                   (b"spinn\n", 1), (b"quit\n", 2)]:
    os.write(fd, keys)
    read_for(wait)
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

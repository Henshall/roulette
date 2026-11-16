# 🎰 roulette

A terminal roulette wheel of **harmless, read-only commands**. Type `roulette`,
watch a reel of shell commands scroll past a pointer, slow to a stop, and land
on one — which then runs.

Every command on the wheel is read-only and non-destructive
(listing files, showing the date, reporting disk usage, memory, processes, and
so on). A spin can never modify files, change system state, or send data over
the network, so it's always safe to play.

**Works on Linux and macOS** — the wheel is a shared portable set plus
platform-specific commands (`/proc`, `free`, `lscpu` on Linux; `sysctl`,
`vm_stat`, `sw_vers` on macOS) chosen automatically at runtime.

```
        🎰  R O U L E T T E  🎰
     every command is read-only — spin away!

   ╔════════════════════════════════════════╗
   ║   df -h | head -n 20                    ║
   ║   cal                                   ║
   ║ ▶  uptime -p                          ◀ ║
   ║   whoami                                ║
   ║   ls --color=always                     ║
   ╚════════════════════════════════════════╝

   🎯 Landed on: uptime -p
```

## Usage

```bash
roulette              # spin and run the winning command
roulette --dry-run    # spin, but don't run anything
roulette --list       # show every command on the wheel
roulette --fast       # skip the animation, just pick and run (alias: --pick)
roulette --help       # all options
```

| Option | Description |
| --- | --- |
| `-n`, `--dry-run` | Spin and pick, but do not execute |
| `-l`, `--list` | List every command and exit |
| `-p`, `--pick`, `-f`, `--fast` | Skip the animation, run the winner immediately |
| `--keep-wheel` | Keep the full wheel on screen after it lands (default: collapse it) |
| `--no-color` | Disable ANSI colors (also honors `NO_COLOR`) |
| `--timeout SECS` | Time the winning command may run (default 15) |
| `--seed N` | Reproducible spin |
| `--russian` | Add the "russian roulette" slot (see below) |
| `--bet CHIPS` | Wager chips on the spin (see Gamble below) |
| `--on TARGET` | Bet on `red`, `black`, `green`, or `jackpot` |
| `--beg` | Beg the house for chips (the only way to earn them back) |
| `--stats` | Show bankroll, win rate and streak |
| `--reset` | Reset the bankroll to 100 chips |
| `-V`, `--version` | Print version |

## 💀 Russian roulette (opt-in)

Pass `--russian` to add an extra slot to the wheel. If the spin lands on it,
**every file and folder in the current directory is deleted**:

```bash
roulette --russian
```

Guardrails, because random file deletion is no joke:

- **Opt-in only.** Without `--russian`, the wheel holds only read-only commands
  and can never delete anything — so you can't trigger it by accident.
- **Recoverable.** Everything is moved to the **trash** (`gio trash`, restorable
  from your file manager), not wiped with `rm`. If no desktop trash is
  available it falls back to `~/.local/share/roulette-trash/<timestamp>/`.
- **Confirmed.** When it lands on the skull it lists every item and makes you
  type `bang` before anything is deleted. It also refuses to delete when run
  non-interactively (e.g. in a pipe or script).

Preview the odds without risk: `roulette --russian --dry-run`.

## 🎲 Gamble (betting)

Every command on the wheel is also a **colored pocket**, so you can actually bet
on the spin. You start with **100 🪙 chips** (saved in `~/.roulette/state.json`):

```bash
roulette --bet 10 --on red       # even money
roulette --bet 10 --on black     # even money
roulette --bet 10 --on green     # land on a "loser" command — pays ~26×
roulette --bet 20 --on jackpot   # land on a marquee pocket — pays ~32×
roulette --stats                 # bankroll, win rate, best streak
roulette --reset                 # back to 100 chips
```

- **Colors:** roughly half the wheel is **red**, half **black**, and the 5
  losing commands are the **green** house pockets (like a `0`/`00`) — land on
  one and red/black bets bust while you watch the fake self-destruct. 😈
- **The command is the outcome:** the pocket you land on both runs *and* settles
  your bet — your prize is the command's output, your punishment is a loser.
- **Streaks:** every third win in a row adds a 🔥 bonus.

Betting is opt-in — plain `roulette` never touches your bankroll. Preview a bet
without spending chips: `roulette --bet 10 --on green --dry-run`.

**Lost everything?** `--reset` is a full wipe, but the *only* way to actually
earn chips back is to **beg**:

```bash
roulette --beg
```

Beg while **broke** and the house grudgingly spots you 100 🪙 — through **20
escalating levels of sass** as you keep coming back (it also tallies how many
times you've gone broke, for posterity). Beg with **money in hand** and you
just get mocked for it.

### ✨ Super spins

The wheel also has **5 "super spin" wildcard pockets** (shown in magenta). Land
on one and something special happens: it runs a high-entropy command, turns
that **output into red or black** (by the parity of the number it produces),
**lights up the wheel** with a flashing red/black reveal, and declares that
color the winner:

```
  ✨✨  S U P E R   S P I N  ✨✨
  🔢 the wheel conjures  948528637  →  948528637 is odd
  ████████████████████  (flashes red/black, settles on…)
    ◉   BLACK   WINS   ◉
  ✅ YOU WIN +10 🪙
```

If you have a bet down, a super spin settles it against that derived color
(red/black only — green and jackpot bets lose on a super). No two super spins
are ever the same.

## Install

Two ways: install the prebuilt **`.deb`**, or build **from source**. roulette is
a single Python 3 script with no third-party dependencies — just `python3` and
`bash`, which ship with every Linux distro.

### 1. Debian / Ubuntu package (`.deb`)

Download the `.deb` from the
[latest release](https://github.com/Henshall/roulette/releases/latest) and
install it — apt pulls in `python3`/`bash` automatically:

```bash
wget https://github.com/Henshall/roulette/releases/download/v1.0.0/roulette_1.0.0_all.deb
sudo apt install ./roulette_1.0.0_all.deb
```

Remove it with `sudo apt remove roulette`.

<details>
<summary>Build the <code>.deb</code> yourself</summary>

Only `dpkg-deb` is needed (already on every Debian system):

```bash
./build-deb.sh                       # produces dist/roulette_1.0.0_all.deb
sudo apt install ./dist/roulette_1.0.0_all.deb
```

Or with the full Debian toolchain:
`sudo apt-get install -y devscripts debhelper && make deb` (produces
`../roulette_1.0.0_all.deb`).
</details>

### 2. From source

Works on **Linux and macOS** (the `.deb` above is Debian/Ubuntu only):

```bash
git clone https://github.com/Henshall/roulette.git
cd roulette
sudo make install          # installs to /usr/local/bin/roulette (+ man page)
```

Prefer no sudo? Install into your home directory with
`make install PREFIX=~/.local` (then make sure `~/.local/bin` is on your `PATH`).
Or skip installing and just run it in place: `./roulette`.

Uninstall with `sudo make uninstall` (or `make uninstall PREFIX=~/.local`).

## How it works

`roulette` is a single, dependency-free Python 3 script (standard library only).
The winning command is executed with `bash -c`, which allows the wheel's
commands to use pipes and fallbacks (e.g. `lsb_release -a 2>/dev/null || cat
/etc/os-release`) and caps noisy output with `| head`. Commands that may be
missing on a minimal system degrade gracefully.

Run `make check` for a quick sanity test that never executes a random command.

## Releases

Tagged versions are published on the
[releases page](https://github.com/Henshall/roulette/releases) with a prebuilt
`.deb` attached (built with `./build-deb.sh`).

## License

MIT — see [LICENSE](LICENSE).

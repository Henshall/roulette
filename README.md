# 🎰 roulette

**The house has no edge. Your croupier, on the other hand, can be bribed.**

<p align="center">
  <img src="https://raw.githubusercontent.com/Henshall/roulette/main/demo/demo.gif" alt="A game of roulette in the terminal: tip the croupier, a near miss on 17, then a rigged straight-up win" width="748">
</p>

A real roulette table in your terminal: a single-zero wheel, the full betting
layout, and a payout rule that makes every bet worth **exactly zero** on
average. Start with 100 🪙 and try to break the bank at 1,000.

You can't beat a fair wheel. You *can* slip the croupier a few chips to rig
your losing spins, as long as the pit boss doesn't notice. Go broke and you can
[**beg**](#-broke) for more, twice. The third time, security walks you out.

```bash
pipx install roulette-game            # Linux or macOS, with Python 3
brew install henshall/tap/roulette    # macOS
```

On **Windows**, download [`roulette.exe`](https://github.com/Henshall/roulette/releases/latest/download/roulette.exe)
and double-click it. On Debian and Ubuntu you can also grab the
[`.deb`](#1-debian--ubuntu-package-deb). Then just type `roulette`.

## Play

```bash
roulette                         # sit down at the table (interactive)
roulette --bet 10 --on red       # one spin, one bet
roulette --bet 5 --on 17         # straight up on 17
roulette --spin                  # just watch the wheel spin, no bets
roulette --table                 # the layout and every payout
roulette --stats                 # bankroll, record, recent numbers
```

At the table, type a target and a chip count in either order — `red 10` or
`10 red`, `2 90` or `90 2` (there's no pocket 90, so that's 90 chips on 2) —
then press **Enter** to spin. When both readings are legal, like `5 17`, it
asks you to say `5 on 17` or `17 on 5`. Enter with no bets is a free spin
(just watch, no chips move); `rebet` puts your last bets back on the table.
`bets`, `undo`, `clear`, `tip`, `swap_table`, `pray`, `table`, `history`,
`stats`, `beg`, `help` and `quit` do what they say, and a typo like `spinn`
gets a "did you mean `spin`?".

Spins too slow? Press **Enter** during a spin to skip to the result, or type
`fast` for quicker spins (it's remembered between games; `fast` again turns
it off). The full command list shows on your first game; after that the table
just reminds you that `help` exists. Long lines wrap to fit your terminal, and
narrow terminals get a compact felt.

| Bet | Example | Pays |
| --- | --- | --- |
| Straight | `17` | 35:1 |
| Split | `17/18`, `17/20` | 17:1 |
| Street | `7-9` | 11:1 |
| Corner | `1/2/4/5` | 8:1 |
| Six line | `1-6` | 5:1 |
| Dozen / column | `d1` `d2` `d3`, `col1` `col2` `col3` | 2:1 |
| Even money | `red` `black` `odd` `even` `low` `high` | 1:1 |
| Zero | `0` (or `green`) | **36:1** |

## ⚖️ Zero edge: the 0 is a ✨ SUPER SPIN

On a casino wheel the 0 is how the house wins: every bet pays as if there were
36 pockets, but there are 37. Here, landing on **0** is never a dead loss:

- bets **on 0** pay **36:1** instead of 35:1, and
- **every other bet rides a SUPER SPIN** — the table lights up, the zero
  vanishes, and the wheel re-spins on 1–36 only to settle them.

So a bet on *k* of the numbers 1–36 wins with probability exactly *k*/36 at
the standard 36/*k* − 1 payout, and a bet on 0 wins 1/37 of the time at 36:1.
**Every bet has an expected value of exactly zero** — `--stats` shows your
realized return alongside it. (Streaks are tracked for bragging rights but pay
no bonus, which would tip the odds.)

## 🏦 Break the bank (how you win)

Every run starts with **100 🪙**. Reach **1,000 🪙** and you **break the bank**:
fireworks, a victory screen, and the win is recorded (`--stats` shows banks
broken and your fastest run). Then the house restocks and run #2 begins with
100 🪙 and a new croupier. Go broke and you can beg, but every beg goes on the
run's record.

On a fair table your chance of breaking the bank is exactly **10%** (100 ÷
1,000), *whatever* strategy you use. To do better, you need a friend on the
inside…

## 🎩 Your croupier (and accomplice)

Each run you're dealt a croupier from a roster of very fancy people — Gaston,
Céleste, Lorenzo, Valentina, Maximilian, Anastasia, Reginald, Penelope,
Thaddeus, Octavia, Dmitri, Séraphine, Astrid, Rodrigo and more (21 in all) — each with their own language to swear in. They
have opinions about your bets, your wins and (especially) your losses.

**They can also be bribed.** Croupiers remember who tipped *recently*. `tip 2`
at the table (or `roulette --tip 2`) buys luck, shown in your prompt as `🍀 +5%`:

- **Every chip you tip is `🍀 +2.5%` luck**, up to **+30%** (12 chips). Luck is the
  chance the croupier rigs a losing spin your way. When they do, the ball
  simply lands on your bet. No cut, no catch, except…
- **Luck fades a little every spin.** A tip loses a tenth of its strength per
  betting spin and is gone after 10: tip 4 and you'll see +10%, +9%, +8%… down
  to +0%. Free spins (no bet) don't count. What you see is exactly what you
  have; past +30% your tips are just gifts.
- **The pit boss is watching.** The bigger the rigged win, the likelier they
  spot it (1% per 3 🪙 won). Get caught and your bets are seized, your recent
  tips are wasted, and an **honest** croupier takes over. **Every bust doubles
  the pit boss's suspicion for the rest of the run** (×2, ×4, ×8…), whichever
  table you're at. They know your face now.
  Bribing your croupier while betting tiny amounts makes them nervous, and
  they'll tell you so: small bets mean long runs, and long runs mean busts.
- **Want someone else?** `swap_table` (or `roulette --swap-table`) moves you to
  another table with a different croupier. Your luck starts over at `🍀 +0%`.
  Right after a bust, the pit boss won't let you move for 5 spins.
- **Tip `0` and your luck goes down** — each zero tip is `🍀 -2.5%`. With negative
  luck, an offended croupier spoils that share of your *winning* spins ("Oops.
  My hand slipped."). It fades over 10 spins like any tip, or tip for real to
  make amends (1 🪙 cancels one zero tip).

How much it helps, measured over 10,000 simulated runs each (betting on red,
`swap_table` after each bust):

| How you tip | Chance to break the bank |
| --- | --- |
| Never | 10% |
| 1 🪙 every spin, betting 10s | ~5% (the tips cost more than the help) |
| **1 🪙 every spin, betting 25s** | **~30%** |
| 2 🪙 every spin, betting 25s | ~30% (the best we've found) |
| 3 🪙 every spin, betting 25s | ~22% |
| Keep +30%, betting 50s | ~30% |

Those odds are for a single bankroll. With the two bailouts begging allows,
your chance of winning a whole game is roughly 28% without tipping and about
50% if you tip steadily and bet 25s.

The wheel itself still has **no house edge**. You're the one cheating.

Other antics (all cosmetic):

- **Your croupier talks.** Straight-up on 17 is "romantic", red is "the beige
  cardigan of bets", and going all in makes them slide the tissues closer.
- **Martingale detector.** Double your bet after a loss a few times in a row
  and the croupier calls it out, with the pit boss bringing popcorn by double #4.
- **The ball misbehaves.** About once in 200 spins it escapes — into a martini,
  under table six, or toward the exit — before the croupier re-throws it.
- **Fireworks.** Hit a straight-up number (or break the bank) for a tiny ASCII
  show. 🎆
- **Near misses.** When the ball lands one pocket away from your number on the
  wheel, the croupier takes it personally. On your behalf. Mostly.
- **Pattern spotting.** Streaks of one colour, alternating colours and repeat
  numbers all get noticed, and so does betting that a colour is "due".
- **Meanwhile…** About once every 50 spins, something happens elsewhere in the
  casino. There are 20 of these, and you'll see every one before any repeats.
- **Leaving.** `quit` gets a send-off that depends on how your night went, and
  on whether your croupier misses your bribes.
- **Pray.** `pray` at the table (or `roulette --pray`) asks the roulette gods
  for help. They have opinions, not powers, and they know whether you've been
  tipping, whether you're broke, and whether you're one spin from glory. Pray
  too many times without betting and they put you on mute.

## 🙏 Broke?

Your bankroll (100 🪙 to start) lives in `~/.roulette/state.json` and is shared
by every mode. The only way to earn chips back is to **beg**:

```bash
roulette --beg
```

Beg while **broke** and the house grudgingly spots you 100 🪙, with a
sassier line the second time and a running count of your bailouts this run
(`stats` also tallies how many times you've gone broke across all runs). Beg
with **money in hand** and you just get mocked for it. `roulette --reset` wipes everything back to 100.

**Three strikes.** The house only bails you out **twice per run**. Beg a
**third** time and security throws you out of the casino (one of ten
different scenes, picked at random) — **game over**. The game then starts
over with a fresh run: 100 🪙, a new croupier, and a clean beg count. Your
lifetime stats are kept, including how many times you've been kicked out.
Begging while you still have chips is just mocked; it doesn't count.

## 🖥️ Command wheel (`--command` / `--russian`)

The original game is still here: a reel of **harmless, read-only shell
commands** scrolls past a pointer, slows to a stop, and the one it lands on
runs.

```bash
roulette --command               # spin and run the winning command
roulette --command --dry-run     # spin, but don't run anything
roulette --list                  # show every command on the wheel
roulette --russian               # command wheel + the russian slot (below)
```

Every command on that wheel is read-only and non-destructive (listing files,
showing the date, reporting disk usage, memory, processes, and so on). It works
on **Linux and macOS** — a shared portable set plus platform-specific commands
(`/proc`, `free`, `lscpu` on Linux; `sysctl`, `vm_stat`, `sw_vers` on macOS).

You can bet on it too — every command is a colored pocket:

```bash
roulette --command --bet 10 --on red       # even money
roulette --command --bet 10 --on green     # land on a "loser" command
roulette --command --bet 20 --on jackpot   # land on a marquee pocket
```

The green "loser" commands are the house pockets — but in keeping with the
zero-edge table, a red/black bet that lands on one isn't lost: you watch the
fake self-destruct, then get a **second-chance super spin**.

### ✨ Super spins

The command wheel also has **5 "super spin" wildcard pockets** (magenta). Land
on one and it runs a high-entropy command, turns that **output into red or
black** (by the parity of the number it produces), **lights up the wheel**, and
declares that color the winner, settling any red/black bet.

### 💀 Russian roulette (opt-in)

`roulette --russian` adds an extra slot to the command wheel. If the spin lands
on it, **every file and folder in the current directory is deleted**.

Guardrails, because random file deletion is no joke:

- **Opt-in only.** Without `--russian`, nothing can ever be deleted.
- **Recoverable.** Everything is moved to the **trash** (`gio trash`, restorable
  from your file manager), not wiped with `rm`. If no desktop trash is
  available it falls back to `~/.local/share/roulette-trash/<timestamp>/`.
- **Confirmed.** When it lands on the skull it lists every item and makes you
  type `bang` before anything is deleted. It also refuses to delete when run
  non-interactively (e.g. in a pipe or script).

Preview the odds without risk: `roulette --russian --dry-run`.

## All options

| Option | Description |
| --- | --- |
| `--spin` | Spin the real wheel once, just to watch (no bets, nothing saved) |
| `--command` | Spin the wheel of harmless commands instead of the table (`--commands` works too) |
| `--russian` | Command wheel plus the russian roulette slot |
| `--table` | Show the betting layout and payouts |
| `--bet CHIPS` | Wager on a single spin |
| `--on TARGET` | What to bet on (default `red`) |
| `-n`, `--dry-run` | Spin, but move no chips / run nothing |
| `-p`, `--pick`, `-f`, `--fast` | Skip the animations |
| `-l`, `--list` | List every command on the command wheel |
| `--keep-wheel` | Command mode: keep the reel on screen after it lands |
| `--timeout SECS` | Command mode: time the winning command may run (default 15) |
| `--tip CHIPS` | Tip the croupier — recent tips get losing spins rigged your way |
| `--swap-table` | Move to another table with a new croupier (luck resets to 0) |
| `--pray` | Pray to the roulette gods (no effect on the odds) |
| `--beg` / `--stats` / `--reset` | Bankroll management |
| `--seed N` | Reproducible spin |
| `--no-color` | Disable ANSI colors (also honors `NO_COLOR`) |
| `-V`, `--version` | Print version |

## Install

Five ways: the prebuilt **`.deb`** (Debian/Ubuntu), **pipx** (any Linux or
macOS), **Homebrew** (macOS), **`roulette.exe`** (Windows), or **from source**. roulette is a single Python 3 script (3.6 or newer)
with no third-party dependencies, just `python3` and `bash`, which ship with
every Linux distro and with Apple's Command Line Tools on macOS. Every change is
tested on Linux, macOS and Windows.

### 1. Debian / Ubuntu package (`.deb`)

Download the `.deb` from the
[latest release](https://github.com/Henshall/roulette/releases/latest) and
install it — apt pulls in `python3`/`bash` automatically:

```bash
wget https://github.com/Henshall/roulette/releases/download/v2.5.1/roulette_2.5.1_all.deb
sudo apt install ./roulette_2.5.1_all.deb
```

Remove it with `sudo apt remove roulette`.

<details>
<summary>Build the <code>.deb</code> yourself</summary>

Only `dpkg-deb` is needed (already on every Debian system):

```bash
./build-deb.sh                       # produces dist/roulette_2.5.1_all.deb
sudo apt install ./dist/roulette_2.5.1_all.deb
```

Or with the full Debian toolchain:
`sudo apt-get install -y devscripts debhelper && make deb` (produces
`../roulette_2.5.1_all.deb`).
</details>

### 2. Any Linux or macOS (pipx)

```bash
pipx install roulette-game
```

Installs the `roulette` command into its own environment. Upgrade with
`pipx upgrade roulette-game`, remove with `pipx uninstall roulette-game`.
(Plain `pip install --user roulette-game` works too.) The man page is
only included in the `.deb`, Homebrew and from-source installs.

### 3. macOS (Homebrew)

```bash
brew install henshall/tap/roulette
```

Upgrade with `brew upgrade roulette`, remove with `brew uninstall roulette`.
It runs on the `python3` that comes with Apple's Command Line Tools (Homebrew
already needs those). Without Homebrew, use the from-source install below.

### 4. Windows (`roulette.exe`)

Download [**roulette.exe**](https://github.com/Henshall/roulette/releases/latest/download/roulette.exe)
from the latest release and double-click it. Nothing else to install: Python
comes bundled inside. It looks best in **Windows Terminal** (the default on
Windows 11), and your bankroll is saved in `%USERPROFILE%\.roulette`.

The first time, Windows will probably say **"Windows protected your PC"**.
That's SmartScreen being wary of any app that isn't commercially code-signed;
click **More info → Run anyway**. Some antivirus tools also flag apps bundled
with PyInstaller by mistake. If you'd rather not run an `.exe` at all,
`pip install roulette-game` works on Windows too (with Python from python.org).

The command wheel (`--command`, `--russian`) runs `bash` commands, so it's
Linux and macOS only; on Windows it's available through
[WSL](https://learn.microsoft.com/windows/wsl/install).

### 5. From source

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
In command mode the winning command is executed with `bash -c`, which allows the wheel's
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

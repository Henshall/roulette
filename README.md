# 🎰 roulette

A **real roulette table** in your terminal — a single-zero (European) wheel,
the full betting layout, a persistent bankroll — with one twist:
**the house has no edge.** Lose it all and you can always
[**beg**](#-broke) the house for another 100 🪙 (it will judge you).

```
                                ▼
  ┌────────────────────────────────────────────────────────────┐
  │ 20  14  31  9   22  18  29  7   28  12  35  3   26  0   32 │
  └────────────────────────────────────────────────────────────┘
                                ▲
  🎯    7    RED · ODD · LOW · 1st 12 · col 1

  ━━ PAYOUTS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ RED                    10 🪙  1:1    →  +10
  ❌ 17                      5 🪙  35:1   →  -5
  net +5 🪙    →    balance 105 🪙
```

## Play

```bash
roulette                         # sit down at the table (interactive)
roulette --bet 10 --on red       # one spin, one bet
roulette --bet 5 --on 17         # straight up on 17
roulette --table                 # the layout and every payout
roulette --stats                 # bankroll, record, recent numbers
```

At the table, type a target and a chip count in either order — `red 10` or
`10 red`, `2 90` or `90 2` (there's no pocket 90, so that's 90 chips on 2) —
then press **Enter** to spin. When both readings are legal, like `5 17`, it
asks you to say `5 on 17` or `17 on 5`. Enter with no bets is a free spin
(just watch, no chips move); `rebet` puts your last bets back on the table. `bets`, `undo`, `clear`, `tip`,
`table`, `history`, `stats`, `beg`, `help` and `quit` do what they say.

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

## 🖥️ Command wheel (`--commands` / `--russian`)

The original game is still here: a reel of **harmless, read-only shell
commands** scrolls past a pointer, slows to a stop, and the one it lands on
runs.

```bash
roulette --commands              # spin and run the winning command
roulette --commands --dry-run    # spin, but don't run anything
roulette --list                  # show every command on the wheel
roulette --russian               # command wheel + the russian slot (below)
```

Every command on that wheel is read-only and non-destructive (listing files,
showing the date, reporting disk usage, memory, processes, and so on). It works
on **Linux and macOS** — a shared portable set plus platform-specific commands
(`/proc`, `free`, `lscpu` on Linux; `sysctl`, `vm_stat`, `sw_vers` on macOS).

You can bet on it too — every command is a colored pocket:

```bash
roulette --commands --bet 10 --on red       # even money
roulette --commands --bet 10 --on green     # land on a "loser" command
roulette --commands --bet 20 --on jackpot   # land on a marquee pocket
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
| `--commands` | Spin the wheel of harmless commands instead of the table |
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

Two ways: install the prebuilt **`.deb`**, or build **from source**. roulette is
a single Python 3 script with no third-party dependencies — just `python3` and
`bash`, which ship with every Linux distro.

### 1. Debian / Ubuntu package (`.deb`)

Download the `.deb` from the
[latest release](https://github.com/Henshall/roulette/releases/latest) and
install it — apt pulls in `python3`/`bash` automatically:

```bash
wget https://github.com/Henshall/roulette/releases/download/v2.3.0/roulette_2.3.0_all.deb
sudo apt install ./roulette_2.3.0_all.deb
```

Remove it with `sudo apt remove roulette`.

<details>
<summary>Build the <code>.deb</code> yourself</summary>

Only `dpkg-deb` is needed (already on every Debian system):

```bash
./build-deb.sh                       # produces dist/roulette_2.3.0_all.deb
sudo apt install ./dist/roulette_2.3.0_all.deb
```

Or with the full Debian toolchain:
`sudo apt-get install -y devscripts debhelper && make deb` (produces
`../roulette_2.3.0_all.deb`).
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

# 🎰 roulette

A terminal roulette wheel of **harmless, read-only commands**. Type `roulette`,
watch a reel of shell commands scroll past a pointer, slow to a stop, and land
on one — which then runs.

Every command on the wheel is read-only and non-destructive
(listing files, showing the date, reporting disk usage, memory, processes, and
so on). A spin can never modify files, change system state, or send data over
the network, so it's always safe to play.

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

## Install

### Debian / Ubuntu (`.deb`)

Build the package and install it:

```bash
sudo apt-get install -y devscripts debhelper
make deb
sudo apt-get install -y ../roulette_1.0.0_all.deb   # pulls in python3, bash
```

> `sudo apt-get install roulette` works once the `.deb` is published to an apt
> repository or a Launchpad PPA. The `debian/` directory here produces that
> package; see **Publishing** below.

### Snap

```bash
snapcraft                      # build roulette_1.0.0_amd64.snap
sudo snap install ./roulette_1.0.0_amd64.snap --dangerous --classic
```

Once published to the Snap Store:

```bash
sudo snap install roulette --classic
```

Classic confinement is used so the winning command can inspect the real system
(disks, processes, network) instead of a sandboxed view.

### From source (no packaging)

```bash
sudo make install          # installs to /usr/local/bin/roulette
# or just:
./roulette
```

Uninstall with `sudo make uninstall`.

## How it works

`roulette` is a single, dependency-free Python 3 script (standard library only).
The winning command is executed with `bash -c`, which allows the wheel's
commands to use pipes and fallbacks (e.g. `lsb_release -a 2>/dev/null || cat
/etc/os-release`) and caps noisy output with `| head`. Commands that may be
missing on a minimal system degrade gracefully.

Run `make check` for a quick sanity test that never executes a random command.

## Publishing

- **apt:** host the built `.deb` in an apt repository (e.g. a
  [Launchpad PPA](https://help.launchpad.net/Packaging/PPA)) so users can
  `sudo apt-get install roulette`.
- **snap:** `snapcraft upload --release=stable roulette_1.0.0_amd64.snap`.
  Classic-confinement snaps require a manual review request on the Snap Store.

## License

MIT — see [LICENSE](LICENSE).

#!/usr/bin/env bash
# Build an installable .deb using only dpkg-deb (no debhelper/devscripts needed).
# Output: dist/roulette_<version>_all.deb
set -euo pipefail
cd "$(dirname "$0")"

VERSION=$(sed -n 's/^__version__ = "\(.*\)"/\1/p' roulette)
[ -n "$VERSION" ] || { echo "could not read __version__ from ./roulette" >&2; exit 1; }
PKG="roulette_${VERSION}_all"

BUILD="$(mktemp -d)"
trap 'rm -rf "$BUILD"' EXIT
root="$BUILD/$PKG"

# File tree
install -D -m 0755 roulette "$root/usr/bin/roulette"
install -D -m 0644 man/roulette.1 "$root/usr/share/man/man1/roulette.1"
gzip -9 -n "$root/usr/share/man/man1/roulette.1"

# Control metadata
install -d "$root/DEBIAN"
cat > "$root/DEBIAN/control" <<EOF
Package: roulette
Version: $VERSION
Section: games
Priority: optional
Architecture: all
Depends: python3 (>= 3.6), bash
Recommends: util-linux, procps, coreutils
Maintainer: Roulette Maintainer <sourcecodeholdings@protonmail.com>
Description: terminal roulette wheel of harmless read-only commands
 roulette spins a reel of shell commands past a pointer, slows to a stop,
 and runs whichever command it lands on. Every command on the wheel is
 read-only and non-destructive (listing files, showing the date, reporting
 disk usage, and so on), so a spin can never harm your system.
EOF

mkdir -p dist
dpkg-deb --root-owner-group --build "$root" "dist/$PKG.deb" >/dev/null
echo "Built dist/$PKG.deb"

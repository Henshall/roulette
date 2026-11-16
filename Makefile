PREFIX ?= /usr/local
DESTDIR ?=
BINDIR  = $(DESTDIR)$(PREFIX)/bin
MANDIR  = $(DESTDIR)$(PREFIX)/share/man/man1

.PHONY: install uninstall deb check clean

install:
	install -d $(BINDIR)
	install -m 0755 roulette $(BINDIR)/roulette
	install -d $(MANDIR)
	install -m 0644 man/roulette.1 $(MANDIR)/roulette.1
	@echo "Installed roulette to $(BINDIR)/roulette"

uninstall:
	rm -f $(BINDIR)/roulette
	rm -f $(MANDIR)/roulette.1

# Build a .deb (requires devscripts/debhelper): produces ../roulette_*.deb
deb:
	dpkg-buildpackage -us -uc -b

# Quick sanity checks that don't execute a random command
check:
	python3 -c "import ast; ast.parse(open('roulette').read()); print('syntax OK')"
	./roulette --list >/dev/null && echo "list OK"
	./roulette --dry-run --pick >/dev/null && echo "dry-run OK"
	./roulette --table >/dev/null && echo "table OK"
	./roulette --commands --dry-run --pick >/dev/null && echo "commands dry-run OK"

clean:
	rm -rf debian/roulette debian/.debhelper debian/files debian/*.substvars debian/debhelper-build-stamp
	rm -rf dist *.deb ../roulette_*.deb

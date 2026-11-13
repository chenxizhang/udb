PREFIX ?= /usr/local
bindir ?= $(PREFIX)/bin
docdir ?= $(PREFIX)/share/doc/udb

.PHONY: all check install

all:

check:
	bash -n bin/udb
	PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v

install:
	install -D -m 0755 bin/udb "$(DESTDIR)$(bindir)/udb"
	install -D -m 0644 README.md "$(DESTDIR)$(docdir)/README.md"
	install -D -m 0644 LICENSE "$(DESTDIR)$(docdir)/LICENSE"

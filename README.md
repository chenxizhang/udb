# udb

**Ubuntu Development Bootstrap** -- an Ubuntu
development-environment initializer, usable on both standalone Ubuntu and WSL2.
This project is independent of Canonical and is not an official Ubuntu project.

## Status

The executable is [bin/udb](bin/udb), licensed under the [MIT License](LICENSE).
Maintainer: chenxizhang <ares@xizhang.com> (public maintenance contact).

Release packages are distributed through [GitHub Releases](https://github.com/chenxizhang/udb/releases).
This is not an Ubuntu archive package or an APT repository.
`apt install udb` without a local package file is not available.
No organization-specific tenant or internal tool installer is included.

Initial exact-name checks found no `udb` source or binary package in Ubuntu's
primary archive and no Debian package tracker page for `udb`. These are
preliminary checks, not a name reservation or trademark clearance.

## Running and installing

Supported targets are Ubuntu 22.04, 24.04, and 26.04 on amd64 or arm64, either
standalone with systemd or on WSL2. This is not a generic Linux initializer.

Download the Debian package and checksum list from the
[v0.1.0 release](https://github.com/chenxizhang/udb/releases/tag/v0.1.0):

```sh
curl -fLO https://github.com/chenxizhang/udb/releases/download/v0.1.0/udb_0.1.0-1_all.deb
curl -fLO https://github.com/chenxizhang/udb/releases/download/v0.1.0/SHA256SUMS
sha256sum --ignore-missing --check SHA256SUMS
sudo apt install ./udb_0.1.0-1_all.deb
udb --help
```

Installing the package does not initialize the host. Read the help, then run
`udb` separately as your ordinary user when ready.

Alternatively, clone and inspect the source:

```sh
git clone https://github.com/chenxizhang/udb.git
cd udb
./bin/udb --help
make check
```

Run `./bin/udb` as your ordinary user to initialize the machine. Do not run it
with `sudo` or `sh`. Default work mode skips WorkIQ unless `--tenant` is given;
`--personal` includes WorkIQ. Neither mode selects a tenant automatically.
`--tenant TENANT` explicitly scopes Azure login; otherwise it uses `az login`.

To install the command for later use:

```sh
sudo make install
udb --help
```

`make install` only copies the executable and documentation. It does not run
initialization, authentication, or remote installers. `PREFIX` defaults to
`/usr/local`; `DESTDIR` supports package staging without writing into the host:
`make install PREFIX=/usr DESTDIR=/path/to/staging`.

**Important side effects when initialization is explicitly run:** apt packages
are upgraded; Docker group membership grants root-equivalent access; WSL may
receive passwordless sudo; generated Copilot shortcuts use `--yolo`; selected
WorkIQ login accepts its EULA if not already recorded. Read `udb --help`.
These behaviors require archive-review consideration; an MIT license
does not make the entire setup policy suitable for every machine.

## Implementation

The entry point is explicitly Bash, not POSIX `sh`. Bash coordinates native
package managers, task results, timeouts, signals, and interactive CLI login.
Python 3 standard-library helpers handle structured JSON/configuration edits,
atomic replacement, restoration, and archive inspection. Small POSIX `sh`
blocks limit individual privileged operations; they are not an alternative
interpreter for the main program.

This division avoids fragile shell parsing of structured data. Rewriting the
orchestrator in Rust would still require the same external tools, privilege
boundaries, network checks, and interactive authentication, while adding a
compiled build/release toolchain. There is no identified CPU-bound workload
that calls for Rust here.

The standalone executable is self-contained. Python helpers use quoted
here-documents and positional arguments rather than interpolating shell values
into Python code. Releases include the executable, source package, Debian
package, and SHA-256 checksums.

## Building packages

The `debian/` directory uses debhelper compatibility level 13. Install the
declared build dependencies, then run `dpkg-buildpackage -us -uc` from a source
tree alongside its matching `udb_0.1.0.orig.tar.gz` upstream archive.
The release source package is unsigned for review; a sponsor must choose the
Ubuntu target release and sign an actual archive upload.

The release also contains a build-validation report. Package checks exercise
command/help behavior and installation/removal without running machine
initialization. They are not a claim that every external service and interactive
login has been tested on every supported Ubuntu version.

## Getting into the official Ubuntu archive

GitHub Releases, a personal APT repository, and a Launchpad PPA can distribute
packages, but none is the official Ubuntu archive. Installing from a PPA or a
personal APT repository requires adding that source first.

Ubuntu's documented process is:

1. Establish an upstream release with an explicit redistributable license,
   source, documentation, and a deliberate public maintenance contact.
2. Prefer Debian-first inclusion where appropriate. Check existing WNPP
   requests, file an Intent to Package if maintaining the package, prepare a
   policy-compliant source package, and seek a Debian sponsor if needed.
   Debian unstable packages are normally synced into the Ubuntu development
   release before the Debian Import Freeze.
3. If pursuing Ubuntu directly, first check existing requests. File a Launchpad
   bug against Ubuntu with the `needs-packaging` tag, the source location, and
   the actual license. Where applicable, link the Debian WNPP request.
   A request is not an accepted package.
4. Prepare and validate the source and binary packages, including Lintian and a
   clean-environment build. Request sponsorship in Launchpad, subscribing
   `ubuntu-sponsors` when the work is ready for review. A sponsor with upload
   rights must review and upload; a GitHub account does not confer those rights.
5. After upload, a new package enters the NEW queue for Archive Admin review.
   Approval, successful builds, and release/migration requirements still apply.

Normal new-package inclusion targets a development release. It does not make
the package immediately available on already released Ubuntu versions; those
need separate, approved distribution paths. Official archive inclusion also
does not automatically imply Canonical commercial support.

The [Ubuntu packaging request](https://bugs.launchpad.net/bugs/2174382) has been
filed, and `ubuntu-sponsors` is subscribed for review. The
[submission text](packaging/needs-packaging.txt) contains the public source,
license, maintenance contact, and review notes. Submission is not sponsor
approval or acceptance into the Ubuntu archive.

## Publication and package requirements

Before requesting archive review:

- Preserve required license notices for all included material.
- Use only the approved public maintenance contact. Archive metadata, bug
  reports, and signing-key identities can be publicly retained.
- Keep organization-specific defaults and internal installers out. Do not publish local
  logs, authentication state, shell histories, backups, or copied Git history.
- Review the initializer's side effects above with the sponsor. Decide whether
  third-party tools, EULA acceptance, and WSL privilege-policy changes must be
  separated or made additional explicit options for archive suitability.
- Install only the command and documentation from the Debian package. Never run
  machine initialization, login flows, remote installers, or system upgrades
  from package installation hooks. Initialization must be separately invoked by
  the ordinary user, with elevation requested only for the relevant operations.
- Preserve download verification, bounded probes, user-owned configuration,
  failure reporting, and idempotent reruns. Test without initializing a shared
  build host.

An open-source wrapper that installs proprietary tools is not automatically
eligible for Debian `main` or Ubuntu `universe`. The wrapper's own licensing,
purpose, external dependencies, and downloads need review. Debian explicitly
lists free wrappers for non-free programs as examples for `contrib`; Ubuntu has
different component names. Do not promise a component before sponsor/archive
review.

## Authoritative references

- [Ubuntu: new packages](https://ubuntu.com/project/docs/how-ubuntu-is-made/processes/new-packages/)
- [Ubuntu: sponsorship](https://ubuntu.com/project/docs/how-ubuntu-is-made/processes/sponsorship/)
- [Ubuntu: finding a sponsor](https://ubuntu.com/project/docs/contributors/uploading/find-a-sponsor/)
- [Ubuntu: creating a package](https://ubuntu.com/project/docs/contributors/new-package/create-a-new-package/)
- [Debian: WNPP](https://www.debian.org/devel/wnpp/)
- [Debian Policy: archive areas and copyright](https://www.debian.org/doc/debian-policy/ch-archive.html)
- [Debian Policy: control fields, including Maintainer](https://www.debian.org/doc/debian-policy/ch-controlfields.html)

Some official tutorials retain historical tool/version examples. Follow their
current process requirements, but use the actual target development release and
current packaging tools rather than copying old release names.

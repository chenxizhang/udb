# udb

**Ubuntu Development Bootstrap** -- a proposed short name for an Ubuntu
development-environment initializer, usable on both standalone Ubuntu and WSL2.
This project is independent of Canonical and is not an official Ubuntu project.

## Status

This repository currently contains documentation and a packaging-request draft
only. It does **not** contain an executable, a released Debian package, or an APT
repository. No Ubuntu or Debian inclusion request has been submitted.
`apt install udb` is a future goal, not an available installation command.

The existing personal initializer remains unchanged. Its source has not been
copied here: a public Gist is not, by itself, an open-source license.
An explicit license from the copyright holder is required before publishing
that source as this project or distributing packages.

Initial exact-name checks found no `udb` source or binary package in Ubuntu's
primary archive and no Debian package tracker page for `udb`. These are
preliminary checks, not a name reservation or trademark clearance.

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

The unsubmitted [request template](packaging/needs-packaging.txt) deliberately
contains placeholders. Do not file it as a completed request.

## Publication and package requirements

Before any source release or submission:

- Confirm the copyright holder's choice of license and preserve required notices
  for all included material. Do not invent a license for the existing script.
- Choose a reachable, explicitly approved public maintainer contact. Archive
  metadata, bug reports, and signing-key identities can be publicly retained.
  Do not extract private contact information from local Git configuration.
- Remove organization-specific tenants, internal installer references, and
  account assumptions from the general-purpose version. Do not publish local
  logs, authentication state, shell histories, backups, or copied Git history.
- Make third-party proprietary tools and authentication explicit choices.
  Do not silently accept EULAs or weaken sudo policy for general users.
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

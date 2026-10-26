# Runtime databases are not source artifacts

This PR removes only tracked SQLite snapshots from its proposed source tree.
It does not read the database contents, change a hosted database, deploy code,
remove earlier commits or rewrite Git history. The old blobs remain recoverable
from the parent commit. Main and prior history still expose the old snapshots
until separately reviewed cleanup and release decisions are made.

The snapshots' presence is not evidence that they contain real or sensitive
records; no such claim is made. Treat them as potentially confidential until
the data owner completes a private review. Do not post their contents, accounts,
password hashes or export files into an issue, PR, CI log or chat.

The regression scans tracked filenames, without opening database files. Existing
Django CI creates schema, users and records from migrations in a disposable
in-memory SQLite database. Application migrations/schema code are preserved.
SQLite files and their journal/WAL/SHM sidecars are ignored so a local run will
not accidentally reintroduce them to version control.

Before any eventual approved deployment, identify whether that deployment uses
a persistent SQLite path in the checkout. Take and verify a private backup,
move runtime data to storage outside the disposable source tree and configure
that path explicitly. Do not deploy this deletion into a checkout containing the
only working copy of a database. For a configured external PostgreSQL database,
this PR neither connects to it nor migrates it.

If a private owner review confirms exposed sensitive data, follow a separate
incident plan: preserve a protected recovery copy, decide whether credential
revocation is required, coordinate all branches/forks/clones and open PRs, and
only then consider a reviewed history rewrite and host-cache purge. Deleting a
file in a new commit does not erase it from Git history or downstream copies.

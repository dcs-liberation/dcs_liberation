Pull requests should be made against the `develop` branch. Any backports
necessary will be handled by the development team.

Pull requests should be focused on one task. Multiple bug fixes should be
multiple PRs. We cannot merge half a PR, and combined PRs are much more
difficult to review. PRs that do not adhere to this will have their review
delayed.

Prefer rebase to merge, and squash commits as needed to preserve a readable
commit history. This project maintains linear history in the develop branch, so
we will either rebase or squash your PR when merging. It is much easier for us
if your branch already has a readable commit history (ensure that your commit
subject lines are clear enough to identify the patch in the git log). An
exception to this is made for large PRs that are likely to require multiple
rounds of review; in that case it's easier if you **don't** do this (GitHub
does not preserve the history of old commits, so we cannot filter a PR for only
new changes if a branch is force pushed) and we will squash it when merging.

New features and bug fixes are usually worth mentioning in the changelog.
Exceptions are fixes for bugs that never shipped (were only present in a canary
build), and changes with no intended user observable behavior, such as a
refactor. If you're comfortable writing the note yourself, add it to
`changelog.md` in the root of the project in the section for the upcoming
release.

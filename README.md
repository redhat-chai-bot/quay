# PR7812 UI comparison fixtures

These screenshots are synthetic component fixtures for the Robot API tokens UI.
They use no backend and no real credentials, identities, or token secrets.

- `screenshots/pr7812/before-readonly.png` — source base `ada8067ee43cbb2750f68f83170c4ef1b281d087`.
- `screenshots/pr7812/after-readonly.png` — source head `ee70ee29efea23d8ba3fe176ba1397871ef9a9ba` for a read-only viewer.
- `screenshots/pr7812/after-manager.png` — source head `ee70ee29efea23d8ba3fe176ba1397871ef9a9ba` for an authorized manager.

The read-only comparison preserves the token table, search, and pagination while
removing mutation controls. The manager fixture retains those controls.

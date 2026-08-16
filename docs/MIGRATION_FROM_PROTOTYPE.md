# Migration from the original prototype

The original repository is intentionally replaced rather than incrementally patched.

## Why

The prototype contained:

- a committed `venv/`
- committed `__pycache__/`
- placeholder District Courts scraping
- placeholder CAPTCHA output
- placeholder API endpoints
- `assert True` tests
- an S3 ZIP path with a missing `io` import
- a corrupted README tail
- an outdated eCourts target URL

Those issues make it unsuitable as a public research tool without a clean rebuild.

## Recommended Git history cleanup

Because the committed virtual environment made the old repository very large, simply deleting `venv/` in a new commit will not remove it from history.

For a small early-stage repository with no downstream users, the cleanest option is to replace the reachable history with the rebuilt source tree.

See the push instructions provided with the release package.

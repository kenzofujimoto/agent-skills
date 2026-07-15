# Release Process

1. Update the skill and repository changelogs.
2. Confirm the manifest version and skill metadata agree.
3. Run `python -m pytest` and `python scripts/validate_repo.py`.
4. Run the platform package script.
5. Inspect the ZIP contents and verify its SHA-256 digest.
6. Commit with a conventional commit message and push `main`.
7. Create an immutable version tag and GitHub Release.
8. Attach the ZIP and `.sha256` file, then verify the published assets.

Never rebuild an existing release under the same version. Publish a new patch version instead.

# Contributing

Contributions should be focused, portable, and safe to publish.

1. Create a branch such as `feature/my-skill` or `fix/validator-paths`.
2. Create or update a skill following `docs/adding-a-skill.md`.
3. Add tests before changing script behavior.
4. Run `python -m pytest` and `python scripts/validate_repo.py`.
5. Package the affected skill and inspect the archive.
6. Confirm that no credential, private asset, downloaded model, or browser profile is present.
7. Open a draft pull request using a conventional commit title.

By contributing original work, you agree to license it under the repository's MIT License. Do not submit content you do not have permission to distribute.

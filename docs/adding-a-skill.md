# Adding a Skill

1. Run `scripts/new-skill.ps1 -Name my-new-skill` or `scripts/new-skill.sh my-new-skill`.
2. Edit `SKILL.md` so its instructions are actionable, scoped, and portable.
3. Add only necessary scripts, references, recipes, and templates. Do not add downloaded assets.
4. Update the version in `skills.json` and the skill changelog.
5. Run `python scripts/validate_repo.py` and the full test suite.
6. Install locally with the platform installer and exercise the workflow.
7. Package the skill and inspect both the ZIP and SHA-256 file.
8. Create a focused branch and open a draft pull request.
9. After merge, follow `release-process.md` to create a tagged release.

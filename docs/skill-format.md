# Skill Format

Each skill lives at `skills/<slug>/`. The slug uses lowercase ASCII letters, digits, and single hyphens.

Required files:

- `SKILL.md` with YAML frontmatter containing `name` and `description`;
- `README.md` for human-oriented documentation;
- `CHANGELOG.md` following Keep a Changelog.

Optional directories are `references/`, `recipes/`, `scripts/`, and `templates/`. References must use portable relative paths. Executable helpers must validate inputs, report errors, and avoid implicit network or destructive actions.

The canonical version is stored in `skills.json`; released skills should also expose a matching `VERSION` file when their runtime uses one.

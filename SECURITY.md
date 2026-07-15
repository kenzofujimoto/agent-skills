# Security Policy

Never publish OAuth tokens, access tokens, browser profiles, cookies, `.env` files, private assets, session data, or credentials in examples. Use environment-variable names and placeholder values only.

Run `python scripts/validate_repo.py` before committing. The validator detects common secret patterns and forbidden files, but it does not replace manual review.

To report a vulnerability, use GitHub's private vulnerability reporting channel when it is available. Otherwise contact the repository owner privately without including secrets in a public issue. Supported releases are the latest release and the current `main` branch.


# Sofware-AI Agent Starter

This repository provides a local agent for price-finding tasks using the `browser-use` library. All operations run locally—no cloud features or remote execution.

## Quickstart
1. Copy `.env.example` to `.env` and add your `OPENAI_API_KEY`.
2. Create a Python virtual environment and install dependencies:
	```bash
	python -m venv .venv
	.venv\Scripts\activate  # On Windows
	pip install -r requirements.txt
	```
3. Install Chromium for Playwright:
	```bash
	python -m playwright install chromium
	```
4. Run the agent:
	```bash
	./scripts/run_local.sh
	```

## Security & Legal Notice
- Cloud features and stealth automation are intentionally disabled.
- Do **not** automate purchases or logins without human supervision.
- Always review the Terms of Service and robots.txt of target websites before scraping.

## Next Steps & Improvements
- Replace free-text extraction with site-specific selector-based parsing.
- Add rate limiting, retries, and backoff strategies.
- Run the agent under a restricted user account for safety.
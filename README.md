# Sofware-AI Agent Starter


Local starter repo: Use browser-use locally (no cloud) to implement a simple price finder agent.


## Quickstart
1. Copy `.env.example` to `.env` and اضافه کن `OPENAI_API_KEY`.
2. create venv, install requirements.
3. python -m playwright install chromium
4. ./scripts/run_local.sh


## Security & Legal
- This repo intentionally avoids `use_cloud` and cloud stealth features.
- Do NOT run automated purchasing or login actions without human review.
- Check each target site's Terms of Service and robots.txt.


## Next steps
- Replace free-text extraction with selector-based parsing per-site.
- Add rate-limiting and retry/backoff.
- Run agent under a limited user account.
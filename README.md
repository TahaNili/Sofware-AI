
# Sofware-AI Agent Starter

Lightweight local starter repository for a price-finding agent built on top of `browser-use` and Playwright. The agent is designed to run entirely locally and demonstrates a simple pipeline: plan a search with an LLM, run a browser-based agent, and save results to CSV.

Table of contents
- Quickstart (Windows / macOS / Linux)
- Project structure and key files
- Usage
- Known issues & safety notes
- Troubleshooting & next steps

## Quickstart
Follow the platform-appropriate steps below. The repository expects a Python 3.10+ environment.

Windows (PowerShell)
```powershell
copy .env.example .env
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install chromium
# Then run the local starter script
./scripts/run_local.sh
```

macOS / Linux (bash)
```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install chromium
./scripts/run_local.sh
```

Note: `.env.example` in this repo is currently empty; add your `OPENAI_API_KEY` there as `OPENAI_API_KEY=<your-key>` (or set it in your environment) before running.

## Project structure and key files
- `agent/main.py` — CLI entrypoint. Prompts for an item name, calls the planner to get a list of steps, instantiates `LocalExecutor`, and runs the extraction.
- `agent/planner.py` — Uses the OpenAI client to ask an LLM for a short JSON array of search steps. Returns the parsed list or an empty list on error.
- `agent/executor.py` — Creates a `browser_use.Agent` configured with `ChatBrowserUse` and a Playwright `BrowserSession`. Runs the agent and writes the raw output to a timestamped CSV file.
- `utils/logger.py` — Simple logging configuration used by the project.
- `scripts/run_local.sh` — Convenience script that creates a venv, installs requirements, installs Playwright browsers, loads `.env`, and runs `agent/main.py`.
- `requirements.txt` — Python dependencies (includes `browser-use`, `playwright`, `openai`, `python-dotenv`, `pandas`, and a `chromium` marker).

## Usage
1. Set `OPENAI_API_KEY` in `.env` or your environment.
2. Run the script and follow prompts to enter an item name to search for.
3. The agent will plan steps, run a browser agent, and save the raw output to `results_<timestamp>.csv`.

Example (interactive):
- Enter item: `wireless mouse`
- Planned steps printed to console
- Agent runs and `results_*.csv` is created with a `raw_output` column

## Known issues & notes
- CSV writing bug: The current `agent/executor.py` opens the file with a `with` context and writes the header inside it, but the call that writes the agent output (`writer.writerow([out])`) is placed after the `with` block and therefore attempts to write to a closed file. This will raise a `ValueError`. Fixing this requires moving the second write inside the `with` block. I can patch this for you if you'd like.
- `planner.py` initializes an OpenAI client using an environment variable key. The code currently calls `os.getenv('sk-...')` with an actual key string argument; you should replace that with the environment variable name (for example `os.getenv('OPENAI_API_KEY')`) and keep your real key out of source.
- `agent/executor.py` previously contained an inner function defined inside `__init__` (older version). The repo currently exposes `run_search_and_extract` as a proper method (correct). If you see nested function definitions elsewhere, consider promoting them to methods.

## Troubleshooting
- If Playwright fails to install browsers, run `python -m playwright install chromium --with-deps` and check your network/firewall settings.
- If LLM responses are not valid JSON, `planner.py` will return an empty list. Try running `agent/planner.py` interactively to inspect the raw LLM output.

## Next steps (recommended)
- Replace free-text extraction with selector-based parsing for each target site to improve reliability.
- Add rate-limiting and retry/backoff to avoid triggering anti-bot protections.
- Add unit tests for `planner.py` (mocking the OpenAI response) and for `executor.py` (mocking the Agent) to catch regressions.
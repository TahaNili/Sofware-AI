Add initial Windows AI assistant structure with GUI, planner, and executor

This commit adds the initial scaffold for the "Sofware-AI" project and includes the following key components:

- UI: `ui/main_window.py`
  - Main PySide6-based GUI with a chat area, user input, send button and a status/progress bar.
  - Uses a worker thread (QThread) for running blocking or long-running agent operations.
  - Sets a Persian-friendly font (Vazir) and includes a startup welcome message.

- Agent core: `agent/`
  - `planner.py`: Asynchronously calls the OpenAI API (AsyncOpenAI) to analyze user prompts and returns an action plan as a JSON-like dict.
  - `executor.py`: WebExecutor scaffold for performing web/product searches (currently returns a sample result for testing).
  - `agent/main.py`: A simple interactive CLI entry that demonstrates the request → plan → execute flow.

- Windows integration: `agent/windows/system.py`
  - `WindowsController` utilities to run programs, list running apps (psutil), read basic system info and change settings (e.g., wallpaper) using pywin32.

- Misc:
  - `utils/logger.py`: basic logger configuration.
  - `README.md` and `requirements.txt` updated with project description and dependencies.

Technical notes and limitations:
- `planner.py` requires `OPENAI_API_KEY` to be set in environment variables (or .env) to call OpenAI.
- `executor.py` currently contains a stub and needs a real web-scraping/search implementation.
- Some platform-specific operations (win32 APIs) may need additional error handling and permission checks.
- Linting/tests are not included in this commit; please run test/lint steps before release.

Next steps/optional improvements:
- Implement actual web search logic in `executor.py` and add unit/integration tests.
- Add automated linting and CI configuration.
- Improve error handling and input validation for Windows integration methods.

Created and committed `COMMIT_MESSAGE.md` to document this commit message in the repository.
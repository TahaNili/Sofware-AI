
"""Project entrypoint: choose GUI (PySide6) or CLI fallback.

This launcher loads environment variables (if python-dotenv is available),
initializes the AI factory and either starts the Qt GUI or the console CLI
based on availability and command-line flags.

It prefers GUI when PySide6 is installed and the user hasn't requested CLI.
If GUI fails to start, it falls back to the CLI mode.
"""

import os
import sys
import argparse
import asyncio
from typing import Optional

from utils.logger import logger
from agent.ai.factory import AIFactory


def load_dotenv_if_present() -> None:
	try:
		from dotenv import load_dotenv
		load_dotenv()
		logger.info("Loaded .env file (if present)")
	except Exception:
		logger.debug("python-dotenv not available or .env missing; skipping load")


async def run_cli() -> int:
	"""Run the console-based CLI (agent.cli.main). Returns exit code."""
	try:
		# agent.cli exposes an async main() function
		import agent.cli as cli_mod
		if hasattr(cli_mod, "main"):
			return await cli_mod.main()

		# As a fallback, execute as a module subprocess
		proc = await asyncio.create_subprocess_exec(sys.executable, "-m", "agent.cli")
		await proc.wait()
		return proc.returncode or 0
	except Exception as e:
		logger.exception("Failed to run CLI mode: %s", e)
		return 1


def run_gui(argv: Optional[list] = None) -> int:
	"""Run the PySide6 GUI. Raises if PySide6 is not installed or GUI init fails."""
	argv = argv if argv is not None else sys.argv
	try:
		from PySide6.QtWidgets import QApplication
	except Exception as e:
		logger.debug("PySide6 not available: %s", e)
		raise

	try:
		from ui.main_window import MainWindow
	except Exception as e:
		logger.exception("Failed to import UI components: %s", e)
		raise

	app = QApplication(argv)
	factory = AIFactory()
	window = MainWindow(factory)
	window.show()
	# Return the Qt application exit code
	return app.exec()


def parse_args(argv: Optional[list] = None) -> argparse.Namespace:
	p = argparse.ArgumentParser(prog="Sofware-AI", description="Sofware-AI launcher")
	p.add_argument("--cli", action="store_true", help="Run in console CLI mode")
	p.add_argument("--no-gui", action="store_true", help="Do not attempt to start GUI")
	p.add_argument("--debug", action="store_true", help="Enable debug logging")
	return p.parse_args(argv)


def main(argv: Optional[list] = None) -> int:
	argv = argv if argv is not None else sys.argv[1:]
	args = parse_args(argv)

	if args.debug:
		logger.setLevel("DEBUG")

	load_dotenv_if_present()

	# If user explicitly requested CLI, run it
	if args.cli or args.no_gui:
		logger.info("Starting in CLI mode")
		return asyncio.run(run_cli())

	# Prefer GUI when available, otherwise fall back to CLI
	try:
		logger.info("Attempting to start GUI mode")
		return run_gui([sys.argv[0]] + list(argv))
	except Exception as e:
		logger.warning("GUI unavailable or failed to start (%s). Falling back to CLI.", e)
		return asyncio.run(run_cli())


if __name__ == "__main__":
	try:
		exit_code = main()
	except Exception as e:
		logger.exception("Unhandled error in launcher: %s", e)
		exit_code = 1
	sys.exit(exit_code)

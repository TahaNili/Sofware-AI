"""
Simple wrapper to run browser-use (or other commands) inside an isolated virtualenv.

Usage pattern:
- Create virtualenv (see README update) and install packages from requirements-browser.txt
- Call run_in_venv([...]) to execute a command using that venv's python

This wrapper intentionally keeps runtime invocation simple and returns stdout/stderr.
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path
from typing import Tuple, List, Optional

DEFAULT_VENV = Path('.venv-browser')


def _python_executable(venv_path: Path) -> Optional[Path]:
    """Return the python executable path for the venv (Windows & Unix) if present."""
    if not venv_path.exists():
        return None
    # Windows
    candidate = venv_path / 'Scripts' / 'python.exe'
    if candidate.exists():
        return candidate
    # Unix
    candidate = venv_path / 'bin' / 'python'
    if candidate.exists():
        return candidate
    return None


def run_in_venv(args: List[str], venv_path: str | Path = DEFAULT_VENV, timeout: int = 300) -> Tuple[int, str, str]:
    """Run a command using the virtualenv's python. Returns (returncode, stdout, stderr).

    Example:
        run_in_venv(['-m', 'browser_use', 'some', 'args'])

    Notes:
    - Caller should ensure the venv exists and packages are installed.
    - This wrapper allows keeping browser-use and its openai pin isolated from the main env.
    """
    venv = Path(venv_path)
    python = _python_executable(venv)
    if python is None:
        raise FileNotFoundError(f"Python executable not found in venv '{venv}'")

    cmd = [str(python)] + args
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as e:
        return -1, '', f'Timeout after {timeout}s: {e}'


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Run a command inside .venv-browser')
    parser.add_argument('cmd', nargs='+', help='Command to run (example: -m browser_use arg1 arg2)')
    parser.add_argument('--venv', default=str(DEFAULT_VENV), help='Path to virtualenv')
    args = parser.parse_args()

    try:
        rc, out, err = run_in_venv(args.cmd, args.venv)
        print(out)
        if err:
            print(err, file=sys.stderr)
        raise SystemExit(rc)
    except Exception as e:
        print(str(e))
        raise SystemExit(2)

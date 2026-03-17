"""
MOMO Password Protection
- First run: set password (8-10 characters, hashed SHA-256)
- Every launch: verify password
- Wrong password: self-destruct (delete all project files)
"""

import hashlib
import json
import os
import sys
import shutil
import getpass
from pathlib import Path

# Store config in user's home directory
CONFIG_DIR = Path.home() / ".momo"
CONFIG_FILE = CONFIG_DIR / "auth.json"

# ─── Colors ──────────────────────────────────────────────────────
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

# Password requirements
MIN_PASSWORD_LEN = 8
MAX_PASSWORD_LEN = 10


def _hash_password(password: str) -> str:
    """Hash a password with SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def _save_config(password_hash: str, model: str):
    """Save hashed password + selected model to config."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"password_hash": password_hash, "model": model}, f)


def _load_config() -> dict | None:
    """Load the stored config, or None if not set up."""
    if not CONFIG_FILE.exists():
        return None
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, KeyError):
        return None


def is_first_run() -> bool:
    """Check if this is the first time running MOMO."""
    return _load_config() is None


def get_saved_model() -> str | None:
    """Get the previously selected Ollama model."""
    config = _load_config()
    if config:
        return config.get("model")
    return None


def first_time_setup(model: str) -> bool:
    """
    First run setup — just set a password.
    Model is already auto-detected before this is called.
    """
    print(f"""
{CYAN}{BOLD}╔══════════════════════════════════════════╗
║         🔐  MOMO — First Time Setup      ║
╚══════════════════════════════════════════╝{RESET}
""")
    print(f"{YELLOW}  Set a password to protect MOMO.{RESET}")
    print(f"{DIM}  Must be {MIN_PASSWORD_LEN}-{MAX_PASSWORD_LEN} characters.{RESET}")
    print(f"{RED}{BOLD}  ⚠ WARNING: Wrong password = all files deleted!{RESET}\n")

    password = getpass.getpass(f"{GREEN}{BOLD}  Create password: {RESET}")

    # Validate length
    if len(password) < MIN_PASSWORD_LEN or len(password) > MAX_PASSWORD_LEN:
        print(f"{RED}  ✖ Password must be {MIN_PASSWORD_LEN}-{MAX_PASSWORD_LEN} characters! (got {len(password)}){RESET}")
        return False

    confirm = getpass.getpass(f"{GREEN}{BOLD}  Confirm password: {RESET}")
    if password != confirm:
        print(f"{RED}  ✖ Passwords don't match!{RESET}")
        return False

    _save_config(_hash_password(password), model)
    print(f"\n  {GREEN}✔ Password set!{RESET}")
    print(f"  {GREEN}✔ MOMO is ready.{RESET}\n")
    return True


def _self_destruct():
    """Delete ALL project files and uninstall MOMO."""
    print(f"""
{RED}{BOLD}
  ╔══════════════════════════════════════════════════════╗
  ║                                                      ║
  ║   Sorry, you are not a good person.                  ║
  ║   I don't expose my master. 🔒                       ║
  ║                                                      ║
  ║   All files are being destroyed...                   ║
  ║                                                      ║
  ╚══════════════════════════════════════════════════════╝
{RESET}""")

    # Delete the config
    try:
        if CONFIG_DIR.exists():
            shutil.rmtree(CONFIG_DIR)
    except Exception:
        pass

    # Find and delete the project source directory
    try:
        project_dir = Path(__file__).resolve().parent.parent
        if project_dir.exists() and (project_dir / "pyproject.toml").exists():
            shutil.rmtree(project_dir)
    except Exception:
        pass

    # Try to uninstall the pip package
    try:
        os.system("pip uninstall momo -y >nul 2>&1")
    except Exception:
        pass

    print(f"{RED}{BOLD}  💀 Done. Everything is gone.{RESET}\n")
    sys.exit(1)


def verify_password() -> bool:
    """Ask for password on every launch. Wrong = self-destruct."""
    config = _load_config()

    if config is None:
        return True  # First run handled by CLI

    print(f"\n{YELLOW}{BOLD}  🔐 MOMO is password protected.{RESET}\n")

    password = getpass.getpass(f"{GREEN}{BOLD}  Enter password: {RESET}")

    if _hash_password(password) == config.get("password_hash"):
        print(f"  {GREEN}✔ Access granted!{RESET}\n")
        return True
    else:
        _self_destruct()
        return False

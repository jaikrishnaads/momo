"""
MOMO CLI — Terminal entry point.
Type `momo` and everything just works.

Flow:
  1. Auto-start Ollama server (no manual `ollama serve` needed)
  2. First run:  Set password (8-10 chars) → auto-detect model → chat
  3. Next runs:  Enter password → auto-detect model → chat
  4. On exit:    All chat history destroyed (ephemeral)
"""

import sys
import time
import subprocess
from momo.engine import chat, check_ollama, list_ollama_models
from momo.auth import verify_password, is_first_run, first_time_setup, get_saved_model

# ─── Colors ──────────────────────────────────────────────────────
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def banner(model: str):
    print(f"""
{CYAN}{BOLD}╔══════════════════════════════════════════╗
║          🤖  MOMO AI  Chatbot            ║
║      Terminal Edition • {model:<17s}║
╚══════════════════════════════════════════╝{RESET}
{DIM}  • Type your question and press Enter
  • Type 'exit' or 'quit' to leave
  • Type 'clear' to reset conversation
  • Chat is ephemeral — nothing is saved{RESET}
""")


def _start_ollama():
    """Auto-start Ollama server in background if not already running."""
    if check_ollama():
        print(f"  {GREEN}✔ Ollama server already running{RESET}")
        return True

    print(f"  {DIM}Starting Ollama server...{RESET}", end="\r")
    try:
        # Start ollama serve in background (hidden, detached)
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW
            if sys.platform == "win32" else 0,
        )

        # Wait for it to come up (max 15 seconds)
        for i in range(15):
            time.sleep(1)
            if check_ollama():
                print(f"  {GREEN}✔ Ollama server started!{RESET}              ")
                return True

        print(f"  {RED}✖ Ollama server didn't start in time{RESET}")
        return False

    except FileNotFoundError:
        print(f"""
{RED}{BOLD}  ✖ Ollama is not installed!{RESET}

{YELLOW}  Install Ollama first:{RESET}
    → https://ollama.com/download

{YELLOW}  Then pull a model:{RESET}
    → ollama pull gemma2:2b

{YELLOW}  Then just run:{RESET}
    → momo
""")
        return False


def _get_model() -> str | None:
    """Get the best available model — saved model or auto-detect."""
    # Try saved model first
    saved = get_saved_model()
    models = list_ollama_models()

    if not models:
        print(f"\n{RED}{BOLD}  ✖ No Ollama models found!{RESET}")
        print(f"{YELLOW}  Pull a model first:{RESET}")
        print(f"    ollama pull gemma2:2b\n")
        return None

    # If saved model exists and is available, use it silently
    if saved and saved in models:
        print(f"  {DIM}Model: {saved}{RESET}")
        return saved

    # If only one model, use it automatically
    if len(models) == 1:
        print(f"  {DIM}Model: {models[0]}{RESET}")
        return models[0]

    # Multiple models, no saved preference — ask user to pick
    print(f"\n{YELLOW}{BOLD}  Select an Ollama model:{RESET}\n")
    for i, model in enumerate(models, 1):
        print(f"    {CYAN}{i}.{RESET} {model}")
    print()

    while True:
        try:
            choice = input(f"{GREEN}{BOLD}  Enter number (1-{len(models)}): {RESET}").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(models):
                return models[idx]
            print(f"{RED}  Invalid choice.{RESET}")
        except ValueError:
            print(f"{RED}  Enter a number.{RESET}")


def main():
    """Main CLI entry point — type `momo` and go."""

    # ── Step 1: Auto-start Ollama ──
    if not _start_ollama():
        sys.exit(1)

    # ── Step 2: Auth ──
    if is_first_run():
        # First run: pick model first, then set password
        model = _get_model()
        if not model:
            sys.exit(1)

        result = first_time_setup(model)
        if not result:
            sys.exit(1)

        selected_model = model
    else:
        # Returning user: password first
        if not verify_password():
            sys.exit(1)

        selected_model = _get_model()
        if not selected_model:
            sys.exit(1)

    # ── Step 3: Chat ──
    banner(selected_model)

    # In-session only — NOT persisted anywhere
    history: list[dict] = []

    while True:
        try:
            user_input = input(f"{GREEN}{BOLD}You ➤ {RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            history.clear()
            print(f"\n{DIM}  🗑 Chat history destroyed.{RESET}")
            print(f"{YELLOW}  Goodbye! 👋{RESET}")
            sys.exit(0)

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            history.clear()
            print(f"\n{DIM}  🗑 Chat history destroyed.{RESET}")
            print(f"{YELLOW}  Goodbye! 👋{RESET}")
            break

        if user_input.lower() == "clear":
            history.clear()
            print(f"{DIM}  ↻ Conversation cleared.{RESET}\n")
            continue

        # ── Get AI response ──
        print(f"{DIM}  ⏳ Thinking...{RESET}", end="\r")

        response = chat(user_input, selected_model, history)

        print(" " * 40, end="\r")
        print(f"{CYAN}{BOLD}MOMO ➤ {RESET}{response}\n")

        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()

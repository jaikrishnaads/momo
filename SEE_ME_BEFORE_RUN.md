# 📋 SEE ME BEFORE RUN

> **⚠️ READ THIS COMPLETELY before doing anything. Follow every step in order.**

---

## 🔧 What You Need Before Setup

Make sure these are installed on your system:

| # | Requirement | Download Link |
|---|-------------|---------------|
| 1 | **Python 3.10+** | [python.org/downloads](https://www.python.org/downloads/) |
| 2 | **Ollama** | [ollama.com/download](https://ollama.com/download) |

> ⚠️ **Ollama is a separate app** — it is the AI engine that runs the brain. Install it first.

---

## 📥 Setup Steps

### Step 1: Install Ollama

1. Go to [ollama.com/download](https://ollama.com/download)
2. Download and install for your OS (Windows / Mac / Linux)
3. Verify it works — open a terminal and run:
   ```
   ollama --version
   ```

### Step 2: Download an AI Model

Open a terminal and run:

```
ollama pull gemma2:2b
```

This downloads the AI model (~1.6 GB). Wait for it to finish.

**Other models you can use (recommended for low-end PCs):**

| Model | Size | RAM Usage | Command |
|-------|------|-----------|---------|
| gemma3:1b | ~815 MB | ~1 GB | `ollama pull gemma3:1b` |
| gemma2:2b | ~1.6 GB | ~2 GB | `ollama pull gemma2:2b` |
| llama3.2:1b | ~1.3 GB | ~1.5 GB | `ollama pull llama3.2:1b` |

> 💡 You can pull multiple models. MOMO will let you choose during setup.

### Step 3: Install MOMO

Open a terminal **inside this folder** and run:

```
pip install .
```

This installs MOMO and all its dependencies. After this, the `momo` command works globally.

> 💡 If you want to use a virtual environment:
> ```
> python -m venv .venv
> .venv\Scripts\activate
> pip install .
> ```

### Step 4: Run MOMO

Just type:

```
momo
```

**That's it!** MOMO handles everything automatically from here.

---

## 🔐 First Time Running `momo`

When you type `momo` for the first time, it will:

1. **Start the Ollama server** automatically (no manual work needed)
2. **Detect your models** — if you have one, it uses it. If multiple, you pick.
3. **Ask you to set a password:**
   - Must be **8–10 characters**
   - Stored securely (SHA-256 hashed, NOT plain text)
   - You need this **every time** you run MOMO
   - ⚠️ **If you enter the wrong password later, ALL files will be deleted!**

---

## 🔁 Running MOMO After Setup

```
momo
```

1. Ollama starts automatically
2. Enter your password
3. Chat with AI!

---

## 💬 Using MOMO

| What to do | How |
|------------|-----|
| Ask a question | Just type it and press Enter |
| Clear conversation | Type `clear` |
| Exit MOMO | Type `exit` or `quit` |
| Emergency exit | Press `Ctrl+C` |

> 🗑️ **All chats are temporary** — when you exit, everything is gone. Nothing is saved.

---

## ⚠️ Important Warnings

- **Wrong password = ALL files deleted** — no recovery
- **No "forgot password" option** — remember your password
- **No chat history** — conversations are destroyed on exit
- **Ollama must be installed first** — MOMO cannot work without it

---

## 🆘 Problems?

| Problem | Fix |
|---------|-----|
| `momo` command not found | Run `pip install .` again inside this folder |
| "Ollama is not installed" | Download Ollama from [ollama.com](https://ollama.com/download) |
| "No Ollama models found" | Run `ollama pull gemma2:2b` |
| Forgot password | Reinstall MOMO from scratch |

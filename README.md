# 🤖 MOMO AI Chatbot

A terminal AI chatbot powered by **Ollama (gemma2:2b)** + **DuckDuckGo** web search.  
Install once, then just type **`momo`** in any terminal to chat.

---

## 🚀 Setup

### 1. Install Ollama (one-time, separate)

Download and install from [ollama.com/download](https://ollama.com/download), then pull the model:

```bash
ollama pull gemma2:2b
```

### 2. Install MOMO

```bash
pip install .
```

This installs MOMO globally on your system. You can now use the `momo` command from **any folder or drive** (C:, D:, E:).

### 3. Use it

Start Ollama (if not already running):
```bash
ollama serve
```

Then just type:
```bash
momo
```

That's it! 🎉

---

## 💥 Recovery (Wrong Password / Self-Destruct)

If you enter the wrong password, the project deletes its own source code out of security. To recover:
1. Uninstall the broken command: `pip uninstall momo -y`
2. Extract the original project folder again from your backup/ZIP.
3. CD into the new folder and run `pip install .` to reinstall.

---

## 📁 Project Structure

```
├── pyproject.toml         # Package config + CLI entry point
├── momo/
│   ├── __init__.py        # Package init
│   ├── engine.py          # LangChain engine (Ollama + DuckDuckGo)
│   └── cli.py             # Terminal chatbot interface
```

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| LLM | Ollama (gemma2:2b) — runs locally |
| Framework | LangChain |
| Web Search | DuckDuckGo |
| Interface | Terminal CLI (`momo` command) |

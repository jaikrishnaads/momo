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

This installs MOMO and all its dependencies automatically.

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

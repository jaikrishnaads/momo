"""
MOMO Chatbot Engine
Uses local Ollama LLM + DuckDuckGo web search.
Model is selected during first-time setup and saved.
"""

import json
import urllib.request
import urllib.error
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from duckduckgo_search import DDGS

# ─── Configuration ───────────────────────────────────────────────
OLLAMA_BASE_URL = "http://localhost:11434"

# ─── Search Decision Keywords ────────────────────────────────────
SEARCH_KEYWORDS = [
    "price", "cost", "rate", "stock", "weather", "news", "today", "current",
    "latest", "now", "live", "who is", "who are", "president", "minister",
    "prime minister", "chief minister", "governor", "ceo", "election",
    "score", "match", "result", "release", "launch", "announce",
    "2024", "2025", "2026", "trending", "update", "recent",
]


def check_ollama() -> bool:
    """Check if Ollama server is running and reachable."""
    try:
        req = urllib.request.Request(OLLAMA_BASE_URL, method="GET")
        with urllib.request.urlopen(req, timeout=3):
            return True
    except (urllib.error.URLError, OSError):
        return False


def list_ollama_models() -> list[str]:
    """Get list of locally available Ollama models."""
    try:
        req = urllib.request.Request(f"{OLLAMA_BASE_URL}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            models = data.get("models", [])
            return [m["name"] for m in models]
    except Exception:
        return []


def _get_llm(model: str):
    """Create a new LLM instance with the specified model."""
    return ChatOllama(
        model=model,
        base_url=OLLAMA_BASE_URL,
        temperature=0.5,
    )


def needs_search(query: str, llm) -> bool:
    """Decide if a query needs web search — keyword check + LLM fallback."""
    query_lower = query.lower()

    # Fast keyword check
    for kw in SEARCH_KEYWORDS:
        if kw in query_lower:
            return True

    # LLM fallback decision
    try:
        parser = StrOutputParser()
        decision_prompt = ChatPromptTemplate.from_messages([
            ("system", "Reply ONLY 'SEARCH' or 'KNOW'. Say SEARCH if the query needs current/real-time information from the internet. Say KNOW if you can answer from general knowledge."),
            ("human", "Query: {query}\n\nSEARCH or KNOW?"),
        ])
        chain = decision_prompt | llm | parser
        result = chain.invoke({"query": query})
        return "SEARCH" in result.strip().upper()
    except Exception:
        return False


def web_search(query: str, max_results: int = 5) -> str | None:
    """Search DuckDuckGo and return formatted results."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, region="in-en", max_results=max_results))
            if results:
                return "\n".join(
                    f"[{i+1}] {r['title']}\n{r['body']}" for i, r in enumerate(results)
                )
    except Exception:
        pass
    return None


# ─── System Prompt ────────────────────────────────────────────────
SYSTEM_PROMPT = """You are MOMO, a friendly and intelligent AI assistant.

RULES:
1. Be concise, helpful, and conversational.
2. When web search results are provided, use them to answer and briefly cite sources.
3. If no search results are provided, answer from your own knowledge.
4. If you don't know something, say so honestly."""


def chat(user_message: str, model: str, history: list[dict] = None) -> str:
    """
    Process a user message through the LangChain pipeline.

    Args:
        user_message: The user's input text
        model: Ollama model name to use
        history: List of {"role": "user"|"assistant", "content": "..."} dicts

    Returns:
        The AI's response string
    """
    llm = _get_llm(model)

    # ── Step 1: Decide search ──
    search_results = None
    if needs_search(user_message, llm):
        search_results = web_search(user_message)

    # ── Step 2: Build messages ──
    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    # Add conversation history (last 10 pairs)
    if history:
        for msg in history[-20:]:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))

    # ── Step 3: Construct final prompt ──
    if search_results:
        final_prompt = f"""Here are real-time web search results for context:

{search_results}

User Question: {user_message}

Answer using the search results above. Cite sources briefly."""
    else:
        final_prompt = user_message

    messages.append(HumanMessage(content=final_prompt))

    # ── Step 4: Call LLM ──
    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

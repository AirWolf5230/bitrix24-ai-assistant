import httpx

from app.assistant.prompts import SYSTEM_PROMPT
from app.knowledge.storage import load_store


OLLAMA_URL = "http://172.17.32.1:11434/api/generate"
MODEL = "gemma4:latest"


store = load_store()


async def ask_llm(question: str):

    # 1. поиск релевантных документов
    context_chunks = await store.search(question)

    context = "\n\n".join(context_chunks)

    # 2. сбор промпта
    prompt = f"""
{SYSTEM_PROMPT}

Ты отвечаешь только по документации Bitrix24 API.

Если ответа нет в контексте — скажи:
"В документации Bitrix24 информации не найдено."

---

КОНТЕКСТ:
{context}

---

ВОПРОС:
{question}

---

ОТВЕТ:
"""

    # 3. запрос в Ollama
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            }
        )

    return r.json().get("response", "")
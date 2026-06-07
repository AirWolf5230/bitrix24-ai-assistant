import httpx

OLLAMA_URL = "http://172.17.32.1:11434/api/generate"
MODEL = "gemma4:latest"


async def process_user_message(message: str) -> str:
    """
    Главный сервис обработки сообщений:
    - сюда потом подключим RAG
    - сейчас просто Ollama + контекст
    """

    try:
        prompt = build_prompt(message)

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "stream": False
                }
            )

        data = response.json()
        return data.get("response", "Пустой ответ модели")

    except Exception as e:
        print("OLLAMA ERROR:", repr(e))
        return "Ошибка обращения к модели"


def build_prompt(user_text: str) -> str:
    """
    Здесь потом будет RAG (Bitrix docs)
    """

    SYSTEM = """
Ты технический ассистент по Bitrix24 API.
Отвечай кратко, по делу, на русском языке.
Если не знаешь — так и скажи.
"""

    return f"{SYSTEM}\n\nВопрос: {user_text}\nОтвет:"
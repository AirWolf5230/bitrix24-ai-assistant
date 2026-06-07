import faiss
import numpy as np
import httpx

EMBED_MODEL = "nomic-embed-text"
OLLAMA_URL = "http://172.17.32.1:11434/api/embeddings"


class VectorStore:
    def __init__(self, dim=768):
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []

    async def embed(self, text: str):
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(
                OLLAMA_URL,
                json={
                    "model": EMBED_MODEL,
                    "prompt": text
                }
            )

        return np.array(r.json()["embedding"], dtype="float32")

    async def add(self, text: str):
        vec = await self.embed(text)

        if vec.shape[0] != 768:
            vec = vec[:768]  # защита от несовпадения размерности

        self.index.add(np.array([vec]))
        self.texts.append(text)

    async def search(self, query: str, k=5):
        q = await self.embed(query)

        if q.shape[0] != 768:
            q = q[:768]

        D, I = self.index.search(np.array([q]), k)

        return [self.texts[i] for i in I[0] if i < len(self.texts)]
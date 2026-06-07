import asyncio
import pickle

from app.knowledge.parser import crawl
from app.knowledge.search import VectorStore


async def build():

    print("START RAG BUILD")

    chunks = crawl("https://apidocs.bitrix24.ru/")

    print(f"TOTAL CHUNKS: {len(chunks)}")

    store = VectorStore()

    for i, chunk in enumerate(chunks[:200]):

        try:
            await store.add(chunk)
        except Exception as e:
            print("EMBED ERROR:", e)

        if i % 10 == 0:
            print(f"EMBEDDED {i}/{len(chunks)}")

    with open("app/knowledge/storage/index.pkl", "wb") as f:
        pickle.dump(store, f)

    print("RAG READY")


if __name__ == "__main__":
    asyncio.run(build())
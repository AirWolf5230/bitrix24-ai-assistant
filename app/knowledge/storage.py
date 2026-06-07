import pickle
import os


INDEX_PATH = "app/knowledge/storage/index.pkl"


def load_store():
    if not os.path.exists(INDEX_PATH):
        raise RuntimeError("RAG индекс не найден. Сначала запусти build_db")

    with open(INDEX_PATH, "rb") as f:
        return pickle.load(f)
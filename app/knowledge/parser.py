import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://apidocs.bitrix24.ru/"


def fetch(url: str):
    print(f"[HTTP] {url}")
    r = requests.get(
        url,
        timeout=20,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    r.raise_for_status()
    return r.text


def extract_links(html: str):
    soup = BeautifulSoup(html, "lxml")

    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if href.startswith("#"):
            continue

        full = urljoin(BASE_URL, href)

        if "apidocs.bitrix24.ru" in full:
            links.append(full)

    return list(set(links))


def extract_text(html: str):
    soup = BeautifulSoup(html, "lxml")

    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    text = soup.get_text("\n")

    lines = [
        l.strip()
        for l in text.split("\n")
        if len(l.strip()) > 30
    ]

    return lines


def crawl(start_url: str, max_pages: int = 20):
    visited = set()
    queue = [start_url]

    all_chunks = []

    while queue and len(visited) < max_pages:

        url = queue.pop(0)

        if url in visited:
            continue

        try:
            html = fetch(url)
        except Exception as e:
            print(f"[ERROR] {url} -> {e}")
            continue

        visited.add(url)

        chunks = extract_text(html)
        all_chunks.extend(chunks)

        print(f"[OK] {url} | chunks: {len(chunks)}")

        links = extract_links(html)

        for l in links[:50]:  
            if l not in visited:
                queue.append(l)

    print(f"[DONE] pages={len(visited)} chunks={len(all_chunks)}")

    return all_chunks
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json

BASE_URL = "https://seapol.com/"
visited = set()
collected_data = []

def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ["http", "https"] and BASE_URL in url

def crawl(url, depth=0, max_depth=3):
    if depth > max_depth:
        return
    if url in visited:
        return
    print(f"Crawling (depth {depth}): {url}")
    visited.add(url)

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return
    except requests.RequestException:
        return

    soup = BeautifulSoup(response.text, "lxml")

    # Get readable content
    page_text = soup.get_text(separator=' ', strip=True)
    collected_data.append({
        "url": url,
        "content": page_text
    })

    # Follow internal links
    for link in soup.find_all("a", href=True):
        next_url = urljoin(BASE_URL, link['href'])
        if is_valid_url(next_url) and next_url not in visited:
            crawl(next_url, depth + 1, max_depth)


def save_to_json(filename="website_data.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    crawl(BASE_URL)
    save_to_json()
    print(f"\n✅ Scraping completed. {len(collected_data)} pages saved to website_data.json")

import json
import re

BLACKLIST_KEYWORDS = [
    "read more", "click here", "home", "login", "submit",
    "menu", "search", "back to top", "toggle"
]

def is_relevant(text):
    text = text.strip()
    if len(text) < 50:  # increased minimum length
        return False
    text_lower = text.lower()

    if any(bad in text_lower for bad in BLACKLIST_KEYWORDS):
        return False

    if text_lower.count(" ") < 5:  # must have at least 5 words
        return False

    if len(set(text_lower)) <= 5:  # filter out junk
        return False

    return True


def clean_data(input_file="website_data.json", output_file="website_data_cleaned.json"):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 🔍 Debug: print the first few entries
    print(f"\n🔍 Loaded {len(data)} entries from {input_file}")
    for i, entry in enumerate(data[:10]):  # Show first 10 entries
        print(f"\nEntry {i+1}:")
        print("URL:", entry.get("url"))
        print("Content:", entry.get("content")[:200])  # First 200 characters of content

    cleaned = []
    seen = set()

    for entry in data:
        content = entry["content"].strip()
        if not is_relevant(content):
            continue
        content_hash = hash(content.lower())
        if content_hash in seen:
            continue
        seen.add(content_hash)
        cleaned.append({
            "url": entry["url"],
            "content": content
        })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Cleaned data saved to {output_file} ({len(cleaned)} entries)")

if __name__ == "__main__":
    clean_data()

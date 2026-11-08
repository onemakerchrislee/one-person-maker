
import json
import requests
import feedparser
from pathlib import Path
from datetime import datetime, timezone

SOURCES = {
    "OpenAI": "https://openai.com/news/rss.xml",
    "Google AI": "https://blog.google/technology/ai/rss/",
    "Hugging Face": "https://huggingface.co/blog/feed.xml"
}

news = []

headers = {
    "User-Agent": "Daily-AI-Radar/1.0"
}

for source, url in SOURCES.items():
    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )
        response.raise_for_status()

        feed = feedparser.parse(response.content)

        for entry in feed.entries[:15]:
            news.append({
                "source": source,
                "title": entry.get("title", ""),
                "summary": entry.get("summary", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", "")
            })

        print(f"{source}: collected {len(feed.entries)} entries")

    except Exception as error:
        print(f"{source} failed: {error}")

if not news:
    raise RuntimeError("No news collected. Please check RSS sources.")

news.sort(
    key=lambda item: item["published"],
    reverse=True
)

output = Path(__file__).parent / "news.json"

with open(output, "w", encoding="utf-8") as file:
    json.dump(news, file, ensure_ascii=False, indent=2)

print(f"Successfully saved {len(news)} news items.")
print(f"Output: {output}")


from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
import os
from dotenv import load_dotenv
load_dotenv()

@tool
def duckduckgo_search(query: str) -> str:
    """Search the web using DuckDuckGo."""

    try:
        # Use primp backend (faster, no Yandex fallback issues)
        results = DDGS(timeout=20).text(
            query,
            max_results=5,
            backend="lite",   # uses lite.duckduckgo.com — avoids Yandex redirect
        )
    except Exception:
        # Fallback: plain backend with longer timeout
        results = DDGS(timeout=30).text(
            query,
            max_results=5,
            backend="api",
        )

    output = []
    for result in results:
        output.append(
            f"Title: {result['title']}\n"
            f"URL: {result['href']}\n"
            f"Content: {result['body']}\n"
        )

    return "\n".join(output) if output else "No results found."

@tool
def scrape_webpage(url: str) -> str:
    """Extract text content from a webpage."""

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
            timeout=20,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Could not retrieve page: {e}"

    soup = BeautifulSoup(response.text, "lxml")

    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)

    return text[:10000]

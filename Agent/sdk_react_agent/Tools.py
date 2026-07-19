"""
Tools.py — Web search and deep research tools.
"""

from __future__ import annotations

from typing import Callable
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

Emitter = Callable[[str, str], None]

BAD_DOMAINS = ["linkedin.com", "facebook.com", "instagram.com"]
MAX_PAGE_CHARS = 2000  # characters per page (enough context, won't blow up model)
MAX_SEARCH_RESULTS = 3


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _fetch_page(url: str, emit: Emitter) -> str:
    """Fetch a URL and return cleaned plain text (capped at MAX_PAGE_CHARS)."""
    try:
        emit("FETCH", f"Fetching: {url}")
        resp = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        emit(
            "FETCH",
            f"Extracted {len(text):,} characters → capping at {MAX_PAGE_CHARS:,}",
        )
        return text[:MAX_PAGE_CHARS]

    except Exception as exc:
        emit("FETCH", f"Failed ({url}): {exc}")
        return ""


# ---------------------------------------------------------------------------
# Public tools
# ---------------------------------------------------------------------------


def search(query: str, emit: Emitter) -> list[dict]:
    """
    Search the web for `query` using DuckDuckGo.

    Returns a list of dicts:
        [{"title": str, "href": str, "content": str}, ...]
    """
    emit("SEARCH", f"Query: {query!r}")
    results: list[dict] = []

    with DDGS() as ddgs:
        for doc in ddgs.text(query, max_results=MAX_SEARCH_RESULTS):
            url = doc.get("href", "")
            if any(bad in url for bad in BAD_DOMAINS):
                emit("SEARCH", f"Skipping blocked domain: {url}")
                continue

            title = doc.get("title", "")
            emit("SEARCH", f"Processing: {title}")
            page_text = _fetch_page(url, emit)

            if page_text:
                results.append({"title": title, "href": url, "content": page_text})

    emit("SEARCH", f"Done — {len(results)} result(s) with content")
    return results


def research(query: str, sources: list[dict], emit: Emitter) -> str:
    """
    Synthesise research from already-fetched `sources`.

    `sources` must be a list of dicts with keys: title, href, content.
    Returns a formatted string summarising the findings.
    """
    emit("RESEARCH", f"Starting research: {query!r}")

    if not sources:
        emit("RESEARCH", "No sources provided.")
        return "No sources available for research."

    sections: list[str] = []
    for i, item in enumerate(sources, start=1):
        title = item.get("title", "Untitled")
        url = item.get("href", "")
        content = item.get("content", "")
        emit("RESEARCH", f"[{i}/{len(sources)}] {title}")
        sections.append(f"Source {i}: {title}\nURL: {url}\n\n{content}\n{'─' * 60}")

    emit("RESEARCH", "Done.")
    return f"Research query: {query}\n\n" + "\n\n".join(sections)

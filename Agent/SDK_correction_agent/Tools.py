from bs4 import BeautifulSoup
import requests
from ddgs import DDGS

# from Tools import tool

BAD_DOMAINS = ["linkedin.com", "facebook.com", "instagram.com"]


# --------------------
# FETCH PAGE
# --------------------
def Fetch_page(url: str, emit) -> str:
    try:
        emit("FETCH", f"Fetching URL: {url}")
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()

        emit("FETCH", "Parsing content...")
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove noise: scripts, styles, nav, footer
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        emit("FETCH", f"Extracted {len(text)} characters")
        return text[:1000]  # cap to avoid overflowing model context

    except Exception as e:
        emit("FETCH", f"Failed to fetch {url}: {e}")
        return ""


# --------------------
# SEARCH
# --------------------
# @tool
def search(query: str, emit) -> list:
    emit("SEARCH", f"Searching for: {query}")
    content = []

    with DDGS() as ddgs:
        for doc in ddgs.text(query, max_results=3):
            url = doc["href"]

            if any(domain in url for domain in BAD_DOMAINS):
                emit("SEARCH", f"Skipping blocked domain: {url}")
                continue

            emit("SEARCH", f"Fetching content: {doc['title']}")
            page_text = Fetch_page(url=url, emit=emit)  # ✅ actually use the result

            if page_text:  # only add if we got content
                content.append(
                    {
                        "title": doc["title"],
                        "href": url,
                        "content": page_text,  # ✅ real content included
                    }
                )

    emit("SEARCH", f"Returning {len(content)} results with content")
    return content


# --------------------
# RESEARCH
# --------------------
# @tool
def research(query: str, sources: list, emit) -> str:
    emit("RESEARCH", f"Starting research: {query}")

    # results = search(query, emit)  # ✅ missing line that was causing the crash

    if not sources:
        emit("RESEARCH", "No sources found.")
        return "No sources for research found."

    research_result = []
    total = len(sources)

    for i, item in enumerate(sources):
        url = item["href"]
        title = item["title"]
        content = item.get("content", "")  # ✅ content already fetched by search()

        emit("RESEARCH", f"[{i+1}/{total}] Processing: {title}")

        research_result.append(f"""
Query: {query}
Title: {title}
URL: {url}

Content:
{content}

----------------------------------------
""")

    emit("RESEARCH", "Research completed")
    return "\n".join(research_result)

from langchain.tools import tool
from tavily import TavilyClient

import requests
from bs4 import BeautifulSoup

search_engine = TavilyClient()


@tool
def search(query):
    """
    search the given quey and return the result
    """

    state = {}

    search_result = search_engine.search(query=query, max_results=5)
    for i, item in enumerate(search_result):
        title = item["title"]
        URl = item["href"]
        content = item["content"]
        state["search_result"] = URl

    return state


@tool
def resaerch(url):
    """
    get all urls and research deeply for better and efficent answers

    """

    response = requests.get(url=url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for tags in soup.find_all(
        [
            "nav",
            "header",
            "footer",
            "aside",
            "script",
            "style",
            "noscript",
            "iframe",
            "form",
            "button",
            "svg",
        ]
    ):
        tags.decompose()

    text = soup.get_text(separator=" ", strip=True)
    return text[:3000]

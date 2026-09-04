from ddgs import DDGS


def search_web(query: str, max_results: int = 3) -> str:
    """Search the web for current, real-time information relevant to
    international students in Korea, not found in the guidebook or FAQ."""
    with DDGS() as ddgs:
        results = list(ddgs.text(query, region="kr-kr", max_results=max_results))

    if not results:
        return "No web results found."

    formatted = []
    for result in results:
        title = result.get("title", "No title")
        body = result.get("body", "")
        href = result.get("href", "")
        formatted.append(f"{title}\n{body}\nSource: {href}")

    return "\n\n---\n\n".join(formatted)
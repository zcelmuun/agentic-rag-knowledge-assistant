import socket

_original_getaddrinfo = socket.getaddrinfo

def _ipv4_only_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    return _original_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)

socket.getaddrinfo = _ipv4_only_getaddrinfo


from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

import os
from dotenv import load_dotenv

load_dotenv()

model = SentenceTransformer("BAAI/bge-m3")
client = QdrantClient(
    url=os.environ.get("QDRANT_URL"),
    api_key=os.environ.get("QDRANT_API_KEY")
)


def search_guidebook(query: str, top_k: int = 3) -> str:
    """Search the CBNU guidebook for information relevant to the query."""
    query_vector = model.encode(query).tolist()

    results = client.query_points(
        collection_name="cbnu_guidebook",
        query=query_vector,
        limit=top_k
    ).points

    if not results:
        return "No relevant information found in the guidebook."

    formatted_results = []
    for result in results:
        section_title = result.payload["section_title"]
        language = result.payload["language"]
        text = result.payload["text"]
        formatted_results.append(
            f"[Section: {section_title} | Language: {language}]\n{text}"
        )

    return "\n\n---\n\n".join(formatted_results)


from src.sql_store.queries import search_faq as _search_faq


def search_faq_tool(query: str, language: str = "en") -> str:
    """Search frequently asked questions about CBNU academic rules,
    part-time work, leave of absence, and insurance. Use this for quick,
    direct questions before doing a full guidebook search. Language must
    be 'en', 'ko', or 'zh'."""
    return _search_faq(query, language)
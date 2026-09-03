from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-m3")
client = QdrantClient(host="localhost", port=6333)


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
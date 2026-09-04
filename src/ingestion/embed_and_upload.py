import json
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer

load_dotenv()

with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks.")

model = SentenceTransformer("intfloat/multilingual-e5-small")
client = QdrantClient(
    url=os.environ.get("QDRANT_URL"),
    api_key=os.environ.get("QDRANT_API_KEY")
)

points = []
for i, chunk in enumerate(chunks):
    vector = model.encode(chunk["text"]).tolist()
    point = PointStruct(id=i, vector=vector, payload=chunk)
    points.append(point)
    print(f"Embedded chunk {i + 1}/{len(chunks)}")

client.upsert(collection_name="cbnu_guidebook_v2", points=points)

print(f"Uploaded {len(points)} points to Qdrant collection 'cbnu_guidebook_v2'.")

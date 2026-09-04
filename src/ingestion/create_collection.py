import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

load_dotenv()

client = QdrantClient(
    url=os.environ.get("QDRANT_URL"),
    api_key=os.environ.get("QDRANT_API_KEY")
)

client.create_collection(
    collection_name="cbnu_guidebook_v2",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

print("Collection 'cbnu_guidebook_v2' created successfully.")

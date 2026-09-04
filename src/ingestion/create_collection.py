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
    collection_name="cbnu_guidebook",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
)

print("Collection 'cbnu_guidebook' created successfully.")

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(host="localhost", port=6333)

client.create_collection(
    collection_name="cbnu_guidebook",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
)

print("Collection 'cbnu_guidebook' created successfully.")
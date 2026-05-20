from pinecone import Pinecone,ServerlessSpec

# Initialize a Pinecone client with your API key
pc = Pinecone(api_key="")

# Create an index for dense vectors with integrated embedding
# index_name = "medicalindex"
index = pc.Index("medicalindex")
dummy_vector_1024 = [0.1] * 1024

vectors = [
        ("vec1", dummy_vector_1024, {"genre": "comedy"})

]

index.upsert(vectors=vectors)

import chromadb
chroma_client = chromadb.PersistentClient()

collection = chroma_client.get_collection('fitness_source')


def test_storage_vector():
    data = collection.query(
        query_texts=["healthy diet"],
        n_results=5,
    )
    assert data != None
    print(data)
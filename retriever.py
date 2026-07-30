import chromadb
from chromadb.utils import embedding_functions
from config import CHROMA_COLLECTION, CHROMA_PATH, EMBEDDING_MODEL, N_RESULTS

# Lazy-initialized globals — keep imports cheap at module load.
_ef = None
_client = None
_collection = None


def _init_collection():
    """Initialize the embedding function, client, and collection on first use."""
    global _ef, _client, _collection
    if _collection is not None:
        return _collection

    # Initialize embedding function (may download model on first use)
    _ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )

    # Initialize client and collection
    _client = chromadb.PersistentClient(path=CHROMA_PATH)
    _collection = _client.get_or_create_collection(
        name=CHROMA_COLLECTION,
        embedding_function=_ef,
        metadata={"hnsw:space": "cosine"},
    )

    return _collection


def get_collection():
    """Return the ChromaDB collection, initializing it lazily on first use."""
    return _init_collection()


def embed_and_store(chunks):
    """
    Embed a list of chunks and store them in the vector database.

    This function is already implemented — read through it before moving on.

    _collection.add() takes three parallel lists built from the chunks
    returned by chunk_document():
      - documents : raw text strings — ChromaDB's embedding function converts
                    these to vectors automatically using sentence-transformers
      - metadatas : one dict per chunk, stored alongside the vector so that
                    retrieve() can surface which game a result came from
      - ids       : the unique chunk_id strings used to identify each entry

    You don't generate embeddings manually here — you hand over the text
    and ChromaDB handles the vector math.
    """
    collection = get_collection()
    collection.add(
        documents=[c["text"] for c in chunks],
        metadatas=[{"game": c["game"]} for c in chunks],
        ids=[c["chunk_id"] for c in chunks],
    )
    print(f"Stored {collection.count()} total chunks in the vector database.")


def retrieve(query: str, top_k: int = N_RESULTS) -> list[dict]:
    """
    Find the most relevant rule chunks for a user's question.
    Retrieves the most relevant document chunks for a given query using semantic search.

    Use _collection.query() to run a semantic search. It takes:
      - query_texts : a list containing your query string
      - n_results   : how many results to return
      - include     : what to return — use ["documents", "metadatas", "distances"]

    Return a list of dicts, each with:
      - "text"     : the chunk text
      - "game"     : the game name (pulled from metadata)
      - "distance" : the similarity score (lower = more similar for cosine)
    """
    collection = get_collection()

    if collection.count() == 0:
        return []

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    retrieved_chunks = []

    if not results or not results.get("documents") or not results["documents"][0]:
        return retrieved_chunks

    documents = results["documents"][0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results["distances"][0]

    for doc, meta, dist in zip(documents, metadatas, distances):
        retrieved_chunks.append({
                "text": doc,
                "game": meta.get("game", "Unknown") if isinstance(meta, dict) else "Unknown",
                "distance": dist
        })   

        print(f"[{meta.get('game', 'Unknown') if isinstance(meta, dict) else 'Unknown'}] (dist: {dist:.3f}) {doc[:80]}...")

    return retrieved_chunks

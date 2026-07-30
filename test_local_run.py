from app import run_ingestion
from retriever import retrieve
from generator import generate_response

if __name__ == "__main__":
    print("Running ingestion...")
    run_ingestion()

    query = "How do you set up the board in Catan?"
    print(f"Retrieving for: {query}")
    retrieved = retrieve(query)
    print(f"Retrieved {len(retrieved)} chunks")
    for i, r in enumerate(retrieved, start=1):
        print(f"{i}. [{r.get('game')}] dist={r.get('distance'):.3f} text={r.get('text')[:80]}...")

    print("Generating response...")
    answer = generate_response(query, retrieved)
    print("\nAnswer:\n", answer)

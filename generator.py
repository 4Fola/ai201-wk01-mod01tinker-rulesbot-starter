from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


def _format_context(retrieved_chunks):
    """Turn retrieved chunks into a compact prompt-friendly context block."""
    formatted_chunks = []
    for index, chunk in enumerate(retrieved_chunks[:5], start=1):
        game = chunk.get("game", "Unknown")
        text = " ".join(str(chunk.get("text", "")).split())
        distance = chunk.get("distance")

        header = f"Chunk {index} | Game: {game}"
        if distance is not None:
            header += f" | Relevance: {distance:.3f}"

        formatted_chunks.append(f"{header}\n{text}")

    return "\n\n".join(formatted_chunks)


def _fallback_response(query, retrieved_chunks):
    """Create a useful grounded answer even when the LLM is unavailable."""
    top_chunk = retrieved_chunks[0]
    game = top_chunk.get("game", "Unknown")
    excerpt = " ".join(str(top_chunk.get("text", "")).split())
    snippet = excerpt[:500]

    return (
        f"Based on the loaded rules for {game}, the closest match I found is: {snippet}...\n"
        "This answer is grounded in the retrieved rule excerpts and may be incomplete. "
        "If you add a GROQ API key, the app can generate a more polished response."
    )


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved rule chunks.

    The response is built from the retrieved excerpts only. If the LLM is not
    available, the function falls back to a concise summary of the best match.
    """
    if not retrieved_chunks:
        return (
            "I couldn't find anything relevant in the loaded rule books. "
            "Try rephrasing your question — or check that your ingestion pipeline is working."
        )

    context = _format_context(retrieved_chunks)

    if _client is None:
        return _fallback_response(query, retrieved_chunks)

    try:
        completion = _client.chat.completions.create(
            model=LLM_MODEL,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Answer using only the supplied rule excerpts. "
                        "Do not use outside board-game knowledge. "
                        "Mention which game the answer comes from. "
                        "If the excerpts do not contain enough information, say so clearly."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Question: {query}\n\n"
                        f"Rule excerpts:\n{context}\n\n"
                        "Provide a concise answer grounded in these excerpts."
                    ),
                },
            ],
        )
        answer = completion.choices[0].message.content
        if answer and answer.strip():
            return answer.strip()
    except Exception:
        pass

    return _fallback_response(query, retrieved_chunks)

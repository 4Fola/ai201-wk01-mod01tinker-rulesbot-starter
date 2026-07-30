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
    if not retrieved_chunks:
        return (
            "I couldn't find anything relevant in the loaded rule books. "
            "Try rephrasing your question — or check that your ingestion pipeline is working."
        )

    top_chunk = retrieved_chunks[0]
    game = top_chunk.get("game", "Unknown")
    excerpt = " ".join(str(top_chunk.get("text", "")).split())
    snippet = excerpt[:500]

    return (
        f"Based on the loaded rules for {game}, the closest match I found is: {snippet}...\n"
        "This answer is grounded in the retrieved rule excerpts and may be incomplete. "
        "If you add a GROQ API key, the app can generate a more polished response."
    )


def generate_response(query: str, retrieved_chunks: list[dict]) -> str:
    """Generate a grounded answer from retrieved rule chunks.

    Uses the Groq client when an API key is present; otherwise falls back
    to a minimal grounded summary.

    Milestone 3: Generate a Grounded Response
    - Addressed: Grounding failures and hallucinations.
    - Logic: Applies a strict system prompt to prohibit outside knowledge and 
      formats context explicitly with source metadata.
    """

    if not retrieved_chunks:
        return _fallback_response(query, retrieved_chunks)

    # 1. Format the retrieved context cleanly for the LLM
    context = _format_context(retrieved_chunks)
    for chunk in retrieved_chunks:
        context += f"\nSource: {chunk['game']}\nRule: {chunk['text']}\n"

    if _client is None:
        return _fallback_response(query, retrieved_chunks)

    # 2. Define the strong grounding instruction (System Prompt)
    system_prompt = (
        "Answer using only the supplied rule excerpts. "
        "Do not use outside board-game knowledge. "
        "Mention which game the answer comes from. "
        "If the excerpts do not contain enough information, say so clearly."
        "do not draw on outside knowledge or fill in gaps from what you know about board games."
    )

    # 3. Combine the context and the user's query
    user_prompt = f"Question: {query}\n\nRule excerpts:\n{context}\n\nProvide a concise answer grounded in these excerpts."

    # 4. Generate the response via the LLM API
    # Assuming _client and config are imported at the top of the file per the starter repo
    try:
        completion = _client.chat.completions.create(
            model=LLM_MODEL, # Uses the model defined in config.py            
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0, # Using a low temperature enforces deterministic, grounded answers
        )

        # Groq responses mirror common chat-completion shapes
        answer = completion.choices[0].message.content
        if answer and answer.strip():
            return answer.strip()
    except Exception as e:
        print(f"LLM completion failed: {e}")

    # Return the generated text string
    return _fallback_response(query, retrieved_chunks)

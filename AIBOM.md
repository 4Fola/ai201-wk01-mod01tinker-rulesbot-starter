# RulesBot AI Bill of Materials (AIBOM)

| Component Category | Name / Tool | Purpose / Function | Origin / Source |
| :--- | :--- | :--- | :--- |
| **Embedding Model** | `sentence-transformers` | Converts document chunks and user queries into vector embeddings for semantic search. | Hugging Face / PyPI |
| **Generative Model** | Groq API (e.g., Llama 3 or Mixtral) | Generates grounded conversational responses based strictly on retrieved context. | Groq Cloud |
| **Vector Database** | ChromaDB | Stores text chunks and their embeddings; performs vector similarity search. | Open-Source / PyPI |
| **Dataset** | Board Game Rulebooks | Provides the factual grounding context for RAG generation. | Local `/docs` directory |
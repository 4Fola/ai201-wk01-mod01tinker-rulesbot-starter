# Spec: `retrieve()`

**File:** `retriever.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user's natural language query, find the most relevant chunks from the vector store using semantic similarity search. Return them ranked by relevance so that `generate_response()` can use them as context.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's natural language question |
| `n_results` | `int` | Maximum number of chunks to return (default: `N_RESULTS` from `config.py`) |

**Output:** `list[dict]`

Each dict in the returned list must contain exactly these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | The chunk text |
| `"game"` | `str` | The game name this chunk came from |
| `"distance"` | `float` | Cosine distance score — lower means more similar to the query |

Results should be ordered from most to least relevant (lowest to highest distance). Returns an empty list `[]` if the collection contains no documents.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Query approach

*Describe how you will use `_collection.query()` to find relevant chunks. What arguments will you pass, and why?*

```
[your answer here]
```

---

### Return structure

*Sketch out what one item in your return list looks like as a concrete example. Where does each field come from in the query results?*

```
The retrieval function will return a list of dictionaries, where each dictionary contains the chunk text, the game name (from metadata), and the distance score.
```

---

### Handling the nested result structure

*`_collection.query()` returns nested lists. Describe what index you need to access to get the actual list of results for a single query, and why the nesting exists.*

```
ChromaDB returns a nested list because it supports batch querying. Since we only pass one query string, we must access index [0] (e.g., results["documents"][0]) to get the actual lists of documents, metadata, and distances.
```

---

### Relevance threshold

*Will you filter out results above a certain distance score, or return all `n_results` regardless of how relevant they are? What are the tradeoffs of each approach?*

```
We will retrieve the top 3 results (top_k=3). A distance score around 0.1–0.2 indicates high relevance, while 0.7–0.9 means the context is loosely related.
```

---

### Edge cases

*How does your implementation behave when: (a) the collection is empty, (b) the query matches no chunks well, (c) the query matches chunks from multiple games?*

```
[your answer here]
```

---

### Questions:

*You query "how do you win?" and get back chunks from Catan, Ticket to Ride, Pandemic, and Monopoly. Is this a retrieval failure?*

```
No. The query "how do you win?" is semantically similar to the winning conditions of all four games. Semantic search correctly returned the most relevant chunks across the full corpus.
```

*What should RulesBot do when retrieving winning conditions across four games?*

```
Since the retrieval correctly matched the semantic intent across the database, the bot should ideally ask for clarification (e.g., "Which game are you asking about?"). Alternatively, it could summarize the winning conditions for all four games, though that risks hitting token limits or overwhelming the user.
```


---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 3.*

**Test query and top result returned:**

```
Query: [your test query]
Top result game: [game name]
Distance score: [score]
Does it make sense? [yes / no / explain]
```

**One thing about the query results that surprised you:**

```
[your answer here]
```

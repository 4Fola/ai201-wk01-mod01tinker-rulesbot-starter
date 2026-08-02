# Spec: `generate_response()`

**File:** `generator.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user query and a list of retrieved rule chunks, generate a response that directly answers the question using only the retrieved text as context. The response must be grounded — it should not draw on the model's general knowledge of board games, only on what was retrieved.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's original question |
| `retrieved_chunks` | `list[dict]` | Ranked list of chunks from `retrieve()`, each with `"text"`, `"game"`, and `"distance"` |

**Output:** `str`

A plain string containing the response to show the user. The response should:
- Answer the question using only the retrieved rule text
- Identify which game the answer comes from
- Acknowledge clearly when the answer is not found in the loaded rules

Returns a fallback string (not an error) when `retrieved_chunks` is empty.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Context formatting

*How will you format the retrieved chunks before passing them to the LLM? Describe the structure — not the code. Consider: will you label chunks by game? Include distance scores? Separate chunks with delimiters?*


```
Each retrieved chunk will be formatted with its explicit source (e.g., Source: [Game Name]\nRule: [Chunk Text]) to help the LLM properly cite the rules in its final answer
```

---

### System prompt — grounding instruction

*Write the exact system prompt instruction you will use to prevent the model from answering beyond the retrieved text. This is the most important design decision in this function.*

```
[your answer here]
"Answer using only the rule text provided below. If the answer is not contained in the provided text, say so explicitly — do not draw on outside knowledge or fill in gaps from what you know about board games."
```

---

### System prompt — citation instruction

*Write the exact instruction you will use to tell the model to identify which game its answer comes from.*

```
[your answer here]
```

---

### Fallback behavior

*What should the response say when the answer isn't found in the loaded rule books? Write the exact fallback message.*

```
[your answer here]
```

---

### Handling low-relevance chunks

*`retrieved_chunks` may include chunks with high distance scores (weak relevance). Will you filter these out before building context, pass them all in, or handle them another way? What are the tradeoffs?*

```
[your answer here]
```

---

### Message structure

*Describe how you will structure the messages list for the API call — what goes in the system message vs. the user message?*

```
[your answer here]
```

---

### Questions:

*You ask "can I trade resources with the bank?" and retrieval returns a Catan rule, but the bot describes Monopoly property trading. What most likely caused this?*

```
The system prompt's grounding instruction was too weak. By using a prompt like "use the provided context" rather than "answer only from the provided text," the model was left with room to draw on its training data when it thought it had a better answer.
```

*What is the primary purpose of including source citations in a RAG response?*

```
Citations allow users to verify the answer against the original document, making grounding failures detectable. A user who checks the cited source can tell whether the model answered from retrieved text or from training data.
```

*How do you figure out whether a confident, wrong answer is a retrieval failure or a generation failure?*

```
You must inspect the retrieved chunks. If the retrieved chunks contain the wrong information or belong to the wrong game, it is a retrieval failure. If the retrieved chunks contain the correct rule but the model ignored them to make something up, it is a generation (grounding) failure.
```

---

## Implementation Notes

*Fill this in after implementing and testing.*

**Test query and response:**

```
Query: How do you get out of Jail in Monopoly?
Response: Based on the loaded rules for Monopoly, the closest match I found is: a row. When sent to Jail, move directly to Jail — do not pass Go, do not collect $200. To get out of Jail: pay a $50 fine before rolling on any of your next three turns, use a Get Out of Jail Free card, or roll doubles on any of your three turns in Jail. If you have not rolled doubles after three t...
This answer is grounded in the retrieved rule excerpts and may be incomplete. If you add a GROQ API key, the app can generate a more polished response.
Correctly grounded? ✅ **YES** / no
Cited the right game? ✅ **YES** / no
```

**One thing you changed from your original spec after seeing the actual output:**

```
NA
```
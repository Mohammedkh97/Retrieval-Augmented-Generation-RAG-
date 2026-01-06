## 🎥 Video: Module 3 — Reranking  
**Instructor:** Zain Hassan  
**Video Duration:** ~4 minutes  
**Source:** [Coursera Reranking Lecture](https://www.coursera.org/learn/retrieval-augmented-generation-rag/lecture/HwQkZ/reranking)

---

## 🧠 1. What Is Reranking?

- Reranking is a **post-retrieval process**.
- It improves the **quality of retrieved documents** before sending them to the LLM.
- Uses **high-performing but expensive models** to re-score and re-rank the initial results.

> “A nice way to get the best of both worlds in semantic search is to just use multiple search techniques together.”

---

## 🔄 2. How Reranking Works

1. A **vector database** retrieves an initial set of documents.
2. A **reranker model** re-scores and reorders these documents.
3. Only the **most relevant subset** is passed to the LLM.

> “Since only a handful of documents need to be re-scored and re-ranked, it’s possible to use high-performing but costly models.”

![alt text](<images/Purpose of Reranking.png>)
---

## 🧪 3. Example Scenario

- Prompt: *“What is the capital of Canada?”*
- Vector search might return:
  - “Toronto is in Canada.”
  - “The capital of France is Paris.”
  - “Canada is the maple syrup capital of the world.”

None of these directly answer the question.

> “This is where the reranker can come in to re-score and re-rank these results so that only the truly relevant documents are ultimately returned.”

---

## 📈 4. Overfetching Strategy

- Retrieve **20–100 documents** using vector or hybrid search.
- Reranker re-scores them.
- Return **top 5–10** most relevant results.

> “You’ll usually over-fetch documents in your initial vector database retrieval.”

---

## 🧠 5. Cross-Encoder Reranking

- Most rerankers use a **cross-encoder architecture**.
- Cross-encoders:
  - Provide **better results** than bi-encoders.
  - Are **slower** and **not scalable** for full corpus search.
- But once bi-encoders narrow the list, cross-encoders become feasible.

> “A cross-encoder will add a little bit of latency… but this trade-off is almost always worth it.”

---

## 🤖 6. LLM-Based Reranking

- Similar to cross-encoders, but uses an **LLM** directly.
- LLM receives prompt + document pair.
- Returns a **numerical relevance score**.

> “LLMs specifically designed for this task are able to analyze the pair, assess their relevance, and respond with a numerical relevance score.”

![alt text](<images/LLMs Based Scoring.png>)
### ⚠️ Tradeoffs:
- Just as inefficient as cross-encoders.
- Scoring begins **only after prompt is received**.
- Still **costly per document**.

---

## ✅ 7. Practical Implementation

- Many vector databases support reranking with **a single line of configuration**.
- Example: Add `reranker=True` or specify a reranker model.
- Recommended strategy:
  - Overfetch **15–25 documents**
  - Rerank to select **top 5–10**

> “Using a reranker is one of the first techniques you should explore adding to your RAG pipeline.”

---

## 🧪 Summary Table

| Technique              | When Used                     | Pros                          | Cons                          |
|------------------------|-------------------------------|-------------------------------|-------------------------------|
| Bi-encoder retrieval   | Initial search                | Fast, scalable                | Moderate relevance            |
| Cross-encoder reranking| After narrowing candidates    | High relevance                | Slower, costly                |
| LLM-based reranking    | After narrowing candidates    | Flexible, high-quality        | Costly, latency-sensitive     |

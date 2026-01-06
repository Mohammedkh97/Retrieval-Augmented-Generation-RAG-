## 🎥 Video: Hybrid Search

**Instructor:** Zain Hassan  
**Module:** 2 — Information Retrieval  
**Duration:** ~7 minutes  
**Source:** [Coursera RAG Course](https://www.coursera.org/learn/retrieval-augmented-generation-rag/lecture/WOe6W/hybrid-search)

---

## 🧠 1. Purpose of Hybrid Search

- Hybrid search combines multiple retrieval techniques to **leverage their strengths** and **mitigate their weaknesses**.
- It’s the **default strategy** in most production-grade RAG systems.

---

## 🔍 2. Review of Individual Techniques

### a) Metadata Filtering

- Uses **rigid criteria** stored in document metadata to narrow down results.
- Fast, easy to implement, and interpretable.
- Not a true search technique—acts as a **strict yes/no filter**.

### b) Keyword Search

- Scores and ranks documents based on **exact keyword matches** with the prompt.
- Fast and effective, especially for:
  - Technical terms
  - Product names
- Limitation: **no semantic understanding**.

### c) Semantic Search

- Scores and ranks documents based on **meaning similarity**.
- Uses **vector embeddings** to represent prompts and documents.
- More flexible, but **computationally intensive**.

---

## 🧪 3. Hybrid Search Pipeline

### Step-by-step:

1. **Prompt Received**

   - The retriever receives a user prompt.

2. **Dual Search Execution**

   - Performs both:
     - **Keyword search**
     - **Semantic search**
   - Each returns a **ranked list** of ~50 documents.

3. **Metadata Filtering**

   - Both lists are filtered using metadata.
   - Example:
     - Keyword list → 35 docs
     - Semantic list → 30 docs

4. **Ranking Fusion**
   - Combine both filtered lists using **Reciprocal Rank Fusion (RRF)**.

![alt text](<images/Hybrid Search2.png>)

## 📐 4. Reciprocal Rank Fusion (RRF)

### Formula:

\[
\text{Score} = \sum\_{i} \frac{1}{k + r_i}
\]

Where:

- \( r_i \) = rank of the document in list \( i \)
- \( k \) = hyperparameter controlling rank sensitivity

### Example:

- Document ranked:
  - 2nd in keyword list → \( \frac{1}{2} = 0.5 \)
  - 10th in semantic list → \( \frac{1}{10} = 0.1 \)
- Total score = 0.6

![alt text](<images/RRF Calc.png>)

### Behavior:

- **Lower ranks = higher scores**
- **Documents ranked highly in either list are rewarded**
- **Documents appearing in both lists get additive scores**

---

## ⚙️ 5. Tuning the K Parameter

- **K = 0**:

  - Top-ranked document gets full weight (1.0)
  - 10th-ranked gets 0.1 → 10× difference
  - Can cause **dominance by one list**

- **K = 50**:
  - Top-ranked = 1/50 = 0.02
  - 10th-ranked = 1/60 = ~0.0167
  - **Balances influence** across ranks

> RRF only considers **rank**, not the raw scores that produced those ranks.

---

## ⚖️ 6. Beta Weighting Between Search Types

- A second hyperparameter, **β (beta)**, controls weighting between:
  - Semantic search
  - Keyword search

### Example:

- β = 0.8 → 80% semantic, 20% keyword
- β = 0.3 → 30% semantic, 70% keyword

### Use Cases:

- **Exact match critical** → favor keyword search
- **Meaning match preferred** → favor semantic search

> A 70–30 semantic–keyword split is a **good starting point**.

---

## 📦 7. Final Document Selection

- After fusion and weighting:
  - Select **top-K documents** from the final ranking.
  - These are returned by the retriever.

---

## ✅ 8. Benefits of Hybrid Search

| Technique          | Strengths                          |
| ------------------ | ---------------------------------- |
| Keyword Search     | Exact matches, fast, interpretable |
| Semantic Search    | Meaning-based, flexible            |
| Metadata Filtering | Strict control, access filtering   |

- Hybrid search **combines all three**.
- Allows **fine-tuning** for:
  - Domain-specific needs
  - Performance optimization
  - Retrieval quality

---

## 🔧 9. Customization Opportunities

- Adjust:
  - BM25 parameters
  - Metadata filter logic
  - RRF K value
  - β weighting
- Tailor the retriever to:
  - Your knowledge base
  - Your application’s goals

---

## 🧭 Final Takeaway

Hybrid search is the **most powerful and flexible retrieval strategy** in RAG.  
It blends:

- **Precision** from keyword search
- **Flexibility** from semantic search
- **Control** from metadata filtering

> “To do that tuning, however, you need a way to measure how well a retriever is performing. So join me in the next video to look at how retrievers are evaluated.” — Zain Hassan

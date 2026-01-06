## 🎥 Video: Keyword Search – BM25

**Instructor:** Zain Hassan  
**Duration:** ~4–5 minutes  
**Module:** 2 — Information Retrieval  
**Source:** [Coursera RAG Course](https://www.coursera.org/learn/retrieval-augmented-generation-rag/lecture/Nl9I6/keyword-search-bm25)

---

### 🧠 Introduction: Why BM25?

- TF‑IDF is a **classic keyword search algorithm**, but most production retrievers use **BM25** (Best Matching 25).
- BM25 is the **25th variant** in a family of scoring functions developed in the Okapi project.
- It improves on TF‑IDF by addressing two key issues:
  1. **Term frequency saturation**
  2. **Document length normalization**

---

### 📐 The BM25 Formula

The formula for a single keyword’s relevance score is:

\[
IDF \times \frac{TF \times (k_1 + 1)}{TF + k_1 \times \left(1 - b + b \times \frac{\text{document length}}{\text{average document length}}\right)}
\]

This is the **core BM25 function** for a single keyword in a document.

- **IDF** = Inverse Document Frequency (rarity of the term across the corpus)
- **TF** = Term Frequency (how many times the keyword appears in the document)
- **k₁** = saturation parameter (controls diminishing returns of repeated terms)
- **b** = normalization parameter (controls how strongly document length is penalized)
- **document length / average document length** = adjusts for long vs. short documents

The final document score is the **sum of this value across all query terms**.

---

### 🔍 Improvements Over TF‑IDF

1. **Term Frequency Saturation**

   - In TF‑IDF, if a word appears 20 times, it scores twice as much as 10 times.
   - BM25 **dampens this effect**: after a certain point, extra repetitions don’t add much.
   - Example: “pizza” appearing 20 times isn’t twice as relevant as 10 times.

2. **Document Length Normalization**

   - TF‑IDF penalizes long documents too aggressively.
   - BM25 applies a **diminishing penalty**: long docs are penalized, but not excessively.
   - This allows long but relevant documents to still rank highly.
   - This is called **document length normalization**.

3. **Tunable Hyperparameters**
   - \( k \) (commonly ~1.2–2.0): controls how quickly term frequency saturates.
   - \( b \) (commonly ~0.75): controls how strongly document length is normalized.
   - These can be tuned per dataset for optimal retrieval.

---

### 🧪 Example Walkthrough

Suppose we have 3 documents and the query is:

> “pizza oven”

- **Doc 1**: “How to make pizza in a wood-fired oven”
- **Doc 2**: “Pizza, pizza, pizza everywhere”
- **Doc 3**: “History of ovens in ancient Rome”

#### Step 1: Compute IDF

- `pizza` appears in 2/3 docs → IDF ≈ log(3/2) = 0.18
- `oven` appears in 2/3 docs → IDF ≈ 0.18

#### Step 2: Apply BM25 Formula

- **Doc 1**:

  - `pizza` freq = 1, `oven` freq = 1
  - Both terms present, moderate length → **high score**

- **Doc 2**:

  - `pizza` freq = 3, `oven` freq = 0
  - Term frequency saturates → not 3× better than Doc 1
  - Missing “oven” → lower score

- **Doc 3**:
  - `pizza` freq = 0, `oven` freq = 1
  - Only one keyword present → medium score

**Ranking outcome:**  
Doc 1 > Doc 2 > Doc 3

---

### ✅ Why BM25 Is the Standard

- **Better ranking** than TF‑IDF in practice.
- **Computationally efficient** (similar cost to TF‑IDF).
- **Tunable** for different domains.
- **Robust**: balances keyword frequency, rarity, and document length.
- **Widely adopted**: the default keyword search algorithm in most retrievers.

---

### ⚠️ Limitations

- Still depends on **exact keyword matches**.
- If a query uses synonyms (e.g., “flatbread” instead of “pizza”), BM25 won’t match unless the exact word appears.
- This is where **semantic search** complements BM25.

---

## 🧭 Final Takeaway

BM25 is the **gold standard for keyword-based retrieval** in RAG systems. It:

- Improves on TF‑IDF with **frequency saturation** and **length normalization**.
- Provides **tunable hyperparameters** for flexibility.
- Ensures retrieved documents contain the **exact keywords** from the user’s query.

But it still needs **semantic search** to handle synonyms and meaning-based matches.

## 🎥 Video: Semantic Search – Introduction

**Instructor:** Zain Hassan  
**Module:** 2 — Information Retrieval  
**Duration:** ~7 minutes  
**Source:** [Coursera RAG Course](https://www.coursera.org/learn/retrieval-augmented-generation-rag/lecture/i1O6p/semantic-search-introduction)

---

## 🧠 1. What Is Semantic Search?

- Semantic search matches documents to prompts based on **shared meaning**, not just shared words.
- It captures **nuances** that keyword search misses.

### Examples:

- Keyword search fails to match:
  - “happy” and “glad” → synonyms
  - “Python” (programming) vs. “Python” (snake) → ambiguous terms
- Semantic search understands **context and meaning**.

---

## 🔍 2. How Semantic Search Works (High-Level)

- Every **document** and **prompt** is mapped to a **vector**.
- These vectors are compared to generate **similarity scores**.
- Documents closest to the prompt vector are considered most relevant.

---

## 🧮 3. Keyword vs. Semantic Vectors

- **Keyword search**: vectors are based on **word counts**.
- **Semantic search**: vectors are generated using an **embedding model**.

---

## 🧠 4. What Is an Embedding Model?

- Embedding models map words (or texts) to **locations in space**, represented as vectors.
- Example:
  - `pizza` → [3, 1]
  - `bear` → [5, 2]
- These can be visualized as points on an x-y axis.

<img src="images/Vector Sapce.png" alt="Cosine Similarity" width="350"/>


## ✨ 5. Semantic Clustering (The “Magic”)

- Embedding models place **similar words near each other** in vector space.
  - `food` and `cuisine` → close together
  - `trombone` and `cat` → far apart
- Axes don’t have intuitive labels (no “food axis” or “animal axis”).
- Think of it as **floating points** where proximity = meaning.

---

## 🧭 6. High-Dimensional Embedding Space

- 2D or 3D space is too limited.
- Real embedding models use **hundreds or thousands of dimensions**.
- This allows:
  - Rich clustering
  - Nuanced relationships
- Though impossible to visualize, the math still applies:
  - Similar concepts → close vectors
  - Dissimilar concepts → distant vectors

![alt text](<images/Understand Embedding Models.png>)

---

## 🧾 7. Embedding Models for Different Inputs

- Embedding models exist for:
  - Individual words
  - Sentences
  - Entire documents
- Each input is mapped to a **single vector**.
- Similar vectors = similar meaning.

![alt text](<images/Embedding Models - Different Inputs.png>)

### Example:

- Sentences:
  - “He spoke softly in class.”
  - “He whispered quietly during class.”
  - “Her daughter brightened the gloomy day.”
- First two → close vectors
- Third → distant vector

![alt text](<images/Sentence Embedding Example.png>)

---

## 📏 8. Measuring Vector Similarity

### a) Euclidean Distance

- Measures **straight-line distance** between vectors.
- Based on **Pythagorean theorem**.
- Works in low dimensions, but less effective in high-dimensional space.

<img src="images/Euclidean Similarity.png" alt="Cosine Similarity" width="200"/>

### b) Cosine Similarity

- Measures **directional similarity**, not absolute distance.
- Example:
  - Vectors (10, 10) and (100, 100) → same direction, different magnitude.
- Range:
  - +1 → same direction
  - –1 → opposite direction
  - 0 → orthogonal (unrelated)

<img src="images/Cosine Similarity.png" alt="Cosine Similarity" width="200"/>

### c) Dot Product

- Measures **projection** of one vector onto another.
- Larger projection = more similar.
- Negative projection = opposite meaning.

<img src="images/Dot Product.png" alt="Cosine Similarity" width="200"/>

## 🧮 9. Summary of Similarity Metrics

| Metric             | Measures              | Range    | Notes                          |
| ------------------ | --------------------- | -------- | ------------------------------ |
| Euclidean Distance | Absolute distance     | ≥ 0      | Less useful in high dimensions |
| Cosine Similarity  | Directional alignment | –1 to +1 | Most common in semantic search |
| Dot Product        | Projection length     | –∞ to +∞ | Sensitive to magnitude & angle |

---

## 🧪 10. Semantic Search Pipeline

1. **Embed all documents** using the embedding model.
2. **Embed the prompt** into the same vector space.
3. **Compare vectors** using cosine similarity or dot product.
4. **Rank documents** by similarity score.
5. **Return top-ranked documents** as most relevant.

> “Thanks to the way the embedding model works, you’ve just found the documents with the most similar meaning to your prompt.” — Zain Hassan

![alt text](<images/Semantic Search.png>)

---

## ✅ 11. Strengths of Semantic Search

- Matches **meaning**, not just words.
- Handles:
  - Synonyms
  - Paraphrasing
  - Contextual ambiguity
- Especially powerful for:
  - Natural language queries
  - Broad or vague prompts

---

## ⚠️ 12. Assumption: Embedding Model Quality

- Semantic search **depends heavily** on the quality of the embedding model.
- If the model is well-trained:
  - Similar concepts → close vectors
- If poorly trained:
  - Semantic search fails

---

## 🧭 13. Transition to Next Topic

- The next video dives deeper into **how embedding models are trained**.
- Understanding this helps explain **why semantic search works so well**.

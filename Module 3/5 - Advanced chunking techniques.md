## 🎥 Video: Module 3 — Advanced Chunking Techniques  
**Instructor:** Zain Hassan  
**Video Duration:** ~5 minutes  
**Source:** [Coursera Video](https://www.coursera.org/learn/retrieval-augmented-generation-rag/lecture/pdpd9/advanced-chunking-techniques)

---

## 🧠 1. Motivation for Advanced Chunking

- Chunking improves retrieval, but **naive chunking risks losing context**.
- Example:  
  > “That night she dreamed, as she did often, that she was finally an Olympic champion.”  
  - A poorly placed split could misrepresent the meaning — making it seem like she **is** a champion, not dreaming of it.

- Fixed-size and recursive splitting **don’t protect against semantic distortion**.

---

## 🧠 2. Semantic Chunking

### 🔍 How It Works:
- Traverse the document **sentence by sentence**.
- For each sentence:
  - Compare its **vector** to the current chunk’s vector.
  - If **distance < threshold**, add to current chunk.
  - If **distance ≥ threshold**, start a new chunk.

![alt text](<Ungraded Lab: Chunking/images/semantic chunking.png>)

### 📊 Visualization:
- A graph shows:
  - **Red line** = dissimilarity threshold
  - **Peak line** = semantic gap between current chunk and next sentence
  - When peak crosses red line → new chunk begins

### ✅ Benefits:
- Chunks follow **train of thought**.
- Handles:
  - Conceptual tangents
  - Ideas spanning multiple paragraphs
- Smarter chunk boundaries
- Higher recall and presicion

### ⚠️ Tradeoff:
- **Computationally expensive**:
  - Requires vectorizing every sentence and repeatedly calculating vectors for every sentence in your knowledge base.
  - Repeated comparisons


---

## 🤖 3. LLM-Based Chunking

### 🧠 How It Works:
- Pass document to a **language model** with instructions:
  - Group similar concepts
  - Split when topics change

### 🧩 Output:
- LLM generates chunks like it generates any other text.

### ✅ Benefits:
- High performance
- Flexible and adaptive

### ⚠️ Tradeoff:
- **Black-box behavior**
- **Costly**, but becoming more viable as LLM prices drop

---

## 🧠 4. Context-Aware Chunking

### 🧠 How It Works:
- Ask LLM to:
  - Create chunks
  - Add **summary text** explaining each chunk’s context

### 📌 Example:
- A blog post ends with a list of names.
- LLM adds:  
  > “This chunk contains acknowledgments from the author.”

### ✅ Benefits:
- Improves:
  - **Vectorization** (semantic clarity)
  - **Retrieval relevance**
  - **LLM generation quality**

### ⚠️ Tradeoff:
- Requires **LLM preprocessing** for every chunk
- **No impact on search speed**, but **high upfront cost**

---

## 🧪 5. When to Use What

| Technique               | Pros                                  | Cons                                  | Use Case                            |
|------------------------|----------------------------------------|---------------------------------------|-------------------------------------|
| Fixed-size / Recursive | Simple, fast, good for prototyping     | May split meaning                    | Default starting point              |
| Semantic Chunking      | Meaning-aware, improves retrieval      | Expensive, tuning required           | When precision matters              |
| LLM-Based Chunking     | Flexible, high performance             | Black-box, costly                    | When budget allows                  |
| Context-Aware Chunking | Enhances both retrieval & generation   | Preprocessing cost                   | First upgrade beyond fixed-size     |

---

## 🎯 Final Takeaway

> “The goal isn’t to implement the most cutting-edge chunking technique. It’s to understand what options are available, how suitable they are to your data, and whether the costs and benefits make it worth implementing in your system.” — Zain Hassan
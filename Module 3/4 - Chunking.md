## 🎥 Video: Module 3 — Chunking

**Instructor:** Zain Hassan
**Video Duration:** ~6 minutes
**Source:** [Coursera Chunking Lecture](https://www.coursera.org/learn/retrieval-augmented-generation-rag/lecture/AvkDR/chunking)

---

## 🧠 1. Why Chunking Matters in RAG

- Vector databases are optimized for retrieval, but **production RAG systems** require additional adaptations.
- One of the most important is **chunking**.

> “Chunking is the practice of breaking longer text documents from your knowledge base into smaller text chunks.”

---

## 🎯 2. Three Reasons to Chunk

1. **Embedding model token limits**: Most models can only embed a limited number of tokens.
2. **Improved search relevance**: Smaller chunks yield more precise matches.
3. **Efficient LLM input**: Only the most relevant text is passed to the LLM, conserving context window space.

![alt text](images/chunking.png)

---

## 📚 3. The Problem with Large Chunks

- Imagine a knowledge base of **1,000 books**.
- If each book is embedded as a single vector:
  - You compress the meaning of an entire book into one vector.
  - This **averages out** all topics and loses specificity.
  - Can't sharply represent specific topics, chapters, or pages.
  - Creates "avaraged" representation across all content.
  - Results in poor search relevance
  - Retrieves entire books, quickly filling LLM context window
  - Retrieval becomes **blurry and imprecise**.

> “You’d be retrieving an entire book at a time, which would quickly fill up your LLM’s context window.”

---

## ✂️ 4. Chunking by Granularity

- Instead of embedding whole books, chunk into:
  - Pages
  - Paragraphs
  - Sentences
- This transforms 1,000 books into **1 million paragraphs** — and vector databases can handle that scale.

---

## ⚖️ 5. Choosing the Right Chunk Size

- **Too big** (e.g., chapters):
  - Still too broad
  - Fills LLM context window
- **Too small** (e.g., words or single sentences):
  - Loses surrounding context
  - Reduces search relevance

> “There’s no one-size-fits-all approach to chunk size.”

![alt text](<images/choose the right chunk size.png>)

---

## 📏 6. Fixed-Size Chunking

- Define a fixed number of characters per chunk (e.g., 250).
- Example:
  - Chunk 1: characters 1–250
  - Chunk 2: 251–500
  - Chunk 3: 501–750

![alt text](<images/fixed size chunk.png>)

### 🧩 Problem:

- Splits may occur mid-word or mid-thought.

---

## 🔁 7. Overlapping Chunks

- Solution: **Allow overlaps** between chunks.
- Example:
  - Chunk 1: 1–250
  - Chunk 2: 226–475
  - Chunk 3: 451–700
- Overlap = 25 characters (10% of chunk size)

> “Overlapping chunks minimizes instances where words are cut off from their context.”

- **Pros**:
  - Preserves context at chunk boundaries
  - Improves search relevance
- **Cons**:
  - Adds redundant vectors
  - Increases storage and compute

![alt text](<images/overlap chunks.png>)

---

## 🔄 8. Recursive Character Text Splitting

- A **dynamic** chunking strategy.
- Split on specific characters (e.g., newline `\n`).
- Produces **variable-sized chunks** based on document structure.

> “You’re accounting for the document structure and increasing the chances that related concepts are kept together.”

- Examples:
  - HTML → split on `<p>` or `<h1>` tags
  - Python → split on function definitions
  - Text → split on newlines

![alt text](<images/Recursive Character Text Splitting.png>)

---

## 🧰 9. Tools and Metadata

- You can implement chunking manually or use **external libraries**.
- If documents have metadata:
  - Ensure each chunk **inherits** metadata from its source.
  - Optionally add **chunk position info**.

---

## ✅ 10. Best Practices and Starting Point

- Start with:
  - **Fixed-size chunks** of ~500 characters
  - **Overlap** of 50–100 characters
- Adjust based on:
  - Document type
  - Embedding model
  - Retrieval performance

> “Chunking your documents has a variety of benefits for vector retrieval, from increasing search relevancy to minimizing the use of your LLM’s context window.”

---

## 🔜 11. What’s Next

- More advanced chunking techniques will be covered in the next video.

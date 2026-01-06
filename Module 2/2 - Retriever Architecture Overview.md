## 🎥 Video: Retriever Architecture Overview

**Instructor:** Zain Hassan  
**Duration:** ~3 minutes  
**Module:** 2 — Information Retrieval  
**Source:** [Coursera RAG Course](https://www.coursera.org/learn/retrieval-augmented-generation-rag/lecture/j1Dc1/retriever-architecture-overview)

---

### 🧠 Purpose of the Video

Zain introduces a **mental model** for understanding how retrievers work within a RAG system. This sets the foundation for deeper dives into search techniques like metadata filtering, keyword search, and semantic search.

---

## 🏗️ High-Level Retriever Architecture

When a RAG system receives a user prompt, the following steps occur:

1. **Prompt Routing**

   - The prompt is first sent to the **retriever**, not directly to the LLM.

2. **Knowledge Base Access**

   - The retriever queries a **knowledge base**—typically a collection of text files or documents stored in a database.

3. **Document Selection**

   - The retriever must **quickly and accurately** decide which documents are most relevant to the prompt.

4. **Document Return**
   - These selected documents are then passed to the LLM to be included in the **augmented prompt**.

![alt text](<images/Retriever architecture overview.png>)

---

## 🔍 Dual Search Techniques

Modern retrievers use **two complementary search methods**:
![alt text](<images/Search Techniques.png>)

### 1. 🔤 Keyword Search

- Matches documents that contain **exact words** from the prompt.
- Time-tested and reliable.
- Useful for precision and exact phrase matching.

### 2. 🧠 Semantic Search

- Matches documents based on **meaning**, not just word overlap.
- Uses embeddings to find conceptually similar content.
- More flexible—can retrieve relevant documents even if they don’t contain the exact words.

> Each technique returns a list of ~20–50 documents. There’s often overlap, but rankings differ due to the nature of each method.

![alt text](<images/Search Techniques-1.png>)

## 🗂️ Metadata Filtering

After initial retrieval:

- Each list (keyword and semantic) is **filtered based on metadata**.
- Example:
  - Engineering team sees technical docs.
  - HR team sees policy docs.
- The system uses user profile or context to **exclude irrelevant documents**.

> This step ensures personalization and relevance based on user role or department.

---

## 🔗 Hybrid Search

Once filtering is complete:

- The retriever **combines both lists** into a **final ranked list**.
- Top-ranked documents are selected and passed to the LLM.

### Benefits of Hybrid Search:

| Technique       | Strengths                               |
| --------------- | --------------------------------------- |
| Keyword Search  | High precision, exact match sensitivity |
| Semantic Search | Flexibility, meaning-based relevance    |
| Metadata Filter | Rigid exclusion based on user context   |

> “Designing a high-performing retriever means understanding the relative strengths of each of these techniques and tuning the balance between them.” — Zain Hassan

![alt text](<images/Hybrid Search.png>)

---

## 🧭 Final Takeaway

This video emphasizes that retrievers are **multi-layered systems**. They:

- Interpret queries.
- Search using multiple strategies.
- Filter based on metadata.
- Combine results for optimal relevance.

The next videos in the module will explore each technique—starting with **metadata filtering**—in greater depth.

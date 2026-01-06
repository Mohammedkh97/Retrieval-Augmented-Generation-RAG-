## 🎥 Video: Introduction to Retrieval-Augmented Generation (RAG)

**Instructor:** Zain Hassan 
**Duration:** ~5 minutes  
**Module:** 1 — RAG Overview  
**Source:** [Coursera RAG Course](https://www.coursera.org/learn/retrieval-augmented-generation-rag/lecture/ob14T/introduction-to-rag)

---

### 🧠 What Is RAG?

- **RAG = Retrieval + Generation**
  - It’s a method that improves LLM responses by retrieving relevant external information before generating an answer.
  - This allows LLMs to go beyond their training data and respond with **grounded, accurate, and up-to-date** information.

---

### 🧪 Real-World Analogy (Used by Zain Hassan)

Zain walks through three questions to illustrate how humans—and RAG systems—handle information:

1. **General Knowledge Question**  
   _“Why are hotels expensive on weekends?”_  
   → You answer from prior knowledge: more demand, higher prices.

2. **Context-Specific Question**  
   _“Why are hotels in Vancouver expensive this weekend?”_  
   → You need to **retrieve** current info (e.g., Taylor Swift concert).

3. **Deep Research Question**  
   _“Why doesn’t Vancouver have more hotel capacity downtown?”_  
   → Requires **specialized knowledge** like urban planning history.

This mirrors the RAG process:

- **Retrieval phase** relevant data.
- **Generation phase** a response using that data.

---

### 🧰 Why LLMs Need RAG

- LLMs are trained on massive datasets, but they can’t know everything—especially::
  - They **don’t know recent events**.
  - They **lack access to private or proprietary data**.
  - They **struggle with niche domains** (e.g., legal, medical, enterprise).

> “It’s unreasonable to expect LLMs to be experts on every topic.” — Zain Hassan

RAG solves this by **injecting relevant context** into the prompt before generation.

---

### 🔧 How RAG Works

- A **retriever** searches a knowledge base for relevant chunks of information.
- The system **augments the user’s prompt** with this retrieved data.
- The LLM then generates a response using both the original query and the added context.

### 🧱 RAG System Architecture

- **Retriever**

  - Searches a knowledge base (e.g., vector DB, documents) for relevant chunks.
  - Can be tuned for semantic search, keyword matching, or hybrid methods.
  - The retriever manages a knowledge base of trusted, relevant, and possibly private information.
  - When the RAG system receives a prompt, the retriever finds and retrieves the most relevant information from the knowledge base to share with the LLM. 
  - The model then uses that retrieved information when it responds to the prompt. 


- **LLM (Generator)**

  - Receives an **augmented prompt**: original query + retrieved context.
  - Generates a response that’s more accurate and grounded.

- **Knowledge Base**
  - Can be public, private, or domain-specific.
  - Examples: internal company docs, medical literature, legal databases.

---

### 🔑 Key Insight

> “Just put it in the prompt.”  
> That’s the essence of RAG: enrich the prompt with retrieved data so the LLM can reason effectively.

> “RAG improves the way LLMs generate text by first retrieving relevant information from a knowledge base.”

## It’s a simple but powerful idea: don’t just ask the model—give it what it needs to know first.

### 💡 Why This Matters for You

As someone building NLP pipelines and preparing for MBZUAI, this video lays the groundwork for:

- **Designing retrieval strategies** (e.g., chunking, indexing).
- **Integrating LLMs with custom datasets**.
- **Building scalable, production-grade RAG systems**.

---

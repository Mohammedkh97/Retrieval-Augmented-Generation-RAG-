## 🎥 Video: Module 3 — Vector Databases  
**Instructor:** Zain Hassan  
**Video Duration:** ~5 minutes  
**Source:** [Coursera Vector Databases Lecture](https://www.coursera.org/learn/retrieval-augmented-generation-rag/lecture/Qp1kF/vector-databases)

---

## 🧠 1. What Is a Vector Database?

- In a **production RAG system**, vectors are stored and retrieved from a **specialized database** called a **vector database**.
- These databases are **built from the ground up** to handle:
  - **High-dimensional vector data**
  - **Vector-oriented algorithms** like **Approximate Nearest Neighbors (ANN)**

---

## 📈 2. Why Vector Databases Emerged

- Became popular in the **early 2020s** due to:
  - Rise of **large language models**
  - Explosion of **embedding-based techniques** like **semantic search**
- Traditional relational databases:
  - Performed **poorly** at semantic search
  - Were closer in performance to **inefficient KNN algorithms**

---

## ⚡ 3. What Vector Databases Optimize

- Tasks like:
  - Building **proximity graphs** (e.g., for HNSW)
  - Computing **vector distances**
- Result: They **scale well** and operate **much faster** in vector-based applications — especially in **RAG systems**

---

## 🛠️ 4. The Tool Used in This Course: Weaviate

- **Weaviate** is the vector database used in this course.
- It’s:
  - **Open-source**
  - Can run **locally or in the cloud**
- Other vector databases exist and offer **similar functionality**.

---

## 🔄 5. Workflow Overview

To prepare a vector database for search, you must:

1. **Set up the database**
2. **Load your documents**
3. Create:
   - **Sparse vectors** for **keyword search**
   - **Dense embedding vectors** for **semantic search**
4. **Create the index** for ANN search (e.g., HNSW index)

Once done, you’re ready to run actual searches.

---

## 🧪 6. Example: Using Weaviate

### a) Create or Connect to a Database
- You can either:
  - Create a new instance
  - Connect to an existing one

### b) Create a Collection
- Example: A collection named `article` to hold news articles.
- You define:
  - Fields like `title` and `body`
  - Data types (e.g., text)
  - **Embedding model** or **vectorizer** to generate semantic vectors

---

## 📥 7. Inserting Data

- Use `batch.addObject()` to insert data.
- It:
  - Adds objects to the collection
  - Tracks errors
  - Allows error handling (e.g., breaking loop if too many errors)

---

## 🔍 8. Running Searches

### a) Vector Search
- Specify:
  - Collection name
  - Text query
  - Metadata request (e.g., return **distance** between query and object vectors)

### b) Keyword Search
- Weaviate auto-generates an **inverted index**.
- You can run **BM25 queries** (learned in Module 2).
- Example: Request top 3 documents ranked by BM25.

### c) Hybrid Search
- Combines **vector** and **keyword** search.
- Uses an **alpha parameter** to balance scores:
  - `alpha = 0.25` → 25% vector search, 75% keyword search
- Results are **re-ranked** and top-k returned.

---

## 🧱 9. Applying Filters

- You can apply filters to properties:
  - Example: Filter by a specific field value
  - If it matches → object is returned
  - If not → object is excluded

---

## 🔁 10. Full Loop Summary

1. Configure the database
2. Load and index your data
3. Write a query (can include hybrid search and filters)

![alt text](images/workflow.png)

> “That’s a good overview of how to use a vector database.” — Zain Hassan
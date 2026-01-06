
## 🎥 Video: Keyword Search – TF-IDF  
**Instructor:** Zain Hassan  
**Duration:** ~7 minutes  
**Module:** 2 — Information Retrieval  
**Source:** [Coursera RAG Course](https://www.coursera.org/learn/retrieval-augmented-generation-rag/lecture/MYS0a/keyword-search-tf-idf)

---

## 🧠 What Is Keyword Search and Why Keyword Search Still Matters?

- Keyword search is a **foundational retrieval technique** used in databases and search engines for decades.
- It retrieves documents based on **shared words** between the prompt and the documents.
- The core assumption:  
  > “Documents that contain more words from the prompt are more likely to be relevant.”

---

## 🧮 Bag-of-Words Representation

- Both the prompt and each document are treated as a **bag of words**:
  - Word order is ignored.
  - Only word frequency matters.

### Example:
> “Making pizza without a pizza oven”  
- Word counts:  
  - `pizza`: 2  
  - `making`, `without`, `a`, `oven`: 1 each

- These counts are stored in a **sparse vector**:
  - Each position corresponds to a word in the vocabulary.
  - Most positions are zero → hence “sparse.”

---

## 🗃️ Term-Document Matrix & Inverted Index

- A **sparse vector** is generated for each document.
- These vectors are arranged into a **term-document matrix**:
  - Rows = words  
  - Columns = documents

![alt text](<images/sparse vectors.png>)

- This matrix is also called an **inverted index**:
  - You start from a word and find all documents that contain it.
  - Opposite of traditional indexing (document → words).

![alt text](<images/Inverted matrix.png>)

---

## ⚙️ Scoring Documents (Basic Keyword Match)

- When a prompt is submitted:
  - A sparse vector is generated for the prompt.
  - Each keyword is matched against the matrix.

### Scoring Logic:
- For each keyword:
  - Find its row in the matrix.
  - Award 1 point to every document that contains it.
- Total score = sum of keyword matches.
- Documents are ranked by score.

### Limitation:
- Doesn’t account for **multiple occurrences** of a keyword.

---

## 🔁 Frequency-Based Scoring

- To improve relevance:
  - Score is increased for **each occurrence** of a keyword.
  - Not just the first match.

### Problem:
- **Longer documents** naturally contain more keywords.
- This can **inflate scores unfairly**.

---

## 📏 Normalization by Document Length

- To correct for document length bias:
  - Divide each document’s score by its total word count.
  - This produces a **normalized score**:
    - Rewards documents where keywords are a **larger share** of the text.
    - Penalizes long documents with diluted relevance.

---

## 📉 Weighting by Rarity – Inverse Document Frequency (IDF)

- Not all keywords are equally informative:
  - Common words (e.g., “the”, “a”) appear in many documents.
  - Rare words (e.g., “pizza”, “oven”) are more meaningful.

### IDF Calculation:
- For each word:
  - Count how many documents it appears in.
  - Divide by total number of documents → Document Frequency (DF)
  - Invert the fraction → Inverse Document Frequency (IDF)

### Example:
- `pizza` in 5 out of 100 docs → DF = 0.05 → IDF = 20  
- `the` in all 100 docs → DF = 1 → IDF = 1

> Rare words get higher IDF scores → more weight in retrieval.

---

## 📉 Log-Scaled IDF

- Raw IDF values can **overweight rare words**.
- To soften this:
  - Use **logarithmic scaling**:
    - Still favors rare words, but less aggressively.

---

## 🧮 TF-IDF Matrix Construction

- Multiply each word’s frequency in a document by its IDF score.
- This produces the **TF-IDF matrix**:
  - Rows = words  
  - Columns = documents  
  - Values = TF × IDF

### Retrieval Logic:
- For each keyword in the prompt:
  - Traverse its row in the TF-IDF matrix.
  - Award each document the corresponding TF-IDF score.

---

## 🧠 TF-IDF Scoring Breakdown

The screen illustrates the **step-by-step transformation** from raw word counts to final TF-IDF scores using a term-document matrix. Here's how it unfolds:

---

### 🔹 Step 1: Build the Term-Document Matrix

Each document is represented as a **sparse vector** of word counts (term frequency). For example:

| Word     | Doc 1 | Doc 2 | Doc 3 |
|----------|-------|-------|-------|
| pizza    | 3     | 0     | 1     |
| oven     | 1     | 0     | 1     |
| the      | 5     | 4     | 6     |

This is the **raw term frequency (TF)** matrix.

---

### 🔹 Step 2: Compute Inverse Document Frequency (IDF)

For each word, calculate:

\[
\text{IDF}(w) = \log\left(\frac{N}{\text{DF}(w)}\right)
\]

Where:
- \( N \) = total number of documents
- \( \text{DF}(w) \) = number of documents containing word \( w \)

Example:
- `pizza` appears in 2 of 3 docs → IDF = log(3/2) ≈ 0.18
- `the` appears in all 3 docs → IDF = log(3/3) = 0

---

### 🔹 Step 3: Multiply TF × IDF

Each cell in the matrix is updated:

\[
\text{TF-IDF}_{i,j} = \text{TF}_{i,j} \times \text{IDF}_i
\]

Example for `pizza`:
- Doc 1: 3 × 0.18 = 0.54  
- Doc 3: 1 × 0.18 = 0.18

Now the matrix reflects **weighted importance** of each word in each document.

---

### 🔹 Step 4: Score Documents for a Prompt

Prompt:  
> “How to make pizza in an oven”

Extract keywords: `pizza`, `oven`, `make`

- For each keyword:
  - Look up its row in the TF-IDF matrix.
  - Sum the scores across documents.

Example scoring:
- Doc 1: pizza (0.54) + oven (0.2) + make (0.1) = **0.84**
- Doc 3: pizza (0.18) + oven (0.2) + make (0) = **0.38**
- Doc 2: all zeros = **0**

→ **Doc 1 is ranked highest**.

---

## ✅ Why This Matters in RAG

- TF-IDF helps **rank documents** by how well they match the prompt.
- It **boosts rare, meaningful words** and **downweights common ones**.
- It’s fast, interpretable, and a strong baseline for hybrid retrievers.

---

## 🧪 Why TF-IDF Is a Strong Baseline

- TF-IDF balances:
  - **Term frequency** (how often a word appears)
  - **Inverse document frequency** (how rare the word is)

- Documents that:
  - Use keywords frequently  
  - Use **rare** keywords  
→ Score higher and are more likely to be relevant.

---

## 🔄 Transition to BM25

- TF-IDF is foundational, but modern systems often use **BM25**:
  - A refined version that improves ranking behavior.
  - Handles term saturation and document length more robustly.

> “Join me in the next video to learn how BM25 works and how keyword search fits into your RAG system.” — Zain Hassan

---

## 🧭 Final Takeaway

TF-IDF is a **cornerstone of keyword-based retrieval**. It’s:
- Simple to implement
- Fast to compute
- Effective in many domains

But it’s best used as part of a **hybrid retriever**, alongside semantic search and metadata filtering, to maximize relevance and robustness in RAG systems.

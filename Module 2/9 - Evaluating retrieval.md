

## 🎥 Video: Evaluating Retriever Quality  
**Instructor:** Zain Hassan  
**Module:** 2 — Information Retrieval  
**Video Title:** Evaluating Retriever Quality  
**Duration:** ~8 minutes  
**Source:** [Coursera RAG Course](https://www.coursera.org/learn/retrieval-augmented-generation-rag/lecture/RKASW/evaluating-retrieval)

---

## 🧠 1. Why Evaluate a Retriever?

- Like any software component, a retriever must be **evaluated** to ensure it’s functioning correctly.
- You can measure:
  - Latency
  - Throughput
  - Resource usage
- But the **most important metric** is **search quality**:
  > “Is the retriever finding relevant documents?”

---

## 🧪 2. Ingredients for Evaluation

To evaluate retrieval quality, you need:

1. **Prompt**  
   - Different prompts yield different performance.
   - Evaluation must be prompt-specific.

2. **Ranked List of Retrieved Documents**  
   - What the retriever returns for the prompt.

3. **Ground Truth List**  
   - The correct set of relevant documents in the knowledge base.
   - Often manually labeled or annotated.

> Without ground truth, you can’t measure retrieval accuracy.

---

## 📊 3. Precision and Recall

### a) Precision  
\[
\text{Precision} = \frac{\text{Relevant Retrieved}}{\text{Total Retrieved}}
\]  
- Measures **trustworthiness** of results.
- Penalizes irrelevant documents.

Precision provides an evaluation of the relevancy of the retrieved documents. It's calculated as the ratio of true positives (relevant documents retrieved) to the total number of documents retrieved (all retrieved documents, including false positives).

$$\text{Precision} = \frac{\text{True Positives (TP)}}{\text{True Positives (TP)} + \text{False Positives (FP)}}$$

### b) Recall  
\[
\text{Recall} = \frac{\text{Relevant Retrieved}}{\text{Total Relevant in KB}}
\]  
- Measures **completeness**.
- Penalizes missing relevant documents.


Recall evaluates the model's ability to retrieve all relevant documents from the dataset. It's calculated as the ratio of true positives to the total number of actual relevant documents (true positives plus false negatives).

$$\text{Recall} = \frac{\text{True Positives (TP)}}{\text{True Positives (TP)} + \text{False Negatives (FN)}}$$

--- 

<div style="text-align: center;">
  <img src="images/precision_recall.png" alt="Description" style="width: 70%;">
</div>

---

### 🧮 Example:

- Knowledge base has **10 relevant documents**.
- Retriever returns **12 documents**, **8 are relevant**.

→ Precision = 8 / 12 = **66%**  
→ Recall = 8 / 10 = **80%**

- Second run: returns **15 documents**, **9 are relevant**.

→ Precision = 9 / 15 = **60%**  
→ Recall = 9 / 10 = **90%**

> You traded **some precision** for **higher recall**.

---

## 📐 4. Precision and Recall at K

- Retrieval metrics depend on how many documents are returned.
- So we standardize using **top-K metrics**.

### Example:

- Top 5 documents → 2 are relevant → Precision@5 = 2 / 5 = **40%**
- Top 10 documents → 6 are relevant → Precision@10 = 6 / 10 = **60%**
- Knowledge base has 8 relevant docs → Recall@10 = 6 / 8 = **75%**

> You can compute metrics at top 1, top 2, top 5, top 15, etc.

---

## 📈 5. Mean Average Precision (MAP)

- MAP rewards **ranking relevant documents highly**.

### Step-by-step:

1. List top-K retrieved documents.
2. Compute **Precision@K** for each row.
3. Add up precision values **only for relevant documents**.
4. Divide by number of relevant documents retrieved in top-K.

### Example:

- Top 6 docs → relevant at ranks 1, 4, 5
- Precision@1 = 1.0  
- Precision@4 = 0.5  
- Precision@5 = 0.6

→ Average Precision@6 = (1 + 0.5 + 0.6) / 3 = **0.7**

- MAP = average of **average precision** across many prompts.

> MAP drops if irrelevant docs are ranked above relevant ones.

---

## 🔁 6. Mean Reciprocal Rank (MRR)

- Measures **how early** the first relevant document appears.

### Formula:
\[
\text{Reciprocal Rank} = \frac{1}{\text{Rank of First Relevant Doc}}
\]

### Example:

- First relevant doc at rank 2 → RR = 1/2 = **0.5**
- At rank 4 → RR = 1/4 = **0.25**

- MRR = average RR across multiple prompts.

### Example:

- First relevant doc at ranks: 1, 3, 6, 2  
→ RR = 1, 1/3, 1/6, 1/2  
→ MRR = (1 + 0.333 + 0.167 + 0.5) / 4 = **0.5**

> MRR emphasizes **early relevance**.

---

## 🧭 7. Choosing the Right Metrics

| Metric | Measures | Use Case |
|--------|----------|----------|
| Recall@K | Completeness | Most foundational |
| Precision@K | Trustworthiness | Penalizes irrelevant docs |
| MAP@K | Ranking quality | Rewards high placement of relevant docs |
| MRR | First hit position | Specialized for early relevance |

> Use metrics to evaluate retriever performance and guide tuning.

---

## ⚠️ 8. Ground Truth Dependency

- All metrics depend on having **ground truth labels**.
- Requires manually marking relevant documents for sample prompts.
- Time-consuming but essential for:
  - Development
  - Monitoring in production

---

## 🧭 Final Takeaway

- Evaluating retrieval is critical to building a high-quality RAG system.
- Use metrics like **Recall**, **Precision**, **MAP**, and **MRR** to:
  - Measure performance
  - Tune hybrid search weights
  - Monitor production behavior

> “Join me in the next video and let’s summarize the main takeaways from this module.” — Zain Hassan

"""
Complete RAG System with TF-IDF, BM25, and Metadata Filtering
Real-world pizza recipe knowledge base example
"""

import math
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Tuple

# ============================================================================
# PART 1: DOCUMENT & METADATA SETUP
# ============================================================================

@dataclass
class Document:
    id: int
    title: str
    content: str
    metadata: Dict

# Sample knowledge base
documents = [
    Document(
        id=1,
        title="How to Make Pizza in a Wood-Fired Oven",
        content="""Learn how to make authentic pizza in a wood-fired oven. 
        Start with quality dough, add tomato sauce, fresh mozzarella cheese, 
        and basil. The oven should reach high temperature. Pizza cooks quickly 
        in wood-fired ovens. The crispy crust and melted cheese make it delicious.""",
        metadata={
            "author": "Chef Maria",
            "date": "2024-01-15",
            "category": "Recipe",
            "region": "UAE",
            "access_level": "public",
            "tags": ["pizza", "cooking", "oven"]
        }
    ),
    Document(
        id=2,
        title="Pizza Business Opportunities in Dubai",
        content="""Dubai's pizza market is growing rapidly. Pizza restaurants 
        are expanding across the emirate. Pizza franchise opportunities exist for 
        entrepreneurs. The pizza industry generates significant revenue. Pizza lovers 
        in Dubai have diverse preferences. Pizza delivery services are popular.""",
        metadata={
            "author": "Business Analyst",
            "date": "2024-03-20",
            "category": "Business",
            "region": "UAE",
            "access_level": "premium",
            "tags": ["pizza", "business", "dubai"]
        }
    ),
    Document(
        id=3,
        title="Traditional Italian Pizza History",
        content="""Pizza originated in Naples, Italy centuries ago. 
        Traditional pizza recipes use simple ingredients. Wood-fired ovens 
        are essential for authentic pizza. Italian pizza culture is UNESCO protected. 
        Pizza is a global phenomenon. Every region in Italy has unique pizza styles.""",
        metadata={
            "author": "Food Historian",
            "date": "2024-02-10",
            "category": "Culture",
            "region": "Italy",
            "access_level": "public",
            "tags": ["pizza", "italy", "history"]
        }
    ),
    Document(
        id=4,
        title="Simple Pizza Dough Recipe",
        content="""Making pizza dough is straightforward. Mix flour and water with salt. 
        Add yeast for fermentation. Knead the dough thoroughly. Let it rise for hours. 
        The dough should be elastic and smooth. Perfect dough creates perfect pizza. 
        Dough quality determines pizza quality.""",
        metadata={
            "author": "Chef Marco",
            "date": "2024-04-05",
            "category": "Recipe",
            "region": "UAE",
            "access_level": "public",
            "tags": ["pizza", "dough", "recipe"]
        }
    )
]

# ============================================================================
# PART 2: TEXT PREPROCESSING
# ============================================================================

def preprocess_text(text: str) -> List[str]:
    """Convert text to lowercase and split into words, remove short words"""
    words = text.lower().split()
    # Remove punctuation and filter short words
    words = [w.strip('.,!?;:') for w in words if len(w) > 2]
    return words

def build_vocab_and_idf(documents: List[Document]) -> Tuple[Dict, Dict]:
    """Build vocabulary and calculate IDF for all documents"""
    vocab = set()
    doc_frequencies = defaultdict(int)
    
    for doc in documents:
        words = set(preprocess_text(doc.content))
        vocab.update(words)
        for word in words:
            doc_frequencies[word] += 1
    
    # Calculate IDF
    idf = {}
    total_docs = len(documents)
    for word in vocab:
        idf[word] = math.log(total_docs / doc_frequencies[word])
    
    return vocab, idf

# ============================================================================
# PART 3: TF-IDF IMPLEMENTATION
# ============================================================================

class TFIDFRetriever:
    """Traditional TF-IDF keyword search"""
    
    def __init__(self, documents: List[Document]):
        self.documents = documents
        self.vocab, self.idf = build_vocab_and_idf(documents)
        self.doc_vectors = self._build_tfidf_vectors()
    
    def _build_tfidf_vectors(self) -> Dict[int, Dict]:
        """Build TF-IDF vectors for all documents"""
        vectors = {}
        for doc in self.documents:
            words = preprocess_text(doc.content)
            tf = defaultdict(int)
            
            for word in words:
                tf[word] += 1
            
            # Normalize TF by document length
            doc_length = len(words)
            tfidf_vec = {}
            for word, count in tf.items():
                normalized_tf = count / doc_length if doc_length > 0 else 0
                tfidf_vec[word] = normalized_tf * self.idf[word]
            
            vectors[doc.id] = tfidf_vec
        
        return vectors
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[Document, float]]:
        """Retrieve documents using TF-IDF scoring"""
        query_words = preprocess_text(query)
        scores = defaultdict(float)
        
        for word in query_words:
            if word in self.idf:
                for doc_id, tfidf_vec in self.doc_vectors.items():
                    if word in tfidf_vec:
                        scores[doc_id] += tfidf_vec[word]
        
        # Sort and return top-k
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        results = [(self._get_doc(doc_id), score) for doc_id, score in ranked]
        
        return results
    
    def _get_doc(self, doc_id: int) -> Document:
        return next(d for d in self.documents if d.id == doc_id)

# ============================================================================
# PART 4: BM25 IMPLEMENTATION
# ============================================================================

class BM25Retriever:
    """BM25 keyword search with saturation and length normalization"""
    
    def __init__(self, documents: List[Document], k1: float = 1.5, b: float = 0.75):
        self.documents = documents
        self.k1 = k1  # Saturation parameter
        self.b = b    # Length normalization parameter
        self.vocab, self.idf = build_vocab_and_idf(documents)
        
        # Calculate average document length
        self.doc_lengths = {}
        total_length = 0
        for doc in documents:
            words = preprocess_text(doc.content)
            self.doc_lengths[doc.id] = len(words)
            total_length += len(words)
        
        self.avg_doc_length = total_length / len(documents) if documents else 0
    
    def _bm25_score(self, word: str, doc_id: int, tf: int) -> float:
        """Calculate BM25 score for a word in a document"""
        if word not in self.idf:
            return 0
        
        idf = self.idf[word]
        doc_length = self.doc_lengths[doc_id]
        
        # BM25 formula
        numerator = tf * (self.k1 + 1)
        denominator = tf + self.k1 * (1 - self.b + self.b * (doc_length / self.avg_doc_length))
        
        return idf * (numerator / denominator)
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[Document, float]]:
        """Retrieve documents using BM25 scoring"""
        query_words = preprocess_text(query)
        scores = defaultdict(float)
        
        for doc in self.documents:
            words = preprocess_text(doc.content)
            tf = defaultdict(int)
            
            for word in words:
                tf[word] += 1
            
            # Score this document
            for query_word in query_words:
                if query_word in tf:
                    score = self._bm25_score(query_word, doc.id, tf[query_word])
                    scores[doc.id] += score
        
        # Sort and return top-k
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        results = [(self._get_doc(doc_id), score) for doc_id, score in ranked]
        
        return results
    
    def _get_doc(self, doc_id: int) -> Document:
        return next(d for d in self.documents if d.id == doc_id)

# ============================================================================
# PART 5: METADATA FILTERING
# ============================================================================

class MetadataFilter:
    """Apply filters based on user context and document metadata"""
    
    @staticmethod
    def filter_documents(
        documents: List[Document],
        access_level: str = "public",
        region: str = None,
        category: str = None
    ) -> List[Document]:
        """Filter documents based on metadata criteria"""
        filtered = []
        
        for doc in documents:
            # Check access level
            if doc.metadata["access_level"] not in [access_level, "public"]:
                continue
            
            # Check region if specified
            if region and doc.metadata["region"] != region:
                continue
            
            # Check category if specified
            if category and doc.metadata["category"] != category:
                continue
            
            filtered.append(doc)
        
        return filtered

# ============================================================================
# PART 6: COMPLETE RAG SYSTEM
# ============================================================================

class RAGSystem:
    """Complete RAG system combining retrieval techniques"""
    
    def __init__(self, documents: List[Document]):
        self.documents = documents
        self.tfidf = TFIDFRetriever(documents)
        self.bm25 = BM25Retriever(documents)
        self.metadata_filter = MetadataFilter()
    
    def retrieve_with_tfidf(self, query: str, top_k: int = 3, user_access: str = None, user_region: str = None) -> List[Tuple[Document, float]]:
        """Retrieve using TF-IDF with optional metadata filtering"""
        results = self.tfidf.retrieve(query, top_k=top_k)
        
        if user_access or user_region:
            filtered_docs = self.metadata_filter.filter_documents(
                self.documents,
                access_level=user_access or "public",
                region=user_region
            )
            filtered_ids = {d.id for d in filtered_docs}
            results = [(doc, score) for doc, score in results if doc.id in filtered_ids]
        
        return results
    
    def retrieve_with_bm25(self, query: str, top_k: int = 3, user_access: str = None, user_region: str = None) -> List[Tuple[Document, float]]:
        """Retrieve using BM25 with optional metadata filtering"""
        results = self.bm25.retrieve(query, top_k=top_k)
        
        if user_access or user_region:
            filtered_docs = self.metadata_filter.filter_documents(
                self.documents,
                access_level=user_access or "public",
                region=user_region
            )
            filtered_ids = {d.id for d in filtered_docs}
            results = [(doc, score) for doc, score in results if doc.id in filtered_ids]
        
        return results

# ============================================================================
# PART 7: DEMONSTRATION
# ============================================================================

def print_results(title: str, results: List[Tuple[Document, float]]):
    """Pretty print retrieval results"""
    print(f"\n{'='*70}")
    print(f"{title}")
    print(f"{'='*70}")
    
    if not results:
        print("❌ No results found")
        return
    
    for idx, (doc, score) in enumerate(results, 1):
        print(f"\n{idx}. {doc.title}")
        print(f"   Author: {doc.metadata['author']}")
        print(f"   Category: {doc.metadata['category']} | Region: {doc.metadata['region']}")
        print(f"   Access Level: {doc.metadata['access_level']}")
        print(f"   Score: {score:.4f}")
        print(f"   Preview: {doc.content[:100]}...")

# ============================================================================
# RUN EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("RAG SYSTEM: Complete Python Example")
    print("="*70)
    
    rag = RAGSystem(documents)
    
    # Example 1: Compare TF-IDF vs BM25
    query = "how to make pizza in an oven"
    
    print(f"\n🔍 QUERY: '{query}'")
    
    tfidf_results = rag.retrieve_with_tfidf(query, top_k=3)
    bm25_results = rag.retrieve_with_bm25(query, top_k=3)
    
    print_results("TF-IDF Results", tfidf_results)
    print_results("BM25 Results", bm25_results)
    
    # Example 2: Metadata Filtering - Public User in UAE
    print("\n\n" + "="*70)
    print("METADATA FILTERING Example")
    print("="*70)
    print("\n👤 User Context: Public Access, Region: UAE")
    
    bm25_filtered = rag.retrieve_with_bm25(
        query,
        top_k=3,
        user_access="public",
        user_region="UAE"
    )
    print_results("BM25 Results (with Metadata Filter)", bm25_filtered)
    
    # Example 3: Premium User Access
    print("\n\n👤 User Context: Premium Access, Region: UAE")
    
    premium_user_results = rag.retrieve_with_bm25(
        query,
        top_k=3,
        user_access="premium",
        user_region="UAE"
    )
    print_results("BM25 Results (Premium User)", premium_user_results)
    
    # Example 4: Different Query
    query2 = "pizza dough recipe"
    print(f"\n\n🔍 QUERY: '{query2}'")
    
    tfidf_results2 = rag.retrieve_with_tfidf(query2, top_k=3)
    bm25_results2 = rag.retrieve_with_bm25(query2, top_k=3)
    
    print_results("TF-IDF Results", tfidf_results2)
    print_results("BM25 Results", bm25_results2)
    
    # Example 5: Show all documents
    print("\n\n" + "="*70)
    print("ALL DOCUMENTS IN KNOWLEDGE BASE")
    print("="*70)
    for doc in documents:
        print(f"\n📄 [{doc.id}] {doc.title}")
        print(f"   Category: {doc.metadata['category']} | Region: {doc.metadata['region']}")
        print(f"   Access: {doc.metadata['access_level']}")
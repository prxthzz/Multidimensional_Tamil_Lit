import json
import math
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

from shared.interfaces.tamil_retrieval import TamilRetrievalInterface
from shared.schemas.tamil_retrieval import (
    TamilRetrievalRequest,
    TamilRetrievalResult,
)

BASE_DIR = Path(__file__).resolve().parents[3]
EMBEDDING_FILE = BASE_DIR / "indexes" / "tamil" / "embeddings.npy"
METADATA_FILE = BASE_DIR / "indexes" / "tamil" / "metadata.json"
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

DEFAULT_HYBRID_WEIGHTS = {
    "semantic": 0.40,
    "lexical": 0.25,
    "theme": 0.15,
    "domain": 0.10,
    "metadata": 0.10,
    "reranker": 0.30,
}

DOMAIN_THEME_MAP = {
    "Physics": ["Cosmic Order", "Time & Space", "Universal Structure", "Gravity", "Light Motion", "Sound & Speech"],
    "Astronomy": ["Cosmic Order", "Stars & Sun", "Sky & Heavenly Bodies", "Sun as Source of Life", "Moonlight & Coolness"],
    "Environment": ["Rain as Universal Nurturer", "Water as Sustenance of Life", "Vaan Chirappu", "Air & Wind", "Harmony with Nature"],
    "Agriculture": ["Agriculture as World Foundation", "Uzhavu", "Nourishment of Humanity", "Fertile Soil", "Water Management"],
    "Biology": ["Sacredness of Life", "Non-killing", "Nourishment", "Green Nature", "Flourishing Plants", "Compassion"],
    "Medicine": ["Marunthu Chapter", "Holistic Health", "Root Cause Diagnosis", "Healthy Eating", "Moderation in Food", "Physical Cleanliness"],
    "Computer Science": ["Arivudaimai", "Meyyunarvu", "True Knowledge", "Power of Words", "Eloquence & Precision"],
    "Psychology": ["Manam Thuyamai", "Self-Control", "Moral Excellence", "Perception of Truth"]
}

def tokenize_tamil_english(text: str) -> List[str]:
    """Tokenizes both Tamil and English text cleanly."""
    if not text:
        return []
    # Replace punctuation with space
    clean = re.sub(r"[^\w\s\u0B80-\u0BFF]", " ", text.lower())
    return [t for t in clean.split() if len(t) > 1]

class SemanticTamilRetriever(TamilRetrievalInterface):
    """
    Production Hybrid Tamil Literary Retriever:
    Combines Genuine Okapi BM25 Lexical Search with Dense Multilingual Embeddings
    and Contextual Theme/Domain metadata scores.
    """

    def __init__(self, top_k: int = 5, custom_weights: Optional[Dict[str, float]] = None):
        self.top_k = top_k
        self.weights = custom_weights or DEFAULT_HYBRID_WEIGHTS
        self.embeddings = np.load(EMBEDDING_FILE)
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)
        
        self.model = SentenceTransformer(MODEL_NAME)
        
        # Build Real Okapi BM25 Index
        corpus_tokens = [tokenize_tamil_english(doc.get("text", "")) for doc in self.metadata]
        self.bm25 = BM25Okapi(corpus_tokens)

    def _build_query(self, request: TamilRetrievalRequest) -> str:
        terms = (
            request.scientific_concepts
            + request.scientific_domains
            + request.context_terms
            + request.query_terms
        )
        return " ".join(
            term.strip()
            for term in terms
            if isinstance(term, str) and term.strip()
        )

    def _find_matched_terms(
        self,
        request: TamilRetrievalRequest,
        text: str,
    ) -> List[str]:
        terms = (
            request.scientific_concepts
            + request.scientific_domains
            + request.context_terms
            + request.query_terms
        )
        matched_terms = []
        text_lower = text.lower()
        for term in terms:
            if isinstance(term, str) and term.strip():
                t = term.strip()
                if t.lower() in text_lower and t not in matched_terms:
                    matched_terms.append(t)
        return matched_terms

    def _compute_theme_score(self, doc_metadata: dict, domains: List[str]) -> float:
        chapter = str(doc_metadata.get("chapter", doc_metadata.get("chapter_number", ""))).lower()
        work = str(doc_metadata.get("work", "")).lower()
        score = 0.0
        for domain in domains:
            expected_themes = DOMAIN_THEME_MAP.get(domain, [])
            for theme in expected_themes:
                if theme.lower() in chapter or theme.lower() in work:
                    score += 0.5
        return min(1.0, score)

    def _compute_domain_score(self, doc_metadata: dict, domains: List[str]) -> float:
        if not domains:
            return 0.5
        chapter = str(doc_metadata.get("chapter", doc_metadata.get("chapter_number", ""))).lower()
        for dom in domains:
            d_lower = dom.lower()
            if d_lower in ["environment", "water", "rain"] and ("vaan" in chapter or "rain" in chapter or "2" in chapter):
                return 1.0
            if d_lower in ["agriculture", "farming"] and ("uzhavu" in chapter or "agriculture" in chapter or "104" in chapter):
                return 1.0
            if d_lower in ["medicine", "health"] and ("marunthu" in chapter or "medicine" in chapter or "95" in chapter):
                return 1.0
        return 0.4

    def retrieve(
        self,
        request: TamilRetrievalRequest,
    ) -> List[TamilRetrievalResult]:
        query_text = self._build_query(request)
        if not query_text:
            return []

        # 1. Semantic Vector Similarity
        query_embedding = self.model.encode(
            [query_text],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )[0]
        raw_semantic_scores = self.embeddings @ query_embedding
        semantic_scores = (raw_semantic_scores + 1.0) / 2.0  # Normalize to [0, 1]

        # 2. Genuine Okapi BM25 Lexical Retrieval
        query_tokens = tokenize_tamil_english(query_text)
        bm25_scores = self.bm25.get_scores(query_tokens)
        max_bm25 = float(np.max(bm25_scores)) if len(bm25_scores) > 0 and np.max(bm25_scores) > 0 else 1.0
        normalized_bm25_scores = bm25_scores / max_bm25

        # 3. Hybrid Rank Candidate Fusion
        fusion_records = []
        for index in range(len(self.metadata)):
            doc = self.metadata[index]
            sem_s = float(semantic_scores[index])
            lex_s = float(normalized_bm25_scores[index])
            theme_s = self._compute_theme_score(doc.get("metadata", {}), request.scientific_domains)
            domain_s = self._compute_domain_score(doc.get("metadata", {}), request.scientific_domains)
            meta_s = 0.9 if doc.get("source_type") == "thirukkural" else 0.75

            hybrid_score = (
                self.weights["semantic"] * sem_s +
                self.weights["lexical"] * lex_s +
                self.weights["theme"] * theme_s +
                self.weights["domain"] * domain_s +
                self.weights["metadata"] * meta_s
            )

            fusion_records.append((index, sem_s, lex_s, theme_s, domain_s, meta_s, hybrid_score))

        fusion_records.sort(key=lambda x: x[6], reverse=True)
        top_candidates = fusion_records[: self.top_k]

        results = []
        for index, sem_s, lex_s, theme_s, domain_s, meta_s, hybrid_score in top_candidates:
            document = self.metadata[index]
            matched_terms = self._find_matched_terms(request, document["text"])
            
            doc_meta = dict(document.get("metadata", {}))
            retrieval_relevance = round(min(1.0, max(0.0, hybrid_score)), 4)

            doc_meta.update({
                "retrieval_relevance": retrieval_relevance,
                "semantic_score": round(sem_s, 4),
                "lexical_score": round(lex_s, 4),
                "keyword_score": round(lex_s, 4),
                "theme_score": round(theme_s, 4),
                "domain_score": round(domain_s, 4),
                "metadata_score": round(meta_s, 4),
                "hybrid_score": round(hybrid_score, 4),
                "cross_encoder_score": None,
                "final_score": round(hybrid_score, 4),
                "active_retrieval_weights": self.weights,
            })

            result = TamilRetrievalResult(
                source_id=document["source_id"],
                source_type=document["source_type"],
                text=document["text"],
                matched_terms=matched_terms,
                retrieval_score=retrieval_relevance,
                semantic_score=round(sem_s, 4),
                keyword_score=round(lex_s, 4),
                theme_score=round(theme_s, 4),
                domain_score=round(domain_s, 4),
                metadata_score=round(meta_s, 4),
                hybrid_score=round(hybrid_score, 4),
                cross_encoder_score=None,
                final_score=round(hybrid_score, 4),
                metadata=doc_meta,
            )
            results.append(result)

        return results
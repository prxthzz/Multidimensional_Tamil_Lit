# Production Architecture Specification

## AI-Assisted Tamil Literary and Scientific Knowledge, Evidence and Research Platform

### 1. System Overview
The platform connects classical Tamil literature (*Thirukkural* and *Thiruvarutpa*) with modern scientific concepts across 8 domains (Physics, Astronomy, Environment, Agriculture, Biology, Medicine, Computer Science, Psychology).

### 2. Multi-Layered Pipeline Architecture

```
USER QUERY (English / Tamil / Tanglish)
   │
   ├── 1. Multilingual Query Understanding (Unicode Normalization & Transliteration)
   ├── 2. Scientific Ontology Mapping (54 Curated Concepts)
   ├── 3. Wormhole Routing Layer (1D-4D Dimension Router)
   ├── 4. Real Okapi BM25 Lexical + Dense Multilingual Vector Hybrid Retrieval
   ├── 5. Cross-Encoder Reranking (mmarco-mMiniLMv2)
   ├── 6. 3-Score Calculation:
   │       - RETRIEVAL RELEVANCE (%)
   │       - EVIDENCE STRENGTH (HIGH, MEDIUM, LOW, NONE)
   │       - INTERPRETATION CONFIDENCE (%)
   ├── 7. Evidence Alignment & Hallucination Guard
   ├── 8. Governed Knowledge Graph & Evidence Record Persistence
   └── 9. LLM Gateway Explanation & Post-Generation Validation
```

### 3. Core Academic Principles
1. **Semantic Similarity ≠ Scientific Proof**: The system explicitly differentiates poetic analogies from empirical scientific discovery.
2. **Provenance & Auditability**: Every generated answer is anchored to persistent `EvidenceRecord` entities with full model/corpus versioning.
3. **Human Expert Overrides**: AI relationship interpretations can be approved, rejected, or modified by Domain/Literary experts. AI never overwrites approved decisions.

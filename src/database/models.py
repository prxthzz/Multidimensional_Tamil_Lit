import datetime
import uuid
from sqlalchemy import (
    Column, String, Integer, Float, Text, Boolean, DateTime, ForeignKey, Enum as SQLEnum, JSON
)
from sqlalchemy.orm import relationship
import enum
from src.database.connection import Base

class RoleEnum(str, enum.Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    DOMAIN_EXPERT = "DOMAIN_EXPERT"
    LITERARY_EXPERT = "LITERARY_EXPERT"
    REVIEWER = "REVIEWER"
    RESEARCHER = "RESEARCHER"
    OPERATOR = "OPERATOR"
    AUDITOR = "AUDITOR"
    GENERAL_USER = "GENERAL_USER"

class RelationshipTypeEnum(str, enum.Enum):
    DIRECT = "DIRECT"
    STRONG_ANALOGY = "STRONG_ANALOGY"
    THEMATIC = "THEMATIC"
    METAPHORICAL = "METAPHORICAL"
    UNSUPPORTED = "UNSUPPORTED"

class EvidenceStrengthEnum(str, enum.Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NONE = "NONE"

class ReviewStatusEnum(str, enum.Enum):
    DRAFT = "DRAFT"
    PENDING_REVIEW = "PENDING_REVIEW"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    NEEDS_REVISION = "NEEDS_REVISION"
    ARCHIVED = "ARCHIVED"

class CopyrightStatusEnum(str, enum.Enum):
    PUBLIC_DOMAIN = "PUBLIC_DOMAIN"
    LICENSED = "LICENSED"
    INSTITUTIONAL = "INSTITUTIONAL"
    PERMISSION_REQUIRED = "PERMISSION_REQUIRED"
    RESTRICTED = "RESTRICTED"
    UNKNOWN = "UNKNOWN"

class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default=RoleEnum.GENERAL_USER)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=True)
    username = Column(String(100), nullable=True)
    action = Column(String(100), nullable=False, index=True)
    resource = Column(String(255), nullable=False)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(50), nullable=True)
    request_id = Column(String(100), nullable=True)
    system_version = Column(String(50), default="0.3.0")
    status = Column(String(50), default="SUCCESS")
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)

class ScientificDomain(Base):
    __tablename__ = "scientific_domains"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, nullable=False)
    tamil_name = Column(String(150), nullable=True)
    description = Column(Text, nullable=True)

class ScientificConcept(Base):
    __tablename__ = "scientific_concepts"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    concept_id = Column(String(100), unique=True, nullable=False, index=True)
    canonical_name = Column(String(200), nullable=False)
    tamil_name = Column(String(200), nullable=True)
    domain_id = Column(String(36), ForeignKey("scientific_domains.id"), nullable=True)
    domain_name = Column(String(100), nullable=False)
    aliases = Column(JSON, default=list)
    tamil_aliases = Column(JSON, default=list)
    definition = Column(Text, nullable=False)
    scientific_sources = Column(JSON, default=list)
    version = Column(String(20), default="1.0.0")
    status = Column(String(50), default="ACTIVE")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class TamilConcept(Base):
    __tablename__ = "tamil_concepts"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tamil_term = Column(String(200), nullable=False, index=True)
    transliteration = Column(String(200), nullable=True)
    category = Column(String(100), nullable=True)
    meaning_english = Column(Text, nullable=True)
    meaning_tamil = Column(Text, nullable=True)

class LiteraryWork(Base):
    __tablename__ = "literary_works"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    work_id = Column(String(100), unique=True, nullable=False, index=True)
    title_english = Column(String(200), nullable=False)
    title_tamil = Column(String(200), nullable=False)
    author = Column(String(200), nullable=True)
    period = Column(String(100), nullable=True)
    license = Column(String(50), default=CopyrightStatusEnum.PUBLIC_DOMAIN)
    copyright_status = Column(String(50), default=CopyrightStatusEnum.PUBLIC_DOMAIN)
    digitization_source = Column(String(255), nullable=True)
    total_verses = Column(Integer, default=0)
    version = Column(String(20), default="1.0.0")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Chapter(Base):
    __tablename__ = "chapters"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    work_id = Column(String(100), ForeignKey("literary_works.work_id"), nullable=False)
    chapter_number = Column(Integer, nullable=False)
    name_tamil = Column(String(200), nullable=False)
    name_english = Column(String(200), nullable=False)
    transliteration = Column(String(200), nullable=True)

class Verse(Base):
    __tablename__ = "verses"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String(100), unique=True, nullable=False, index=True)
    work_id = Column(String(100), nullable=False)
    source_type = Column(String(50), nullable=False)
    verse_number = Column(Integer, nullable=False)
    text_tamil = Column(Text, nullable=False)
    normalized_text = Column(Text, nullable=True)
    chapter_name_tamil = Column(String(200), nullable=True)
    chapter_name_english = Column(String(200), nullable=True)
    section_tamil = Column(String(200), nullable=True)
    section_english = Column(String(200), nullable=True)
    version = Column(String(20), default="1.0.0")

class Translation(Base):
    __tablename__ = "translations"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    verse_id = Column(String(100), ForeignKey("verses.source_id"), nullable=False)
    translator = Column(String(200), nullable=False)
    language = Column(String(50), default="english")
    translation_text = Column(Text, nullable=False)

class Commentary(Base):
    __tablename__ = "commentaries"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    verse_id = Column(String(100), ForeignKey("verses.source_id"), nullable=False)
    commentator = Column(String(200), nullable=False)
    commentary_text = Column(Text, nullable=False)
    language = Column(String(50), default="tamil")

class EvidenceRecord(Base):
    __tablename__ = "evidence_records"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    evidence_id = Column(String(100), unique=True, nullable=False, index=True)
    scientific_concept_id = Column(String(100), nullable=False)
    scientific_concept_name = Column(String(200), nullable=False)
    literary_source_id = Column(String(100), nullable=False)
    verse_id = Column(String(100), nullable=False)
    relationship_type = Column(String(50), nullable=False)
    retrieval_relevance = Column(Float, nullable=False)
    evidence_strength = Column(String(50), nullable=False)
    interpretation_confidence = Column(Float, nullable=False)
    scientific_claim = Column(Text, nullable=True)
    literary_claim = Column(Text, nullable=True)
    comparison = Column(Text, nullable=True)
    supporting_text = Column(Text, nullable=False)
    translation = Column(Text, nullable=True)
    commentary = Column(Text, nullable=True)
    limitations = Column(JSON, default=list)
    review_status = Column(String(50), default=ReviewStatusEnum.DRAFT)
    reviewer_ids = Column(JSON, default=list)
    created_by = Column(String(100), default="SYSTEM")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    version = Column(String(20), default="1.0.0")
    corpus_version = Column(String(20), default="1.0.0")
    embedding_version = Column(String(50), default="paraphrase-multilingual-MiniLM-L12-v2")
    retriever_version = Column(String(50), default="hybrid_v1")
    reranker_version = Column(String(50), default="cross-encoder-mmarco-v1")
    llm_version = Column(String(50), default="qwen2.5-7b-instruct")
    prompt_version = Column(String(20), default="v1.0")

class ExpertReview(Base):
    __tablename__ = "expert_reviews"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    evidence_id = Column(String(100), ForeignKey("evidence_records.evidence_id"), nullable=False)
    reviewer_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    reviewer_name = Column(String(200), nullable=False)
    reviewer_role = Column(String(50), nullable=False)
    status_decision = Column(String(50), nullable=False)
    relationship_override = Column(String(50), nullable=True)
    evidence_strength_override = Column(String(50), nullable=True)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ResearchSession(Base):
    __tablename__ = "research_sessions"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False)
    session_title = Column(String(200), nullable=False)
    saved_queries = Column(JSON, default=list)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class SavedSearch(Base):
    __tablename__ = "saved_searches"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False)
    query_text = Column(String(500), nullable=False)
    filters = Column(JSON, default=dict)
    results_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    run_id = Column(String(100), unique=True, nullable=False, index=True)
    benchmark_file = Column(String(255), default="data/evaluation_benchmark.json")
    total_queries = Column(Integer, nullable=False)
    precision_at_5 = Column(Float, nullable=False)
    recall_at_5 = Column(Float, nullable=False)
    mrr = Column(Float, nullable=False)
    ndcg_at_5 = Column(Float, nullable=False)
    unsupported_claim_rate_pct = Column(Float, nullable=False)
    mean_latency_ms = Column(Float, nullable=False)
    ablation_results = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class SystemConfiguration(Base):
    __tablename__ = "system_configurations"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    config_key = Column(String(100), unique=True, nullable=False)
    config_value = Column(JSON, nullable=False)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class ModelRegistry(Base):
    __tablename__ = "model_registry"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    model_name = Column(String(100), nullable=False)
    model_type = Column(String(50), nullable=False) # EMBEDDING, RERANKER, LLM
    provider = Column(String(50), default="local")
    version = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    parameters = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

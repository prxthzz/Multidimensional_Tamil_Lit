import json
import logging
from pathlib import Path
from passlib.context import CryptContext
from src.database.connection import SessionLocal, init_db
from src.database.models import (
    User, Permission, RoleEnum, ScientificDomain, ScientificConcept,
    LiteraryWork, Chapter, Verse, CopyrightStatusEnum, SystemConfiguration, ModelRegistry
)

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
logger = logging.getLogger("seed")

BASE_DIR = Path(__file__).resolve().parents[2]
KNOWLEDGE_BASE_PATH = BASE_DIR / "data" / "scientific" / "scientific_knowledge.json"
METADATA_INDEX_PATH = BASE_DIR / "indexes" / "tamil" / "metadata.json"

def seed_database():
    init_db()
    db = SessionLocal()
    try:
        # 1. Seed Roles & Default Users
        default_users = [
            ("superadmin", "superadmin@platform.org", "Admin@123456", "Super Administrator", RoleEnum.SUPER_ADMIN),
            ("admin", "admin@platform.org", "Admin@123456", "System Administrator", RoleEnum.ADMIN),
            ("dr_tamil_expert", "tamil_expert@platform.org", "Expert@123456", "Dr. K. Arul (Tamil Literary Expert)", RoleEnum.LITERARY_EXPERT),
            ("dr_sci_expert", "sci_expert@platform.org", "Expert@123456", "Dr. S. Raman (Scientific Domain Expert)", RoleEnum.DOMAIN_EXPERT),
            ("reviewer_1", "reviewer@platform.org", "Review@123456", "Senior Peer Reviewer", RoleEnum.REVIEWER),
            ("researcher_1", "researcher@platform.org", "Research@123456", "Senior Research Fellow", RoleEnum.RESEARCHER),
            ("auditor_1", "auditor@platform.org", "Audit@123456", "Security Auditor", RoleEnum.AUDITOR),
            ("user_demo", "user@platform.org", "User@123456", "General Research User", RoleEnum.GENERAL_USER),
        ]

        for username, email, raw_password, full_name, role in default_users:
            existing = db.query(User).filter(User.username == username).first()
            if not existing:
                hashed = pwd_context.hash(raw_password)
                user = User(
                    username=username,
                    email=email,
                    hashed_password=hashed,
                    full_name=full_name,
                    role=role,
                    is_active=True,
                    is_verified=True
                )
                db.add(user)

        # 2. Seed Literary Works Metadata
        works = [
            ("thirukkural", "Thirukkural", "திருக்குறள்", "Thiruvalluvar", "Classical Sangam / Post-Sangam (c. 31 BCE)", CopyrightStatusEnum.PUBLIC_DOMAIN, 1330),
            ("thiruvarutpa", "Thiruvarutpa", "திருவருட்பா", "Ramalinga Swamigal (Vallalar)", "19th Century CE", CopyrightStatusEnum.PUBLIC_DOMAIN, 570),
        ]
        for work_id, t_eng, t_tam, author, period, license_stat, total_v in works:
            existing_w = db.query(LiteraryWork).filter(LiteraryWork.work_id == work_id).first()
            if not existing_w:
                w = LiteraryWork(
                    work_id=work_id,
                    title_english=t_eng,
                    title_tamil=t_tam,
                    author=author,
                    period=period,
                    license=license_stat,
                    copyright_status=license_stat,
                    digitization_source="Tamil Digital Library & Open Corpus",
                    total_verses=total_v
                )
                db.add(w)

        # 3. Seed Scientific Knowledge Base Concepts
        if KNOWLEDGE_BASE_PATH.exists():
            with open(KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as f:
                kb_data = json.load(f)

            for dom_data in kb_data.get("domains", []):
                dom_name = dom_data["name"]
                dom_obj = db.query(ScientificDomain).filter(ScientificDomain.name == dom_name).first()
                if not dom_obj:
                    dom_obj = ScientificDomain(name=dom_name, description=dom_data.get("description", ""))
                    db.add(dom_obj)
                    db.flush()

                for subdomain in dom_data.get("subdomains", []):
                    for concept in subdomain.get("concepts", []):
                        c_id = concept["id"]
                        existing_c = db.query(ScientificConcept).filter(ScientificConcept.concept_id == c_id).first()
                        if not existing_c:
                            sc = ScientificConcept(
                                concept_id=c_id,
                                canonical_name=concept["name"],
                                tamil_name=concept.get("tamil_name", ""),
                                domain_id=dom_obj.id,
                                domain_name=dom_name,
                                aliases=concept.get("keywords", []),
                                tamil_aliases=concept.get("context_terms", []),
                                definition=concept.get("definition", ""),
                                scientific_sources=["ISO/IEC Standard Scientific Ontology", "NCBI Entrez / IEEE Corpus"],
                                version="1.0.0",
                                status="ACTIVE"
                            )
                            db.add(sc)

        # 4. Seed Metadata Verses
        if METADATA_INDEX_PATH.exists():
            with open(METADATA_INDEX_PATH, "r", encoding="utf-8") as f:
                meta_records = json.load(f)
            
            for item in meta_records:
                s_id = item["source_id"]
                existing_v = db.query(Verse).filter(Verse.source_id == s_id).first()
                if not existing_v:
                    doc_m = item.get("metadata", {})
                    v = Verse(
                        source_id=s_id,
                        work_id=doc_m.get("work", item.get("source_type", "")).lower(),
                        source_type=item.get("source_type", "thirukkural"),
                        verse_number=int(doc_m.get("verse_number", 0)) if str(doc_m.get("verse_number", "0")).isdigit() else 0,
                        text_tamil=item.get("text", ""),
                        normalized_text=item.get("text", "").lower(),
                        chapter_name_tamil=doc_m.get("chapter", ""),
                        chapter_name_english=doc_m.get("chapter", ""),
                        section_tamil=doc_m.get("section", ""),
                        section_english=doc_m.get("section", ""),
                        version="1.0.0"
                    )
                    db.add(v)

        # 5. Default System Configurations
        default_configs = [
            ("retrieval_weights", {
                "semantic": 0.40,
                "keyword": 0.25,
                "theme": 0.15,
                "domain": 0.10,
                "metadata": 0.10,
                "reranker": 0.30
            }, "Configurable Weights for Hybrid Candidate Fusion and Cross-Encoder Reranking"),
            ("llm_gateway_provider", {
                "provider": "local",
                "default_model": "qwen2.5-7b-instruct",
                "external_allowed": False
            }, "System LLM Gateway Configuration"),
            ("security_policy", {
                "jwt_expire_minutes": 120,
                "max_login_attempts": 5,
                "rate_limit_per_min": 60
            }, "Security and Rate Limiting Policies")
        ]

        for key, val, desc in default_configs:
            cfg = db.query(SystemConfiguration).filter(SystemConfiguration.config_key == key).first()
            if not cfg:
                cfg = SystemConfiguration(config_key=key, config_value=val, description=desc)
                db.add(cfg)

        db.commit()
        print("Database seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

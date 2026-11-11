import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Dict, List
from scientific.query.expander import ScientificConceptExpander
from shared.schemas.scientific_query import ScientificQuery

MULTILINGUAL_CONCEPT_MAP = {
    # Astronomy & Space
    "astrophysics": "Astrophysics",
    "meteor": "Meteoroids & Celestial Bodies",
    "meteors": "Meteoroids & Celestial Bodies",
    "meteoroid": "Meteoroids & Celestial Bodies",
    "meteoroids": "Meteoroids & Celestial Bodies",
    "asteroid": "Meteoroids & Celestial Bodies",
    "comet": "Meteoroids & Celestial Bodies",
    "vinveli iyarpiyal": "Astrophysics",
    "விண்வெளி இயற்பியல்": "Astrophysics",
    "vinveli": "Astrophysics",
    "விண்வெளி": "Astrophysics",
    "vinmeen": "Stellar Evolution",
    "விண்மீன்": "Stellar Evolution",
    "andaviyal": "Cosmology",
    "அண்டவியல்": "Cosmology",
    "sooriyan": "Solar Energy & Sun",
    "சூரியன்": "Solar Energy & Sun",
    "chandiran": "Lunar Cycle & Tides",
    "சந்திரன்": "Lunar Cycle & Tides",

    # Physics & Relativity
    "quantum": "Quantum Mechanics & Light",
    "photon": "Light & Electromagnetic Radiation",
    "velikkalam": "Spacetime",
    "வெளிக்காலம்": "Spacetime",
    "eerppu visai": "Gravity",
    "eerppu": "Gravity",
    "ஈர்ப்பு விசை": "Gravity",
    "ஈர்ப்பு": "Gravity",
    "kaala neetchi": "Time Dilation",
    "கால நீட்சி": "Time Dilation",
    "seer kulaivu": "Entropy",
    "சீர்குலைவு": "Entropy",
    "aattral aziyaavidhi": "Conservation of Energy",
    "ஆற்றல் அழியாவிதி": "Conservation of Energy",
    "veppam": "Heat Transfer & Thermal Energy",
    "வெப்பம்": "Heat Transfer & Thermal Energy",

    # Environment & Hydrology
    "neer suzharchi": "Water Cycle",
    "நீர்ச் சுழற்சி": "Water Cycle",
    "mazhai": "Water Cycle",
    "மழை": "Water Cycle",
    "water cycle": "Water Cycle",
    "rain": "Water Cycle",
    "valimandalam": "Atmosphere & Wind",
    "வளிமண்டலம்": "Atmosphere & Wind",
    "kaatru": "Atmosphere & Wind",
    "காற்று": "Atmosphere & Wind",
    "soozhnilai samanilai": "Ecological Balance",
    "சூழ்நிலைச் சமநிலை": "Ecological Balance",

    # Agriculture
    "uzhavu": "Crop Cultivation & Farming",
    "உழவு": "Crop Cultivation & Farming",
    "uzhavu thozhil": "Crop Cultivation & Farming",
    "உழவுத் தொழில்": "Crop Cultivation & Farming",
    "farming": "Crop Cultivation & Farming",
    "agriculture": "Crop Cultivation & Farming",
    "man valam": "Soil Health & Fertility",
    "மண் வளம்": "Soil Health & Fertility",
    "neer paasanam": "Irrigation & Water Management",
    "நீர்ப்பாசனம்": "Irrigation & Water Management",

    # Biology & Medicine
    "uyir": "Life Sustenance & Respiration",
    "உயிர்": "Life Sustenance & Respiration",
    "taavaram": "Plant Biology & Flora",
    "தாவரம்": "Plant Biology & Flora",
    "maruthuvam": "Preventive Healthcare & Diagnosis",
    "மருத்துவம்": "Preventive Healthcare & Diagnosis",
    "marunthu": "Preventive Healthcare & Diagnosis",
    "மருந்து": "Preventive Healthcare & Diagnosis",
    "medicine": "Preventive Healthcare & Diagnosis",
    "unavu": "Nutritional Science & Moderation",
    "உணவு": "Nutritional Science & Moderation",

    # Computer Science & Psychology
    "arivu": "Knowledge & Logical Reasoning",
    "அறிவு": "Knowledge & Logical Reasoning",
    "meyyunarvu": "Perception & Epistemology",
    "மெய்யுணர்வு": "Perception & Epistemology",
    "sollatchi": "Information Exchange & Rhetoric",
    "சொல்லாட்சி": "Information Exchange & Rhetoric",
    "araneri": "Moral Cognition & Self-Control",
    "அறநெறி": "Moral Cognition & Self-Control",
    "manam": "Moral Cognition & Self-Control",
    "மனம்": "Moral Cognition & Self-Control",
}


class ScientificQueryProcessor:
    """
    Converts any user query dynamically into a structured ScientificQuery.
    Supports English, Tamil Unicode, and Tanglish transliteration.
    """

    def __init__(self, knowledge_base_path: str | Path):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.knowledge_base = self._load_knowledge_base()
        self.expander = ScientificConceptExpander(self.knowledge_base_path)

    def _load_knowledge_base(self) -> dict:
        with self.knowledge_base_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def detect_language(self, query: str) -> str:
        if re.search(r"[\u0b80-\u0bff]", query):
            return "tamil"
        lower_q = query.lower()
        for tanglish_term in MULTILINGUAL_CONCEPT_MAP:
            if not re.search(r"[\u0b80-\u0bff]", tanglish_term) and tanglish_term in lower_q:
                return "tanglish"
        return "english"

    def normalize(self, query: str) -> str:
        query = unicodedata.normalize("NFC", query).strip().lower()
        query = re.sub(r"\s+", " ", query)
        query = re.sub(r"\bfields\b", "fields", query)
        query = re.sub(r"\bforces\b", "forces", query)
        query = re.sub(r"\bwaves\b", "wave", query)
        query = re.sub(r"\bparticles\b", "particle", query)
        query = re.sub(r"\boscillations\b", "oscillations", query)
        return query

    def _contains_phrase(self, query: str, phrase: str) -> bool:
        phrase = phrase.strip().lower()
        if not phrase:
            return False
        if re.search(r"[\u0b80-\u0bff]", phrase):
            return phrase in query
        pattern = r"\b" + re.escape(phrase) + r"\b"
        return re.search(pattern, query) is not None

    def _infer_domain(self, query_str: str) -> List[str]:
        q = query_str.lower()
        domains = []
        if any(w in q for w in ["space", "star", "planet", "meteor", "asteroid", "galaxy", "cosmos", "astronomy", "sky", "sun", "moon"]):
            domains.append("Astronomy")
        if any(w in q for w in ["energy", "force", "gravity", "wave", "light", "relativity", "quantum", "time", "motion", "physics"]):
            domains.append("Physics")
        if any(w in q for w in ["water", "rain", "climate", "atmosphere", "environment", "wind", "cloud", "nature"]):
            domains.append("Environment")
        if any(w in q for w in ["crop", "farm", "agriculture", "soil", "plow", "harvest", "grain"]):
            domains.append("Agriculture")
        if any(w in q for w in ["life", "cell", "plant", "flora", "animal", "biology", "organism"]):
            domains.append("Biology")
        if any(w in q for w in ["medicine", "health", "disease", "diet", "doctor", "remedy", "cure"]):
            domains.append("Medicine")
        if any(w in q for w in ["computer", "code", "logic", "information", "speech", "data", "algorithm"]):
            domains.append("Computer Science")
        if any(w in q for w in ["mind", "ethics", "thought", "emotion", "psychology", "moral", "truth"]):
            domains.append("Psychology")
        return domains or ["General Science"]

    def process(self, query: str) -> ScientificQuery:
        normalized_query = self.normalize(query)
        detected_lang = self.detect_language(query)

        concepts = []
        keywords = []
        domains = []
        context_terms = []

        # 1. Multilingual direct dictionary mapping
        for mapped_term, canonical_name in MULTILINGUAL_CONCEPT_MAP.items():
            if self._contains_phrase(normalized_query, mapped_term):
                if canonical_name not in concepts:
                    concepts.append(canonical_name)

        # 2. Knowledge Base concepts traversal
        for domain in self.knowledge_base.get("domains", []):
            domain_name = domain.get("name", "")
            for subdomain in domain.get("subdomains", []):
                subdomain_name = subdomain.get("name", "")
                for concept in subdomain.get("concepts", []):
                    concept_name = concept.get("name", "")
                    tamil_name = concept.get("tamil_name", "")
                    concept_keywords = concept.get("keywords", [])
                    concept_context = concept.get("context_terms", [])

                    match_found = False
                    if self._contains_phrase(normalized_query, concept_name):
                        match_found = True
                    elif tamil_name and self._contains_phrase(normalized_query, tamil_name):
                        match_found = True

                    if not match_found:
                        meaningful_keywords = [
                            kw for kw in concept_keywords if len(kw.split()) >= 2 or re.search(r"[\u0b80-\u0bff]", kw)
                        ]
                        if any(self._contains_phrase(normalized_query, kw) for kw in meaningful_keywords):
                            match_found = True

                    if match_found:
                        if concept_name not in concepts:
                            concepts.append(concept_name)
                        if domain_name and domain_name not in domains:
                            domains.append(domain_name)
                        if subdomain_name and subdomain_name not in domains:
                            domains.append(subdomain_name)
                        for kw in concept_keywords:
                            if kw not in keywords:
                                keywords.append(kw)
                        for term in concept_context:
                            if term not in context_terms:
                                context_terms.append(term)

        # 3. Dynamic Concept Extraction for ANY scientific query
        if not concepts:
            clean_term = re.sub(r"^(what is|who is|explain|tell me about|how does|what are|describe|tell me)\s+", "", normalized_query, flags=re.IGNORECASE).strip(" ?.")
            is_unrelated = any(w in clean_term.lower() for w in ["unrelated", "something", "hello", "hi", "test"])
            if clean_term and not is_unrelated:
                concept_title = clean_term.title()
                concepts.append(concept_title)
                keywords.append(clean_term)
                context_terms.append(clean_term)
                inferred_doms = self._infer_domain(clean_term)
                for d in inferred_doms:
                    if d not in domains:
                        domains.append(d)

        expanded_concepts = self.expander.expand(concepts)

        return ScientificQuery(
            original_query=query,
            normalized_query=normalized_query,
            concepts=concepts,
            keywords=keywords,
            domains=domains,
            context_terms=context_terms,
            expanded_concepts=expanded_concepts,
        )
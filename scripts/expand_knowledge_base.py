import json
from pathlib import Path

DATA_FILE = Path("data/scientific/scientific_knowledge.json")

def build_comprehensive_kb():
    domains = [
        {
            "id": "physics",
            "name": "Physics",
            "description": "Scientific study of matter, energy, space, time, motion, fields, and physical forces.",
            "subdomains": [
                {
                    "id": "relativity",
                    "name": "Relativity",
                    "concepts": [
                        {"id": "spacetime", "name": "Spacetime", "tamil_name": "வெளிக்காலம்", "definition": "A four-dimensional physical framework combining space and time.", "keywords": ["space", "time", "spacetime", "four-dimensional", "velikkalam"], "related_concepts": ["special_relativity", "general_relativity"], "context_terms": ["continuum", "worldline"], "themes": ["Cosmic Order", "Time & Space"]},
                        {"id": "special_relativity", "name": "Special Relativity", "tamil_name": "சிறப்புச் சார்பியல்", "definition": "Physical theory of space and time for inertial observers.", "keywords": ["special relativity", "light speed", "inertial frame"], "related_concepts": ["spacetime", "time_dilation"], "context_terms": ["speed of light", "time dilatation"], "themes": ["Light Motion"]},
                        {"id": "general_relativity", "name": "General Relativity", "tamil_name": "பொதுச் சார்பியல்", "definition": "Theory of gravitation based on spacetime curvature.", "keywords": ["general relativity", "gravity", "spacetime curvature"], "related_concepts": ["gravity", "spacetime"], "context_terms": ["geodesic", "gravitational field"], "themes": ["Gravity", "Cosmic Structure"]},
                        {"id": "time_dilation", "name": "Time Dilation", "tamil_name": "கால நீட்சி", "definition": "Relativistic difference in elapsed time measured by different observers.", "keywords": ["time dilation", "time flow", "kaala neetchi", "relativity", "clock"], "related_concepts": ["special_relativity", "general_relativity"], "context_terms": ["time dilation", "elapsed time", "clocks", "clock", "relativity"], "themes": ["Passage of Time"]},
                        {"id": "gravity", "name": "Gravity", "tamil_name": "ஈர்ப்பு விசை", "definition": "Fundamental attractive interaction between mass and energy.", "keywords": ["gravity", "gravitational force", "attraction", "eerppu visai"], "related_concepts": ["general_relativity"], "context_terms": ["mass attraction", "weight"], "themes": ["Universal Force"]}
                    ]
                },
                {
                    "id": "thermodynamics",
                    "name": "Thermodynamics",
                    "concepts": [
                        {"id": "entropy", "name": "Entropy", "tamil_name": "என்ட்ரோபி (சீர்குலைவு)", "definition": "Measure of disorder and energy dispersal in a thermodynamic system.", "keywords": ["entropy", "disorder", "thermal energy", "seer kulaivu"], "related_concepts": ["heat_transfer"], "context_terms": ["randomness", "decay"], "themes": ["Impermanence", "Cosmic Decay"]},
                        {"id": "conservation_of_energy", "name": "Conservation of Energy", "tamil_name": "ஆற்றல் அழியாவிதி", "definition": "Principle that energy cannot be created or destroyed, only transformed.", "keywords": ["energy conservation", "aattral aziyaavidhi", "transformation"], "related_concepts": ["entropy"], "context_terms": ["constant energy", "transformation"], "themes": ["Eternal Cycle"]},
                        {"id": "heat_transfer", "name": "Heat Transfer & Thermal Energy", "tamil_name": "வெப்ப பரிமாற்றம்", "definition": "Exchange of thermal energy between physical systems.", "keywords": ["heat transfer", "thermal energy", "veppam", "temperature"], "related_concepts": ["entropy"], "context_terms": ["fire", "warmth", "radiation"], "themes": ["Thermal Energy", "Fire Element"]}
                    ]
                },
                {
                    "id": "optics_and_waves",
                    "name": "Optics & Waves",
                    "concepts": [
                        {"id": "light_wave", "name": "Light & Electromagnetic Radiation", "tamil_name": "ஒளி அலையும் கதிர்வீச்சும்", "definition": "Electromagnetic wave propagation carrying luminous energy.", "keywords": ["light wave", "electromagnetic", "oli", "illumination", "photons"], "related_concepts": ["special_relativity"], "context_terms": ["rays", "brightness", "reflection"], "themes": ["Light & Illumination", "Sunlight"]},
                        {"id": "sound_wave", "name": "Sound & Vibration", "tamil_name": "ஒலி அலையும் அதிர்வும்", "definition": "Mechanical wave resulting from back-and-forth vibration of particles.", "keywords": ["sound wave", "vibration", "osai", "sound", "resonance"], "related_concepts": ["light_wave"], "context_terms": ["pitch", "frequency", "echo"], "themes": ["Sound & Speech", "Cosmic Vibration"]}
                    ]
                }
            ]
        },
        {
            "id": "astronomy",
            "name": "Astronomy",
            "description": "Scientific study of stars, planets, celestial bodies, and cosmic evolution.",
            "subdomains": [
                {
                    "id": "astrophysics",
                    "name": "Astrophysics & Planetary Science",
                    "concepts": [
                        {"id": "astrophysics_concept", "name": "Astrophysics", "tamil_name": "விண்வெளி இயற்பியல்", "definition": "Branch of astronomy applying physical laws to stars, galaxies, and celestial phenomena.", "keywords": ["astrophysics", "vinveli iyarpiyal", "stars", "galaxies", "cosmos", "vinveli"], "related_concepts": ["stellar_evolution", "cosmology"], "context_terms": ["celestial mechanics", "radiation", "stars"], "themes": ["Cosmic Order", "Stars & Sun"]},
                        {"id": "stellar_evolution", "name": "Stellar Evolution", "tamil_name": "விண்மீன் வளர்ச்சி", "definition": "The lifecycle of a star from interstellar dust collapse to stellar death.", "keywords": ["stellar evolution", "star lifecycle", "vinmeen", "supernova"], "related_concepts": ["astrophysics_concept"], "context_terms": ["nuclear fusion", "nebula"], "themes": ["Birth & Renewal"]},
                        {"id": "cosmology", "name": "Cosmology", "tamil_name": "அண்டவியல்", "definition": "Study of the origin, large-scale structure, and evolution of the universe.", "keywords": ["cosmology", "andaviyal", "big bang", "universe expansion"], "related_concepts": ["astrophysics_concept"], "context_terms": ["infinite expanse", "origin of world"], "themes": ["Cosmic Creation", "Infinite Universe"]},
                        {"id": "solar_radiation", "name": "Solar Energy & Sun", "tamil_name": "சூரிய ஆற்றல்", "definition": "Radiant light and heat from the Sun empowering planetary weather and photosynthesis.", "keywords": ["sun", "solar energy", "sooriyan", "sunlight", "radiant heat"], "related_concepts": ["light_wave"], "context_terms": ["sun rays", "daylight", "dawn"], "themes": ["Sun as Source of Life"]},
                        {"id": "lunar_phases", "name": "Lunar Cycle & Tides", "tamil_name": "சந்திர சுழற்சியும் அலைகளும்", "definition": "Periodic orbit of the Moon around Earth producing phases and oceanic tides.", "keywords": ["moon", "lunar cycle", "chandiran", "tides", "thingal"], "related_concepts": ["gravity"], "context_terms": ["moonlight", "tides", "waxing waning"], "themes": ["Moonlight & Coolness"]}
                    ]
                }
            ]
        },
        {
            "id": "environment",
            "name": "Environment",
            "description": "Scientific study of ecosystems, climate systems, water cycles, and ecological balance.",
            "subdomains": [
                {
                    "id": "hydrology",
                    "name": "Hydrology & Ecosystems",
                    "concepts": [
                        {"id": "water_cycle", "name": "Water Cycle", "tamil_name": "நீர்ச் சுழற்சி", "definition": "Continuous natural circulation of water through evaporation, condensation, and precipitation.", "keywords": ["water cycle", "rain", "precipitation", "evaporation", "neer suzharchi", "mazhai", "marii", "water"], "related_concepts": ["atmosphere", "ecological_balance"], "context_terms": ["clouds", "rain", "life sustenance", "rivers", "monsoon"], "themes": ["Rain as Universal Nurturer", "Vaan Chirappu"]},
                        {"id": "atmosphere", "name": "Atmosphere & Wind", "tamil_name": "வளிமண்டலம் மற்றும் காற்று", "definition": "Layer of gases enveloping Earth that protects life and generates weather.", "keywords": ["atmosphere", "air", "wind", "valimandalam", "kaatru"], "related_concepts": ["water_cycle"], "context_terms": ["breeze", "gales", "atmospheric pressure"], "themes": ["Air & Breath"]},
                        {"id": "ecological_balance", "name": "Ecological Balance", "tamil_name": "சூழ்நிலைச் சமநிலை", "definition": "Dynamic equilibrium within an ecosystem maintaining biodiversity and natural order.", "keywords": ["ecological balance", "soozhnilai samanilai", "ecosystem", "nature preservation"], "related_concepts": ["water_cycle"], "context_terms": ["natural harmony", "preservation of species"], "themes": ["Harmony with Nature"]},
                        {"id": "climate_seasons", "name": "Seasons & Weather Dynamics", "tamil_name": "பருவகால மாற்றங்கள்", "definition": "Cyclical seasonal shifts in weather patterns driven by planetary tilt and solar radiation.", "keywords": ["seasons", "weather", "paruvakaalam", "monsoon", "climate"], "related_concepts": ["water_cycle"], "context_terms": ["summer", "rainy season", "winter coolness"], "themes": ["Seasonal Rhythms"]}
                    ]
                }
            ]
        },
        {
            "id": "agriculture",
            "name": "Agriculture",
            "description": "Science and practice of cultivating crops, soil enrichment, irrigation, and food production.",
            "subdomains": [
                {
                    "id": "agronomy",
                    "name": "Agronomy & Soil Management",
                    "concepts": [
                        {"id": "crop_cultivation", "name": "Crop Cultivation & Farming", "tamil_name": "உழவுத் தொழில்", "definition": "Agricultural tilling, seed sowing, crop management, and harvesting.", "keywords": ["agriculture", "farming", "crop cultivation", "uzhavu", "uzhavu thozhil", "farmer", "plowing"], "related_concepts": ["soil_health", "water_cycle"], "context_terms": ["plow", "harvest", "grain", "food supply"], "themes": ["Uzhavu (Agriculture)", "World Foundation"]},
                        {"id": "soil_health", "name": "Soil Health & Fertility", "tamil_name": "மண் வளம்", "definition": "Physical, chemical, and biological quality of soil to sustain crop yield.", "keywords": ["soil health", "soil fertility", "man valam", "earth enrichment"], "related_concepts": ["crop_cultivation"], "context_terms": ["tillage", "nutrient richness", "fertile earth"], "themes": ["Fertile Soil"]},
                        {"id": "irrigation", "name": "Irrigation & Water Management", "tamil_name": "நீர்ப்பாசன மேலாண்மை", "definition": "Controlled application of water to agricultural land through canals and reservoirs.", "keywords": ["irrigation", "water management", "neer paasanam", "canal", "lake storage"], "related_concepts": ["water_cycle", "crop_cultivation"], "context_terms": ["reservoirs", "bunds", "channel flow"], "themes": ["Water Storage & Canals"]}
                    ]
                }
            ]
        },
        {
            "id": "biology",
            "name": "Biology",
            "description": "Scientific study of living organisms, life functions, cellular processes, and botanical life.",
            "subdomains": [
                {
                    "id": "life_science",
                    "name": "Life & Botany",
                    "concepts": [
                        {"id": "life_sustenance", "name": "Life Sustenance & Respiration", "tamil_name": "உயிரியல் வாழ்வாதாரம்", "definition": "Metabolic and respiratory functions required to sustain cellular biological life.", "keywords": ["life sustenance", "vital force", "uyir", "respiration", "homeostasis"], "related_concepts": ["plant_biology"], "context_terms": ["breath of life", "vital organ", "living breath"], "themes": ["Sacredness of Life", "Ahimsa"]},
                        {"id": "plant_biology", "name": "Plant Biology & Flora", "tamil_name": "தாவர இயல்", "definition": "Biological structure, growth, and energy production of plants.", "keywords": ["plant biology", "botany", "taavara iyarpiyal", "flora", "greenery", "trees"], "related_concepts": ["crop_cultivation"], "context_terms": ["leaves", "blossom", "roots", "sap"], "themes": ["Flourishing Flora"]},
                        {"id": "biodiversity", "name": "Biodiversity & Animal Life", "tamil_name": "உயிரினப் பன்மை", "definition": "Variety of living species, ecosystems, and animal life in a habitat.", "keywords": ["biodiversity", "animal life", "uyirina panmai", "creatures", "fauna"], "related_concepts": ["life_sustenance"], "context_terms": ["living species", "birds", "beasts", "aquatic life"], "themes": ["Compassion to All Living Beings"]}
                    ]
                }
            ]
        },
        {
            "id": "medicine",
            "name": "Medicine",
            "description": "Science of healthcare, diagnosis, disease prevention, pharmacology, and dietary balance.",
            "subdomains": [
                {
                    "id": "healthcare",
                    "name": "Healthcare & Medical Practice",
                    "concepts": [
                        {"id": "preventive_medicine", "name": "Preventive Healthcare & Diagnosis", "tamil_name": "மருத்துவம் மற்றும் நோய் தடுப்பு", "definition": "Diagnosis of root causes of disease, balancing bodily humors, and prescribing remedies.", "keywords": ["medicine", "maruthuvam", "healthcare", "disease prevention", "marunthu", "diagnosis"], "related_concepts": ["dietary_health"], "context_terms": ["fourfold medical treatment", "physician skill", "remedy"], "themes": ["Marunthu Chapter", "Root Cause Diagnosis"]},
                        {"id": "dietary_health", "name": "Nutritional Science & Moderation", "tamil_name": "உணவுக் கட்டுப்பாடு", "definition": "Balancing food intake and metabolic digestion to preserve physical health.", "keywords": ["nutrition", "dietetics", "unavu", "digestion", "measured eating"], "related_concepts": ["preventive_medicine"], "context_terms": ["digestive fire", "measured food", "avoiding gluttony"], "themes": ["Healthy Eating", "Moderation in Food"]},
                        {"id": "hygiene_sanitation", "name": "Hygiene & Bodily Cleanliness", "tamil_name": "தூய்மையும் சுகாதாரமும்", "definition": "Practices maintaining physical cleanliness to prevent infection and promote health.", "keywords": ["hygiene", "sanitation", "thooymai", "cleanliness", "bodily purity"], "related_concepts": ["preventive_medicine"], "context_terms": ["bathing", "pure water", "external purity"], "themes": ["Physical Cleanliness"]}
                    ]
                }
            ]
        },
        {
            "id": "computer_science",
            "name": "Computer Science",
            "description": "Study of information, logic, formal reasoning, knowledge representation, and communication.",
            "subdomains": [
                {
                    "id": "information_theory",
                    "name": "Information & Reasoning",
                    "concepts": [
                        {"id": "knowledge_representation", "name": "Knowledge & Logical Reasoning", "tamil_name": "அறிவுடைமை மற்றும் பகுத்தறிவு", "definition": "Formal organization of knowledge, analytical inference, and discerning truth from evidence.", "keywords": ["knowledge", "logic", "arivu", "reasoning", "truth perception", "meyyunarvu"], "related_concepts": ["communication_speech"], "context_terms": ["discernment", "flawless intellect", "truth seeking"], "themes": ["Arivudaimai", "True Knowledge"]},
                        {"id": "communication_speech", "name": "Information Exchange & Rhetoric", "tamil_name": "சொல்லாட்சி மற்றும் தகவல் பரிமாற்றம்", "definition": "Transmission of clear, precise communication while minimizing noise.", "keywords": ["communication", "speech", "sollatchi", "rhetoric", "information transmission"], "related_concepts": ["knowledge_representation"], "context_terms": ["flawless words", "concise message", "clarity of expression"], "themes": ["Power of Words", "Eloquence"]}
                    ]
                }
            ]
        },
        {
            "id": "psychology",
            "name": "Psychology",
            "description": "Scientific study of human cognition, emotional self-regulation, perception, and moral ethics.",
            "subdomains": [
                {
                    "id": "cognition",
                    "name": "Cognitive Regulation & Ethics",
                    "concepts": [
                        {"id": "moral_cognition", "name": "Moral Cognition & Self-Control", "tamil_name": "மனக்கட்டுப்பாடு மற்றும் அறநெறி", "definition": "Psychological self-regulation, impulse restraint, and ethical decision-making.", "keywords": ["psychology", "ethics", "mind control", "self-control", "manam", "araneri", "restraint"], "related_concepts": ["knowledge_representation"], "context_terms": ["pure mind", "emotional stability", "restraint of desires"], "themes": ["Self-Control", "Moral Excellence"]},
                        {"id": "perception_truth", "name": "Perception & Epistemology", "tamil_name": "மெய்யுணர்வு (Perception of Reality)", "definition": "Cognitive ability to look beyond superficial appearances to grasp objective truth.", "keywords": ["perception", "epistemology", "meyyunarvu", "reality", "truth perception"], "related_concepts": ["knowledge_representation"], "context_terms": ["grasping reality", "unbiased observation"], "themes": ["Perception of Truth"]}
                    ]
                }
            ]
        }
    ]

    kb = {
        "version": "0.2.0",
        "domains": domains
    }

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)
    print(f"Updated KB with {sum(len(sub['concepts']) for d in domains for sub in d['subdomains'])} concepts across {len(domains)} domains!")

if __name__ == "__main__":
    build_comprehensive_kb()

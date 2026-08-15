"""
Enhanced NLP Processor
- Keyword-first intent detection (ordered by specificity)
- Context carry-forward from previous turn
- Normalised course aliases (b tech → btech, etc.)
- Year mention detection (1st/2nd/3rd/4th year → ignored for fees, just context)
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


class NLPProcessor:
    def __init__(self):
        self.intent_examples = {
            "greeting":         ["hi", "hello", "hey", "good morning", "good afternoon",
                                 "hii", "hello there", "hi there"],
            "farewell":         ["bye", "goodbye", "see you", "see ya", "take care", "later"],
            "thanks":           ["thank you", "thanks", "thanks a lot", "thank u", "thx",
                                 "great thanks", "appreciate it"],
            "department_info":  ["tell me about cse department", "what are the branches",
                                 "departments in college", "details of ece",
                                 "computer science branch", "which departments are there",
                                 "show me all departments", "info about aiml"],
            "course_info":      ["what courses are offered", "is btech available",
                                 "mtech courses", "tell me about mba", "ug programs",
                                 "pg programs", "which courses does the college offer"],
            "fee_info":         ["what is the fee structure", "btech fees", "fees for btech",
                                 "how much does mba cost", "hostel fee", "management quota fees",
                                 "fee details", "annual fee", "tuition fee", "how much is the fee",
                                 "fee for cse", "fee for ece", "fees", "cost of course"],
            "admission_info":   ["how to get admission", "admission process",
                                 "eamcet rank required", "lateral entry eligibility",
                                 "management quota admission", "how to apply", "eligibility criteria",
                                 "how to join", "enrollment process", "tg eapcet", "eamcet"],
            "placement_info":   ["how are the placements", "highest package", "average salary",
                                 "top recruiters", "companies visiting", "placement statistics",
                                 "job offers", "placement record", "who recruits"],
            "facility_info":    ["what facilities are there", "is there a hostel",
                                 "library details", "sports facilities", "campus infrastructure",
                                 "gym", "canteen", "wifi", "transport", "lab facilities"],
            "scholarship_info": ["any scholarships available", "fee reimbursement",
                                 "sports quota concession", "financial aid",
                                 "epass scholarship", "merit scholarship"],
            "event_info":       ["college events", "technical fest", "cultural fest",
                                 "prazasti", "samisti", "annual fest", "hackathon",
                                 "what events are held"],
            "contact_info":     ["where is the college located", "contact number",
                                 "email address", "college address", "phone number",
                                 "how to reach", "location", "directions"],
            "college_info":     ["tell me about the college", "is it autonomous",
                                 "naac grade", "college code", "establishment year",
                                 "about sphoorthy", "overview of college", "founded when"],
            "management_info":  ["who is the principal", "chairman of college",
                                 "director", "management details", "who manages the college",
                                 "principal name", "who is ceo"],
            "hod_info":         ["who is the hod of cse", "ece hod", "head of department",
                                 "hod name", "who heads the department"],
            "club_info":        ["student clubs", "extra curricular activities",
                                 "technical club", "sports club", "what clubs are there",
                                 "student activities", "cultural club"],
        }

        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.training_sentences = []
        self.training_intents = []

        for intent, examples in self.intent_examples.items():
            for example in examples:
                self.training_sentences.append(example)
                self.training_intents.append(intent)

        self.tfidf_matrix = self.vectorizer.fit_transform(self.training_sentences)

        # Ordered longest-match-first so "computer science" beats "cs"
        self.dept_mapping = {
            "computer science and engineering": "cse",
            "computer science": "cse",
            "artificial intelligence and machine learning": "cse_aiml",
            "artificial intelligence": "cse_aiml",
            "ai and machine learning": "cse_aiml",
            "ai & machine learning": "cse_aiml",
            "ai & ml": "cse_aiml",
            "machine learning": "cse_aiml",
            "ai ml": "cse_aiml",
            "aiml": "cse_aiml",
            "data science": "cse_ds",
            "cyber security": "cse_cs",
            "cybersecurity": "cse_cs",
            "cyber": "cse_cs",
            "electronics and communication": "ece",
            "electronics": "ece",
            "civil engineering": "ce",
            "civil": "ce",
            "mechanical engineering": "me",
            "mechanical": "me",
            "mech": "me",
            "cse": "cse",
            "ece": "ece",
            "mba": "mba",
        }

        # Keyword signals keyed by intent — evaluated IN ORDER (most specific first)
        # Tuple: (intent, list_of_trigger_words)
        self._keyword_rules = [
            ("farewell",        ["bye", "goodbye", "see you", "take care"]),
            ("thanks",          ["thank you", "thanks", "thank u", "thx"]),
            ("greeting",        ["hello", "hi ", "hey ", "hii"]),
            ("scholarship_info",["scholarship", "epass", "fee reimbursement", "financial aid"]),
            ("placement_info",  ["placement", "package", "salary", "recruiter", "lpa", "ctc", "offer"]),
            ("admission_info",  ["admission", "join", "enroll", "eligibility", "eamcet", "eapcet",
                                  "lateral entry", "apply", "how to get in"]),
            ("facility_info",   ["hostel", "library", "sports", "gym", "canteen", "wifi",
                                  "transport", "bus", "infrastructure"]),
            ("event_info",      ["event", "fest", "prazasti", "samisti", "hackathon", "cultural"]),
            ("contact_info",    ["contact", "address", "location", "phone", "email", "reach"]),
            ("college_info",    ["naac", "autonomous", "aicte", "jntuh", "established", "founded",
                                  "about college", "about sphoorthy"]),
            ("management_info", ["principal", "chairman", "director", "secretary", "ceo", "management"]),
            ("hod_info",        ["hod", "head of department"]),
            ("club_info",       ["club", "extracurricular", "extra curricular", "society"]),
            # fee AFTER placement/admission so "fee reimbursement" doesn't steal fee
            ("fee_info",        ["fee", "cost", "price", "tuition", "charges", "fees"]),
            ("department_info", ["department", "branch", "branches", "dept"]),
            ("course_info",     ["course", "program", "btech", "mtech", "b.tech", "m.tech",
                                  "ug ", "pg ", "undergraduate", "postgraduate"]),
        ]

    # ── Intent classification ────────────────────────────────────────────────
    def classify_intent(self, text, context=None):
        text_lower = text.lower().strip()
        ctx_intent = (context or {}).get('lastIntent')

        # 1. Short follow-up (≤4 words) — try keywords first, then inherit context
        if len(text_lower.split()) <= 4 and ctx_intent:
            for intent, keywords in self._keyword_rules:
                for kw in keywords:
                    if kw in text_lower:
                        return intent
            # No strong keyword hit → stay on the same topic
            return ctx_intent

        # 2. Keyword rules in priority order (longer texts)
        for intent, keywords in self._keyword_rules:
            for kw in keywords:
                if kw in text_lower:
                    return intent

        # 3. TF-IDF similarity with confidence threshold
        try:
            vec = self.vectorizer.transform([text_lower])
            sims = cosine_similarity(vec, self.tfidf_matrix)[0]
            max_idx = int(sims.argmax())
            score = float(sims[max_idx])
            if score > 0.25:
                return self.training_intents[max_idx]
            # Low confidence + we have prior context → inherit it
            if ctx_intent and score > 0.05:
                return ctx_intent
        except Exception:
            pass

        return ctx_intent if ctx_intent else "general_query"

    # ── Entity extraction ────────────────────────────────────────────────────
    def extract_entities(self, text, context=None):
        entities = {}
        ctx = context or {}
        # Normalise common aliases
        text_lower = text.lower()
        text_lower = re.sub(r'\bb[\s\.]?tech\b', 'btech', text_lower)
        text_lower = re.sub(r'\bm[\s\.]?tech\b', 'mtech', text_lower)

        # ── Department (longest match first) ────────────────────────────────
        for key in sorted(self.dept_mapping, key=len, reverse=True):
            if re.search(r'\b' + re.escape(key) + r'\b', text_lower):
                entities['department'] = self.dept_mapping[key]
                break

        # ── Course ──────────────────────────────────────────────────────────
        course_patterns = [
            (r'\bbtech\b', 'btech'),
            (r'\bmtech\b', 'mtech'),
            (r'\bmba\b',   'mba'),
            (r'\bdiploma\b', 'diploma'),
            (r'\blateral entry\b', 'btech'),   # lateral → btech context
        ]
        for pattern, label in course_patterns:
            if re.search(pattern, text_lower):
                entities['course'] = label
                break

        # ── Year mention (informational, stored but not used to filter fees) ─
        year_match = re.search(r'\b([1-4](?:st|nd|rd|th)?\s*year|year\s*[1-4])\b', text_lower)
        if year_match:
            entities['year'] = year_match.group(0)

        # ── Context carry-forward ────────────────────────────────────────────
        # If user didn't mention a dept/course but the last turn had one, inherit it
        if 'department' not in entities and ctx.get('lastDept'):
            entities['department'] = ctx['lastDept']
        if 'course' not in entities and ctx.get('lastCourse'):
            entities['course'] = ctx['lastCourse']

        return entities

    # ── Public API ───────────────────────────────────────────────────────────
    def process(self, text, context=None):
        intent   = self.classify_intent(text, context)
        entities = self.extract_entities(text, context)
        return {'intent': intent, 'entities': entities}

import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas for dynamic total page count, academic headers, and footers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 11 * inch - 36, "Algorithms & Methods Technical Specification | KG-RAG Campus System")
            self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "Sphoorthy Engineering College")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.6)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
        
        # Running Footer Line & Text
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.6)
        self.line(54, 46, 8.5 * inch - 54, 46)

        self.drawString(54, 32, "Major Project | Department of Computer Science & Engineering")
        text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 32, text)
        self.restoreState()

def build_pdf(filename="Algorithms_and_Methods_Report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Premium Color Palette
    c_primary = colors.HexColor("#0f172a")    # Slate 900 (Dominant Heading)
    c_secondary = colors.HexColor("#0369a1")  # Rich Cyan/Blue 700 (Subheading)
    c_accent = colors.HexColor("#0d9488")     # Teal 600 (Accents/Highlights)
    c_body = colors.HexColor("#334155")       # Slate 700 (Body text)
    c_border = colors.HexColor("#cbd5e1")     # Slate 300 (Dividers & borders)
    c_bg_light = colors.HexColor("#f8fafc")   # Slate 50 (Table alternating fill)
    c_callout_bg = colors.HexColor("#f0fdf4") # Emerald 50 (Callout background)
    c_callout_box = colors.HexColor("#10b981")# Emerald 500 (Callout border)

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=21,
        leading=25,
        textColor=c_primary,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14.5,
        textColor=c_secondary,
        spaceAfter=12
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_body,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=12,
        bulletIndent=4,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderPadding=5,
        spaceAfter=6
    )

    table_header = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell = ParagraphStyle(
        'TC',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_body
    )

    table_cell_bold = ParagraphStyle(
        'TCB',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=c_primary
    )

    table_cell_code = ParagraphStyle(
        'TCCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#0f172a")
    )

    story = []

    # =========================================================================
    # COVER / HEADER SECTION
    # =========================================================================
    story.append(Paragraph("Algorithms & Methods Technical Specification", title_style))
    story.append(Paragraph("Mathematical Formulations, Data Structures, Complexity Analysis & Procedural Workflows", subtitle_style))
    story.append(Paragraph("<b>Project:</b> Knowledge Graph-Based Question Answering System for Efficient Information Retrieval<br/>"
                           "<b>Department:</b> Computer Science & Engineering | <b>Institution:</b> Sphoorthy Engineering College", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_secondary, spaceBefore=0, spaceAfter=10))

    # Executive Summary Card
    exec_text = (
        "<b>Architectural Abstract:</b> This report details the complete computational framework powering the "
        "Knowledge Graph Question Answering (KGQA) system. The solution fuses <b>Vector Space NLP</b> (TF-IDF with "
        "Cosine Similarity), <b>Gestalt Pattern Fuzzy Matching</b> (Levenshtein distance), <b>Deterministic Directed "
        "Graph Traversal</b> (NetworkX Multi-Hop Search over 422+ nodes), <b>Real-Time In-Memory Graph Delta "
        "Synchronization</b>, and <b>Cryptographic Authentication</b> (PBKDF2-HMAC-SHA256). Together, these algorithms "
        "provide sub-150ms query resolution with <b>0% factual hallucination</b>, establishing a verifiable campus information hub."
    )
    summary_table = Table([[Paragraph(exec_text, body_style)]], colWidths=[504])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_callout_bg),
        ('BOX', (0,0), (-1,-1), 1, c_callout_box),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 9),
        ('RIGHTPADDING', (0,0), (-1,-1), 9),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 1: NLP & QUERY RESOLUTION ALGORITHMS
    # =========================================================================
    story.append(Paragraph("1. Natural Language Processing & Query Understanding Pipeline", h1_style))
    story.append(Paragraph(
        "User inquiries arrive as unstructured, conversational natural language strings. The NLP engine translates these queries "
        "into structured graph query intents using a three-stage hybrid classification pipeline.", body_style
    ))

    story.append(Paragraph("1.1 Term Frequency - Inverse Document Frequency (TF-IDF) Vectorization", h2_style))
    story.append(Paragraph(
        "The system maps both user queries and corpus training exemplars into a high-dimensional continuous vector space. "
        "The mathematical formulation implemented via scikit-learn is as follows:", body_style
    ))
    story.append(Paragraph(
        "<b>Term Frequency:</b> TF(t, d) = f(t, d) / ∑ f(t', d)<br/>"
        "<b>Inverse Document Frequency:</b> IDF(t, D) = ln((1 + |D|) / (1 + |{d ∈ D : t ∈ d}|)) + 1<br/>"
        "<b>TF-IDF Weight:</b> W(t, d) = TF(t, d) × IDF(t, D), followed by Euclidean L2 normalization: v_norm = v / ||v||₂",
        code_style
    ))
    story.append(Paragraph(
        "This assigns high diagnostic weights to domain-specific tokens (e.g. <i>'tuition'</i>, <i>'syllabus'</i>, <i>'hod'</i>, <i>'curriculum'</i>) "
        "while automatically penalizing ubiquitous stopwords without degrading context.", body_style
    ))

    story.append(Paragraph("1.2 Cosine Similarity Vector Space Classification", h2_style))
    story.append(Paragraph(
        "For an incoming query vector <b>q</b> and class prototype exemplar vectors <b>x_c</b> across 18 distinct intent categories, "
        "the similarity score is computed via the dot product of normalized vectors:", body_style
    ))
    story.append(Paragraph(
        "Cosine_Similarity(q, x_c) = (q · x_c) / (||q||₂ × ||x_c||₂) = ∑ (q_i × x_{c,i})<br/>"
        "Predicted Intent: ŷ = argmax_c [Cosine_Similarity(q, x_c)], with Confidence Threshold τ = 0.25",
        code_style
    ))
    story.append(Paragraph(
        "If max similarity drops below threshold τ, the query falls back to contextual inference or generalized entity keyword search.", body_style
    ))

    story.append(Paragraph("1.3 Ratcliff/Obershelp & Levenshtein Fuzzy String Matching", h2_style))
    story.append(Paragraph(
        "To resolve colloquial student typos, slang, and abbreviations (e.g., <i>'computr scince'</i> → <i>'CSE'</i>, <i>'artifical intel'</i> → <i>'AIML'</i>), "
        "the engine implements the Gestalt Pattern Matching algorithm via Python's <code>difflib.get_close_matches</code>:", body_style
    ))
    story.append(Paragraph(
        "Similarity_Ratio(s1, s2) = (2 × |M|) / (|s1| + |s2|)<br/>"
        "where M is the sum of characters in matching contiguous substrings. Cutoff parameter is set to 0.80.",
        code_style
    ))
    story.append(Paragraph(
        "This resolves spelling errors in department titles, building names, and faculty names before graph dispatch.", body_style
    ))

    story.append(Paragraph("1.4 Regular Expression Named Entity Recognition (NER)", h2_style))
    story.append(Paragraph(
        "Deterministic entity extraction utilizes pre-compiled regular expression patterns to isolate structured parameters:", body_style
    ))
    story.append(Paragraph(
        "• <b>Faculty Entity:</b> <code>(?:Dr\\.|Prof\\.|Mr\\.|Mrs\\.|Ms\\.)\\s+[A-Z][a-z]+(?:\\s+[A-Z][a-z]+)*</code><br/>"
        "• <b>Course Entity:</b> <code>\\b(?:b\\.?tech|m\\.?tech|mba|diploma|lateral\\s+entry)\\b</code><br/>"
        "• <b>Semester Entity:</b> <code>(?:semester|sem)\\s*(\\d+)|(\\d+)(?:st|nd|rd|th)\\s*sem</code><br/>"
        "• <b>Infrastructure Entity:</b> <code>(?:block|building)\\s*([a-d])|(?:room|lab)\\s*(\\d+)</code>",
        code_style
    ))

    story.append(Paragraph("1.5 Two-Tier Context-Aware Dialogue State Tracking", h2_style))
    story.append(Paragraph(
        "For short follow-up prompts (length ≤ 4 tokens, e.g. <i>'what about fees?'</i> or <i>'who is the HOD?'</i>), "
        "the classifier applies a state-inheritance algorithm. It retains the previously active Department or Course entity "
        "from session context, eliminating repetitive contextual re-prompting by the user.", body_style
    ))

    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 2: KNOWLEDGE GRAPH MODELING ALGORITHMS
    # =========================================================================
    story.append(Paragraph("2. Knowledge Graph Modeling & Construction Algorithms", h1_style))
    story.append(Paragraph(
        "The campus knowledge base is structured as a formal Typed Directed Multigraph G = (V, E, τ_v, τ_e) modeled in NetworkX. "
        "It entirely eliminates pseudo-random heuristic linking in favor of deterministic ontological validation.", body_style
    ))

    # Table of Entities and Relations
    ont_data = [
        ["Layer", "Entity Types (τ_v)", "Formal Relationships (τ_e)", "Validation Invariant"],
        ["Academic Org", "College, Department, Management, HOD", "has_department, has_hod, reports_to", "1 HOD per Department; exact 1:1 mapping"],
        ["Curriculum", "Program, Semester, Subject, Course", "offers_subject, has_semester, has_program", "Subjects partitioned by Semesters 1-8"],
        ["Faculty", "Faculty, ResearchArea", "teaches, specializes_in, member_of", "Deterministic faculty-subject assignments"],
        ["Infrastructure", "Building, Floor, Room, Lab", "has_building, has_room, housed_in, located_on", "Strict hierarchical physical containment"],
        ["Administration", "Fee, Admission, Placement, Scholarship", "has_fee, requires_admission, recruited_by", "Deterministic eligibility & fee records"]
    ]
    t_ont = Table([[Paragraph(f"<b>{c}</b>", table_header) for c in ont_data[0]]] +
                  [[Paragraph(r[0], table_cell_bold), Paragraph(r[1], table_cell), Paragraph(r[2], table_cell_code), Paragraph(r[3], table_cell)] for r in ont_data[1:]],
                  colWidths=[80, 140, 144, 140])
    t_ont.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('BACKGROUND', (0,1), (-1,1), colors.white),
        ('BACKGROUND', (0,2), (-1,2), c_bg_light),
        ('BACKGROUND', (0,3), (-1,3), colors.white),
        ('BACKGROUND', (0,4), (-1,4), c_bg_light),
        ('BACKGROUND', (0,5), (-1,5), colors.white),
    ]))
    story.append(t_ont)
    story.append(Spacer(1, 8))

    story.append(Paragraph("2.1 Topological Construction Pipeline", h2_style))
    story.append(Paragraph(
        "The graph is constructed via a staged deterministic sequence: College Root → Management/Admin → Departments & HODs → "
        "Academic Programs → Semesters (1–8) → Course Subjects → Physical Infrastructure (Buildings → Floors → Rooms → Labs) → "
        "Faculty Rosters → Faculty Assignment Matching. Every insertion validates edge typing against <code>RELATIONSHIP_RULES</code>.", body_style
    ))

    story.append(Paragraph("2.2 Automated Ontological Consistency Validator", h2_style))
    story.append(Paragraph(
        "Implemented in <code>knowledge_graph/er_schema.py</code>, the validation function <code>validate_graph_against_schema(G)</code> "
        "verifies every node v ∈ V for required property existence and inspects every directed edge (u, v) ∈ E: "
        "(τ_v(u), τ_v(v)) must match the allowed domain and range for relation τ_e((u, v)). Any deviation triggers an immediate schema exception.", body_style
    ))

    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 3: DETERMINISTIC MULTI-HOP RETRIEVAL ALGORITHMS
    # =========================================================================
    story.append(Paragraph("3. Multi-Hop Graph Traversal & Graph-RAG Retrieval Engine", h1_style))
    story.append(Paragraph(
        "Unlike generative language models that synthesize probabilistic guesses, this engine traverses explicit relational edges, "
        "guaranteeing <b>100% verifiable factual grounding</b> with zero hallucination.", body_style
    ))

    story.append(Paragraph("3.1 Multi-Hop Path Navigation Algorithm", h2_style))
    story.append(Paragraph(
        "Complex institutional queries require navigating through sequential semantic relations. The traversal engine executes "
        "breadth-first successor exploration over directed edge labels:", body_style
    ))
    story.append(Paragraph(
        "<b>Multi-Hop Query Example:</b> <i>'Where does Dr. Ramarao lecture for Operating Systems?'</i><br/>"
        "Path Traversal: Faculty('Dr. Ramarao') ──teaches──► Subject('CS501_OS') ──offered_in──► Room('Lab_201') ──located_on──► Building('Block_A')<br/>"
        "Mathematical Filtering: N⁺(u, r) = { v ∈ V | (u, v) ∈ E ∧ τ_e((u, v)) = r }",
        code_style
    ))

    story.append(Paragraph("3.2 Subgraph Neighborhood Query Methods", h2_style))
    story.append(Paragraph(
        "Over 15 dedicated traversal algorithms are implemented in <code>knowledge_graph/kg_query.py</code>:", body_style
    ))
    story.append(Paragraph(
        "• <code>query_department(name)</code>: Traverses Department → HOD, Faculty, Programs, Labs, and Recruiters.<br/>"
        "• <code>query_faculty_profile(name)</code>: Collects outgoing <i>teaches</i>, <i>specializes_in</i>, and incoming <i>housed_in</i> edges.<br/>"
        "• <code>query_building(name)</code>: Traverses Building → Floors → Rooms → Department occupancy.<br/>"
        "• <code>query_subjects_by_semester(dept, sem)</code>: Performs two-hop traversal Dept → Semester → Subjects.",
        bullet_style
    ))

    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 4: REAL-TIME IN-MEMORY GRAPH SYNCHRONIZATION
    # =========================================================================
    story.append(Paragraph("4. Real-Time Dynamic In-Memory Graph Synchronization", h1_style))
    story.append(Paragraph(
        "A critical limitation in existing academic KGQA literature is the static assumption (graphs requiring offline rebuilds). "
        "Our system implements a real-time hot-reloading architecture for zero-downtime updates.", body_style
    ))

    story.append(Paragraph("4.1 Atomic Memory Swap Synchronization Pipeline", h2_style))
    story.append(Paragraph(
        "1. <b>Admin Mutation Event:</b> Non-technical staff adds, updates, or deletes an entity (notice, fee, faculty, course) via Web CRUD.<br/>"
        "2. <b>Transactional Persistence:</b> The record is committed atomically to the SQLite / relational database.<br/>"
        "3. <b>Active Worker Sync:</b> The route handler invokes <code>current_app.kg_builder.build_graph()</code>.<br/>"
        "4. <b>Atomic Graph Reference Swap:</b> The active in-memory DiGraph pointer is atomically updated in the Flask application context.<br/>"
        "5. <b>Zero Downtime:</b> Subsequent user queries immediately traverse the newly updated topological nodes in < 15ms without server restart.",
        body_style
    ))

    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 5: SECURITY & ACCESS CONTROL ALGORITHMS
    # =========================================================================
    story.append(Paragraph("5. Cryptographic Authentication & Role-Based Access Control", h1_style))
    story.append(Paragraph(
        "Enterprise campus governance requires strict role segregation across Students, Faculty, and Administrators.", body_style
    ))

    story.append(Paragraph("5.1 Password Hashing via PBKDF2-HMAC-SHA256", h2_style))
    story.append(Paragraph(
        "User credentials are protected using the Password-Based Key Derivation Function 2 (PBKDF2) with SHA-256 HMAC (Werkzeug security):", body_style
    ))
    story.append(Paragraph(
        "Derived_Key = PBKDF2(PRF=HMAC-SHA256, Password=P, Salt=S, Iterations=600,000, KeyLength=32 bytes)",
        code_style
    ))
    story.append(Paragraph(
        "Cryptographically generated random 16-byte salts prevent rainbow table attacks, and 600,000 computational rounds resist hardware-accelerated brute forcing.", body_style
    ))

    story.append(Paragraph("5.2 Role-Based Access Control (RBAC) Lattice", h2_style))
    story.append(Paragraph(
        "Access permissions follow a formal hierarchical lattice: <b>Admin ⪰ Faculty ⪰ Student ⪰ Visitor</b>.<br/>"
        "Authorization Function: <code>Auth(user, action) = True iff Role(user) ≥ RequiredRole(action)</code>.<br/>"
        "Protected endpoints (such as <code>/admin/kg</code> and <code>/admin/users</code>) enforce this via Flask-Login session decorators.", body_style
    ))

    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 6: ALGORITHMIC COMPARISON & COMPLEXITY MATRIX
    # =========================================================================
    story.append(Paragraph("6. Algorithmic Complexity, Rationale & Comparative Evaluation", h1_style))
    story.append(Paragraph(
        "The following matrix summarizes the algorithms employed, their computational complexities, and their explicit operational advantages over baseline alternatives:", body_style
    ))

    comp_data = [
        ["Subsystem / Algorithm", "Input / Process", "Time Complexity", "Space Complexity", "Advantage over Alternative"],
        ["TF-IDF Vectorizer", "User query string (len n tokens)", "O(n × |V_vocab|)", "O(|V_vocab|)", "Zero cloud latency vs. 800ms API latency of external embedding APIs"],
        ["Cosine Similarity Classifier", "Query vector vs. 18 intent classes", "O(k × d)  [k=18, d=vocab]", "O(k × d)", "Deterministic classification; zero hallucination risk"],
        ["Gestalt Pattern Matching", "Mismatched entity token (len m, n)", "O(m × n) worst case", "O(m + n)", "Tolerates severe student typos without requiring neural re-training"],
        ["Regex Entity Extractor", "Raw text scan with compiled regex", "O(n) linear scan", "O(1) auxiliary", "Sub-millisecond parameter extraction for courses, sems, rooms"],
        ["Deterministic KG Builder", "Raw campus JSON (N entities)", "O(V + E) deterministic", "O(V + E) in RAM", "Strict ontological typing; zero stochastic connection noise"],
        ["Multi-Hop Graph Query", "Breadth-first relation traversal", "O(deg(u) × deg(v)) < 15ms", "O(V_subgraph)", "Exact factual ground truth vs. generative LLM hallucinations"],
        ["Dynamic In-Memory Sync", "Admin mutation → Graph rebuild", "O(V + E) ~ 35ms", "O(V + E) in RAM", "Live updates without server restarts or application downtime"],
        ["PBKDF2-HMAC-SHA256", "User password + 16B salt", "O(C) [C=600,000 rounds]", "O(1) memory", "Industry standard resistant to GPU/ASIC rainbow attacks"]
    ]

    t_comp = Table([[Paragraph(f"<b>{c}</b>", table_header) for c in comp_data[0]]] +
                   [[Paragraph(r[0], table_cell_bold), Paragraph(r[1], table_cell), Paragraph(r[2], table_cell_code), Paragraph(r[3], table_cell_code), Paragraph(r[4], table_cell)] for r in comp_data[1:]],
                   colWidths=[100, 105, 95, 84, 120])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('BACKGROUND', (0,1), (-1,1), colors.white),
        ('BACKGROUND', (0,2), (-1,2), c_bg_light),
        ('BACKGROUND', (0,3), (-1,3), colors.white),
        ('BACKGROUND', (0,4), (-1,4), c_bg_light),
        ('BACKGROUND', (0,5), (-1,5), colors.white),
        ('BACKGROUND', (0,6), (-1,6), c_bg_light),
        ('BACKGROUND', (0,7), (-1,7), colors.white),
        ('BACKGROUND', (0,8), (-1,8), c_bg_light),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 12))

    # Concluding Technical Statement
    story.append(Paragraph(
        "<b>Conclusion:</b> By tightly harmonizing fast vector-space NLP, Gestalt fuzzy matching, deterministic ontological "
        "graph traversal, and live in-memory synchronization, this system achieves an optimal balance between conversational flexibility "
        "and mathematical certitude. It eliminates generative hallucination risks and operational API costs while delivering "
        "sub-150ms verified institutional answers across both web and mobile environments.",
        ParagraphStyle('Concl', parent=body_style, fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor("#475569"))
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report generated successfully: {filename}")

if __name__ == "__main__":
    output_pdf = "Algorithms_and_Methods_Report.pdf"
    if len(sys.argv) > 1:
        output_pdf = sys.argv[1]
    build_pdf(output_pdf)

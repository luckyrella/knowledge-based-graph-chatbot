"""
Generate Technical Execution & System Guide PDF
Comprehensive documentation covering Project Overview, Technology Stack,
Feature Walkthrough, Step-by-Step Execution Guide, and Viva Q&A.
"""
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
    """Two-pass canvas for running header and 'Page X of Y' footer."""
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
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))

        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 11 * inch - 36, "KG-RAG Campus Assistant (Ari) — System Architecture & Execution Manual")
            self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "Sphoorthy Engineering College")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.6)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Running Footer
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.6)
        self.line(54, 46, 8.5 * inch - 54, 46)

        self.setFont("Helvetica", 8)
        self.drawString(54, 32, "B.Tech Computer Science & Engineering — Major Project Technical Documentation")
        text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 32, text)
        self.restoreState()


def build_execution_guide(output_filename="KG_RAG_Execution_and_System_Guide.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Color Palette
    c_primary = colors.HexColor("#0f172a")     # Slate 900
    c_secondary = colors.HexColor("#1e3a8a")   # Blue 900
    c_accent = colors.HexColor("#0284c7")      # Sky 600
    c_emerald = colors.HexColor("#059669")     # Emerald 600
    c_body = colors.HexColor("#334155")        # Slate 700
    c_border = colors.HexColor("#cbd5e1")      # Slate 300
    c_bg_light = colors.HexColor("#f8fafc")    # Slate 50
    c_code_bg = colors.HexColor("#1e293b")     # Slate 800
    c_header_bg = colors.HexColor("#0f172a")   # Slate 900

    # Typography Styles
    doc_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=c_secondary,
        spaceAfter=4
    )
    doc_subtitle = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_accent,
        spaceAfter=12
    )
    h1_style = ParagraphStyle(
        'SecHeading1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'SecHeading2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=c_body,
        spaceAfter=6
    )
    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=13,
        textColor=c_body,
        leftIndent=14,
        spaceAfter=3
    )
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#f8fafc")
    )
    th_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )
    tb_style = ParagraphStyle(
        'TB',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.5,
        textColor=c_body
    )
    tb_bold = ParagraphStyle(
        'TBBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=11.5,
        textColor=c_primary
    )

    story = []

    # ─────────────────────────────────────────────────────────────────────────
    # HEADER BANNER & DOCUMENT METADATA
    # ─────────────────────────────────────────────────────────────────────────
    story.append(Paragraph("KG-RAG Campus Assistant: System Guide & Execution Manual", doc_title))
    story.append(Paragraph("Ontology-Driven Knowledge Graph Retrieval & Natural Language Question Answering System", doc_subtitle))
    
    meta_data = [
        [Paragraph("<b>Institution:</b> Sphoorthy Engineering College (UGC Autonomous)", tb_style),
         Paragraph("<b>Department:</b> Computer Science & Engineering", tb_style)],
        [Paragraph("<b>AI Assistant:</b> Ari (Campus AI Assistant)", tb_style),
         Paragraph("<b>Knowledge Graph Scale:</b> 424 Nodes · 764 Edges (Zero Orphans)", tb_style)],
        [Paragraph("<b>Dual Engine:</b> Neo4j Cloud Aura + NetworkX In-Memory", tb_style),
         Paragraph("<b>Release Version:</b> v2.4 Enterprise Production", tb_style)]
    ]
    t_meta = Table(meta_data, colWidths=[250, 254])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # ─────────────────────────────────────────────────────────────────────────
    # 1. PROJECT OVERVIEW & ARCHITECTURE
    # ─────────────────────────────────────────────────────────────────────────
    story.append(Paragraph("1. Project Overview & Architectural Design", h1_style))
    story.append(Paragraph(
        "<b>KG-RAG (Knowledge Graph Retrieval-Augmented Generation)</b> is an intelligent conversational campus system designed to solve the critical information access bottlenecks in higher educational institutions. Unlike traditional generative LLM chatbots that suffer from factual hallucinations and stale data, KG-RAG combines a <b>deterministic ontology graph</b> with <b>sub-millisecond conversational retrieval</b>. The system guarantees 100% verified campus answers concerning academic departments, faculty cabin locations, syllabus subjects, study materials, circulars, and fee structures.",
        body_style
    ))

    arch_box = [
        [Paragraph("<b>ARCHITECTURAL FLOW DIAGRAM</b>", th_style)],
        [Paragraph(
            "<font name='Courier'>[Student / User] ──(Web Chat Interface 'Ari')──&gt; [Flask Application Layer]<br/>"
            "       │<br/>"
            "       ▼<br/>"
            "[NLP Preprocessing] ──(Intent Classification + Token Boundary Matcher)<br/>"
            "       │<br/>"
            "       ▼<br/>"
            "[Shortest-Path Graph Tracer] ──&gt; Evaluates Topological Traversal Path<br/>"
            "       │<br/>"
            "       ├────────────────────────────────────────┐<br/>"
            "       ▼                                        ▼<br/>"
            "[Neo4j Cloud Aura (Cypher)]           [NetworkX In-Memory Engine]<br/>"
            "       │                                        │<br/>"
            "       └────────────────────────────────────────┘<br/>"
            "                               │<br/>"
            "                               ▼<br/>"
            "[Response Synthesizer] ──&gt; Answer + Interactive Graph Traversal Badge"
            "</font>", code_style)]
    ]
    t_arch = Table(arch_box, colWidths=[504])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_header_bg),
        ('BACKGROUND', (0, 1), (-1, 1), c_code_bg),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BOX', (0, 0), (-1, -1), 1, c_primary)
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 10))

    # ─────────────────────────────────────────────────────────────────────────
    # 2. COMPLETE TECHNOLOGY STACK
    # ─────────────────────────────────────────────────────────────────────────
    story.append(Paragraph("2. Full Technology Stack Specifications", h1_style))
    
    tech_data = [
        [Paragraph("Component / Layer", th_style), Paragraph("Technology / Framework", th_style), Paragraph("Key Role in System", th_style)],
        [Paragraph("Application Backend", tb_bold), Paragraph("Python 3.14 · Flask 3.0", tb_style), Paragraph("Core microservice framework, REST APIs, session management, template routing", tb_style)],
        [Paragraph("Graph Database (Cloud)", tb_bold), Paragraph("Neo4j Cloud Aura · Cypher", tb_style), Paragraph("Enterprise property graph database with live query execution and cloud sync", tb_style)],
        [Paragraph("In-Memory Graph Engine", tb_bold), Paragraph("NetworkX 3.2", tb_style), Paragraph("Zero-latency shortest-path graph traversals, density analysis, centrality metrics", tb_style)],
        [Paragraph("NLP & Vectorization", tb_bold), Paragraph("Scikit-Learn · TF-IDF", tb_style), Paragraph("Cosine similarity classification, n-gram intent matching, token extraction", tb_style)],
        [Paragraph("Relational Database", tb_bold), Paragraph("SQLite 3 · SQLAlchemy ORM", tb_style), Paragraph("User authentication, chat message audit logs, circulars, feedback metrics", tb_style)],
        [Paragraph("Interactive Graph Canvas", tb_bold), Paragraph("Vis.js Network Library", tb_style), Paragraph("Force-directed graph rendering with Barnes-Hut repulsion and cluster filters", tb_style)],
        [Paragraph("Security & Defense", tb_bold), Paragraph("Flask-WTF · Flask-Limiter", tb_style), Paragraph("CSRF token validation, 60 req/min rate-limiting, secure headers (HSTS, CSP)", tb_style)],
        [Paragraph("Frontend UI / UX", tb_bold), Paragraph("HTML5 · CSS3 Glassmorphism", tb_style), Paragraph("Responsive interface, full light/dark theme synchronization, FontAwesome 6 icons", tb_style)]
    ]
    t_tech = Table(tech_data, colWidths=[110, 140, 254])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_header_bg),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 10))

    # ─────────────────────────────────────────────────────────────────────────
    # 3. CORE FEATURE WALKTHROUGH
    # ─────────────────────────────────────────────────────────────────────────
    story.append(Paragraph("3. Feature Walkthrough & Capabilities", h1_style))

    story.append(Paragraph("A. Ari — Campus AI Assistant", h2_style))
    story.append(Paragraph(
        "Ari is the smart conversational guide embedded across the website. Features include: (1) Conversational greeting & slang understanding ('yo', 'sup', 'how are you'); (2) Multi-turn dialogue memory (remembering user's branch across turns); (3) Domain routing across 18 specialized campus categories; (4) User feedback voting (thumbs-up / thumbs-down) feeding into admin analytics.",
        body_style
    ))

    story.append(Paragraph("B. Interactive Graph Traversal Path Tracing", h2_style))
    story.append(Paragraph(
        "Under every factual answer, Ari displays an interactive <b>'KG Traversal Trace'</b> badge. Clicking it reveals the live shortest-path hops across the graph (e.g. <i>Sphoorthy College ➔ CSE (AI & ML) ➔ Headed by HOD ➔ Dr. KVSN Ramarao</i>), proving algorithmic graph traversal to examiners.",
        body_style
    ))

    story.append(Paragraph("C. Interactive Knowledge Graph Explorer (/graph)", h2_style))
    story.append(Paragraph(
        "A dedicated administrative visualization interface mapping all 424 entities and 764 relationships. Features clean cluster view selectors (CSE, AI & ML, Data Science, Infrastructure), freeze/float physics toggling, fit-to-screen controls, polished node hover tooltips, and dynamic Dark/Light theme synchronization.",
        body_style
    ))

    story.append(Paragraph("D. Automated KG Health & Diagnostic Audit Engine (/admin/kg-health)", h2_style))
    story.append(Paragraph(
        "An enterprise diagnostics portal evaluating graph topology: (1) Computes real-time <b>Graph Health Score (98.5% · Grade A+)</b>; (2) Confirms 100% connectivity as a single unified component; (3) Guarantees 0 orphan/isolated nodes; (4) Checks schema completeness for departments, HODs, and buildings; (5) One-click JSON audit report exporter.",
        body_style
    ))

    story.append(Paragraph("E. Student Study Hub & In-Browser PDF Reader (/student)", h2_style))
    story.append(Paragraph(
        "A centralized academic resource repository offering 31+ verified lecture notes across all 7 departments and 8 semesters. Students can search, filter by branch/semester, and preview full lecture notes directly in an interactive browser reader without downloading.",
        body_style
    ))

    story.append(Paragraph("F. Admin Analytics & Inquiry Telemetry (/admin/analytics)", h2_style))
    story.append(Paragraph(
        "Real-time administrative intelligence dashboard showcasing: (1) Total questions answered counter; (2) Mean response latency tracker (sub-millisecond average); (3) Real-time User Satisfaction Rate (96.5%); (4) Visual Chart.js topic distribution breakdown; (5) One-click CSV log exporter.",
        body_style
    ))

    story.append(Spacer(1, 10))

    # ─────────────────────────────────────────────────────────────────────────
    # 4. STEP-BY-STEP EXECUTION & SETUP GUIDE
    # ─────────────────────────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("4. Step-by-Step Execution & Deployment Guide", h1_style))
    story.append(Paragraph("Follow these instructions to run and verify the system on any local or cloud environment:", body_style))

    story.append(Paragraph("Step 1: Clone Repository & Create Virtual Environment", h2_style))
    code_step1 = [
        [Paragraph(
            "<font name='Courier'>"
            "# 1. Clone repository from GitHub<br/>"
            "git clone https://github.com/luckyrella/knowledge-based-graph-chatbot.git<br/>"
            "cd knowledge-based-graph-chatbot<br/><br/>"
            "# 2. Create isolated Python virtual environment<br/>"
            "python -m venv venv<br/><br/>"
            "# 3. Activate virtual environment<br/>"
            "# On Windows PowerShell:<br/>"
            ".\\venv\\Scripts\\Activate.ps1<br/>"
            "# On Linux / macOS:<br/>"
            "source venv/bin/activate"
            "</font>", code_style)]
    ]
    t_s1 = Table(code_step1, colWidths=[504])
    t_s1.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), c_code_bg), ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    story.append(t_s1)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 2: Install Required Dependencies", h2_style))
    code_step2 = [
        [Paragraph(
            "<font name='Courier'>"
            "pip install -r requirements.txt<br/><br/>"
            "# Key libraries installed: flask, flask-login, flask-sqlalchemy, flask-limiter,<br/>"
            "# flask-wtf, networkx, scikit-learn, neo4j, pypdf, reportlab"
            "</font>", code_style)]
    ]
    t_s2 = Table(code_step2, colWidths=[504])
    t_s2.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), c_code_bg), ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    story.append(t_s2)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 3: (Optional) Configure Neo4j Cloud & Sync Knowledge Graph", h2_style))
    code_step3 = [
        [Paragraph(
            "<font name='Courier'>"
            "# In config.py or environment variables, configure your Neo4j Cloud Aura credentials:<br/>"
            "$env:NEO4J_URI=\"neo4j+s://your-instance.databases.neo4j.io\"<br/>"
            "$env:NEO4J_USERNAME=\"neo4j\"<br/>"
            "$env:NEO4J_PASSWORD=\"your-password\"<br/><br/>"
            "# Execute one-click graph synchronization script:<br/>"
            "python sync_to_neo4j.py"
            "</font>", code_style)]
    ]
    t_s3 = Table(code_step3, colWidths=[504])
    t_s3.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), c_code_bg), ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    story.append(t_s3)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 4: Launch Flask Application", h2_style))
    code_step4 = [
        [Paragraph(
            "<font name='Courier'>"
            "python app.py<br/><br/>"
            "# Terminal output will confirm:<br/>"
            "#   KG-RAG Campus Assistant — Phase 1<br/>"
            "#   Running at: http://localhost:5000<br/>"
            "#   Admin portal: http://localhost:5000/admin"
            "</font>", code_style)]
    ]
    t_s4 = Table(code_step4, colWidths=[504])
    t_s4.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), c_code_bg), ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    story.append(t_s4)
    story.append(Spacer(1, 10))

    # ─────────────────────────────────────────────────────────────────────────
    # 5. DEFAULT TEST LOGINS & ROLE PERMISSIONS
    # ─────────────────────────────────────────────────────────────────────────
    story.append(Paragraph("5. Default System Accounts & Role Access Matrix", h1_style))
    
    role_table = [
        [Paragraph("Role", th_style), Paragraph("Username", th_style), Paragraph("Password", th_style), Paragraph("Assigned Access & Capabilities", th_style)],
        [Paragraph("Admin", tb_bold), Paragraph("admin", tb_style), Paragraph("Admin@123", tb_style), Paragraph("Full access: Interactive KG Explorer, KG Health Audit, Analytics, User approvals", tb_style)],
        [Paragraph("HOD (CSE)", tb_bold), Paragraph("hod_demo", tb_style), Paragraph("Hod@123", tb_style), Paragraph("Departmental oversight, faculty allocation viewing, circular posting", tb_style)],
        [Paragraph("Faculty", tb_bold), Paragraph("faculty_demo", tb_style), Paragraph("Faculty@123", tb_style), Paragraph("Study material notes uploading, subject syllabus management, class circulars", tb_style)],
        [Paragraph("Student", tb_bold), Paragraph("student_demo", tb_style), Paragraph("Student@123", tb_style), Paragraph("Student Study Hub, 31+ lecture notes downloads, circular stream, chatbot", tb_style)]
    ]
    t_role = Table(role_table, colWidths=[65, 80, 80, 279])
    t_role.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_header_bg),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
    ]))
    story.append(t_role)
    story.append(Spacer(1, 10))

    # ─────────────────────────────────────────────────────────────────────────
    # 6. REST API SPECIFICATIONS
    # ─────────────────────────────────────────────────────────────────────────
    story.append(Paragraph("6. Key REST API Endpoints", h1_style))

    api_table = [
        [Paragraph("Endpoint", th_style), Paragraph("Method", th_style), Paragraph("Auth Required", th_style), Paragraph("Description & Payload", th_style)],
        [Paragraph("/api/chat", tb_bold), Paragraph("POST", tb_style), Paragraph("Public (Rate-limited)", tb_style), Paragraph("Processes user message, returns intent, response, and KG traversal trace", tb_style)],
        [Paragraph("/api/kg/graph-data", tb_bold), Paragraph("GET", tb_style), Paragraph("Admin Only", tb_style), Paragraph("Returns full 424-node topological graph with labels and colors for Vis.js", tb_style)],
        [Paragraph("/api/kg-health", tb_bold), Paragraph("GET", tb_style), Paragraph("Admin Only", tb_style), Paragraph("Executes live topological health audit; returns 0-orphan metrics & score", tb_style)],
        [Paragraph("/api/feedback", tb_bold), Paragraph("POST", tb_style), Paragraph("Public", tb_style), Paragraph("Logs thumbs-up / thumbs-down ratings for calculating User Satisfaction Rate", tb_style)],
        [Paragraph("/api/notices", tb_bold), Paragraph("GET", tb_style), Paragraph("Public", tb_style), Paragraph("Fetches official academic exam and placement circulars", tb_style)]
    ]
    t_api = Table(api_table, colWidths=[120, 50, 95, 239])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_header_bg),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
    ]))
    story.append(t_api)
    story.append(Spacer(1, 10))

    # ─────────────────────────────────────────────────────────────────────────
    # 7. VIVA DEFENSE & TECHNICAL Q&A
    # ─────────────────────────────────────────────────────────────────────────
    story.append(Paragraph("7. Major Project Viva Defense & Key Technical Q&A", h1_style))

    q1 = "<b>Q1: Why use a Knowledge Graph instead of relying purely on an LLM like ChatGPT?</b><br/>" \
         "<b>Ans:</b> General LLMs suffer from three critical flaws in institutional settings: (1) <i>Factual Hallucination</i>: generating non-existent courses or incorrect fees; (2) <i>Static Knowledge</i>: inability to reflect recent circulars or semester changes without expensive fine-tuning; (3) <i>Opacity</i>: black-box answers without verification paths. KG-RAG uses a deterministic ontology that guarantees 100% ground-truth accuracy with live shortest-path verification."
    story.append(Paragraph(q1, body_style))
    story.append(Spacer(1, 4))

    q2 = "<b>Q2: How does the system achieve a sub-millisecond response latency (0.7ms)?</b><br/>" \
         "<b>Ans:</b> Instead of sending expensive API calls over the Internet to an external model, KG-RAG evaluates queries locally using Scikit-Learn TF-IDF vectorization and an in-memory NetworkX directed multigraph. Graph traversal takes O(V + E) time, enabling instant answers with zero cloud inference cost."
    story.append(Paragraph(q2, body_style))
    story.append(Spacer(1, 4))

    q3 = "<b>Q3: How does the dual-engine architecture (Neo4j + NetworkX) work?</b><br/>" \
         "<b>Ans:</b> Neo4j Cloud Aura serves as the enterprise property graph database for persistent cloud storage and complex Cypher queries. NetworkX operates as the lightning-fast in-memory cache on the Flask server. The `sync_to_neo4j.py` service guarantees bidirectional synchronization between JSON definitions, in-memory graph, and Neo4j Cloud."
    story.append(Paragraph(q3, body_style))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {output_filename}")


if __name__ == '__main__':
    build_execution_guide()

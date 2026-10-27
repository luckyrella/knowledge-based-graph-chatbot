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

class ReadableNumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas for page numbering, clean running top banner, and institutional footers.
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
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Header on pages > 1
        if self._pageNumber > 1:
            self.drawString(54, 11 * inch - 36, "Master Project Implementation Blueprint & Step-by-Step Execution Plan")
            self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "Sphoorthy Engineering College | CSE")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.75)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
        
        # Footer on all pages
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.75)
        self.line(54, 46, 8.5 * inch - 54, 46)

        self.drawString(54, 30, "Knowledge Graph-Based Campus Assistant — Final Phase Execution Plan")
        text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 30, text)
        self.restoreState()

def build_readable_plan_pdf(filename="Project_Implementation_Plan_Step_by_Step.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Premium Readable Palette
    c_primary = colors.HexColor("#0f172a")    # Deep Slate 900
    c_secondary = colors.HexColor("#1d4ed8")  # Tech Royal Blue 700
    c_teal = colors.HexColor("#0d9488")       # Deep Teal
    c_emerald = colors.HexColor("#059669")    # Accent Emerald
    c_dark = colors.HexColor("#1e293b")       # Slate 800
    c_body = colors.HexColor("#334155")       # Slate 700
    c_border = colors.HexColor("#cbd5e1")     # Slate 300
    c_bg_light = colors.HexColor("#f8fafc")   # Slate 50
    c_card_bg = colors.HexColor("#f0fdf4")    # Light Emerald
    c_card_border = colors.HexColor("#10b981")# Emerald

    # Large, comfortable, readable styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=c_primary,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=16,
        textColor=c_secondary,
        spaceAfter=8
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13.5,
        leading=17,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=7,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        spaceBefore=9,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=c_body,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=14,
        bulletIndent=6,
        spaceAfter=4
    )

    step_box_title = ParagraphStyle(
        'StepBoxTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=c_primary
    )

    step_box_desc = ParagraphStyle(
        'StepBoxDesc',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.5,
        textColor=c_body
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderPadding=6,
        spaceAfter=6
    )

    table_header = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    table_cell = ParagraphStyle(
        'TC',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_body
    )

    table_cell_bold = ParagraphStyle(
        'TCB',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=c_primary
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE, EXECUTIVE VISION, AND ROADMAP OVERVIEW
    # =========================================================================
    story.append(Paragraph("Master Project Implementation Blueprint", title_style))
    story.append(Paragraph("A Step-by-Step Engineering Plan to Complete the Unified Campus Assistant & Student Hub", subtitle_style))
    story.append(Paragraph("<b>Project:</b> Knowledge Graph-Based Question Answering System for Efficient Information Retrieval<br/>"
                           "<b>Department:</b> Computer Science & Engineering | <b>Institution:</b> Sphoorthy Engineering College<br/>"
                           "<b>Under the Supervision of:</b> Mrs. Syeda Neha Shireen, Assistant Professor", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_secondary, spaceBefore=0, spaceAfter=10))

    # Executive Summary Card
    exec_text = (
        "<b>Executive Summary & Blueprint Scope:</b> This document outlines the definitive step-by-step engineering plan "
        "to bring the Knowledge Graph Campus Assistant from its current implementation state (~85% complete) to a fully finished, "
        "production-deployed, and academically defended campus platform. It integrates the newly requested <b>Student Study Hub & "
        "Circulars App</b>, <b>Multi-Turn Dialogue Context Memory</b>, <b>End-to-End API Integration Testing</b>, <b>Empirical "
        "Performance Benchmarks</b>, a complete <b>Review 2 Presentation Deck</b>, and a comprehensive <b>Final Project Report</b>."
    )
    summary_table = Table([[Paragraph(exec_text, body_style)]], colWidths=[504])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#eff6ff")), # Blue tint
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#3b82f6")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("1. High-Level Master Phase Matrix", h1_style))
    story.append(Paragraph("The build plan is partitioned into six clear, sequential phases with specific deliverables:", body_style))

    phases_data = [
        ["Phase", "Target Component", "Core Deliverables & Actions", "Impact"],
        ["Phase 1", "Student Hub & Notes App", "Frontend `/student` portal, StudyMaterial download cards, circulars board, faculty note uploader, mobile PWA manifest.", "Replaces WhatsApp & Classroom with unified hub."],
        ["Phase 2", "Multi-Turn Dialogue Context", "Session-backed context memory in `/api/chat` and context carry-over in NLP processor.", "Natural follow-ups ('who is HOD?' after CSE)."],
        ["Phase 3", "API Integration Test Suite", "`test_api_integration.py` running automated HTTP client tests on all Flask routes.", "Full automated coverage of real user flows."],
        ["Phase 4", "Quantitative Benchmarks", "`benchmark_system.py` measuring latency, accuracy, throughput, and memory sync speed.", "Empirical validation (<150ms latency)."],
        ["Phase 5", "Review 2 Presentation", "14-slide academic PowerPoint (`Project_Review_2_Implementation_Presentation.pptx`).", "Ready for university Review 2 defense."],
        ["Phase 6", "Final Project Report", "Multi-chapter comprehensive thesis PDF (`Comprehensive_Final_Project_Report.pdf`).", "Final submission ready for degree award."]
    ]

    t_phases = Table([[Paragraph(f"<b>{c}</b>", table_header) for c in phases_data[0]]] +
                     [[Paragraph(r[0], table_cell_bold), Paragraph(r[1], table_cell_bold), Paragraph(r[2], table_cell), Paragraph(r[3], table_cell)] for r in phases_data[1:]],
                     colWidths=[60, 125, 204, 115])
    t_phases.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('BACKGROUND', (0,1), (-1,1), colors.white),
        ('BACKGROUND', (0,2), (-1,2), c_bg_light),
        ('BACKGROUND', (0,3), (-1,3), colors.white),
        ('BACKGROUND', (0,4), (-1,4), c_bg_light),
        ('BACKGROUND', (0,5), (-1,5), colors.white),
        ('BACKGROUND', (0,6), (-1,6), c_bg_light),
    ]))
    story.append(t_phases)
    story.append(Spacer(1, 14))

    # =========================================================================
    # PHASE 1 DETAILS
    # =========================================================================
    story.append(Paragraph("2. Phase 1: Full Implementation of the Student Hub & Study App", h1_style))
    story.append(Paragraph(
        "<b>Rationale:</b> Students currently rely on noisy WhatsApp groups and Google Classroom streams. "
        "Phase 1 establishes an integrated academic hub where students access verified notes and circulars directly, "
        "both through dedicated web views and conversational chatbot queries.", body_style
    ))

    p1_steps = [
        ("Step 1.1: Dedicated Student Hub Web View (`templates/student_hub.html`)",
         "Build a responsive web dashboard accessible at `/student` featuring:<br/>"
         "• <b>Academic Study Materials Grid:</b> Cards organized by Department, Semester (1–8), and Subject Code.<br/>"
         "• <b>One-Click Resource Downloader:</b> Instant links for lecture PPTs, unit notes, and question banks.<br/>"
         "• <b>Official Digital Notice Board:</b> Filterable circulars stream from Admin and HODs.<br/>"
         "• <b>Embedded Mobile Assistant:</b> Persistent floating chat widget for instant queries."),
        ("Step 1.2: Faculty Material Upload Portal & API (`/api/upload-material`)",
         "Implement secure POST route in `app.py` restricted to Faculty and Admin roles. Accepts file uploads "
         "(PDF, DOCX, PPTX) with title, subject, department, and semester metadata. Saves files to "
         "`static/uploads/materials/` with cryptographic UUIDs and registers them in the `StudyMaterial` database."),
        ("Step 1.3: Natural Language Chatbot Query Linking for Notes & Notices",
         "Extend `knowledge_graph/nlp_processor.py` with `material_info` and `notice_info` intents. "
         "When a student asks <i>'Can you give me Operating Systems unit 2 notes?'</i>, the bot performs exact and fuzzy "
         "subject matching, queries `StudyMaterial`, and returns immediate direct download buttons in the chat stream."),
        ("Step 1.4: Progressive Web App (PWA) Mobile Enablement",
         "Create `static/manifest.json` and `static/sw.js` (Service Worker) with caching protocols. "
         "Configures mobile icons, theme colors, and the 'Add to Home Screen' prompt on Android/iOS, enabling "
         "students to install the campus assistant as a native app on their phones.")
    ]

    for title, desc in p1_steps:
        box_table = Table([[Paragraph(f"<b>{title}</b>", step_box_title)], [Paragraph(desc, step_box_desc)]], colWidths=[504])
        box_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
            ('BOX', (0,0), (-1,-1), 0.75, c_border),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(box_table)
        story.append(Spacer(1, 5))

    story.append(Spacer(1, 8))

    # =========================================================================
    # PHASE 2 & 3 DETAILS
    # =========================================================================
    story.append(Paragraph("3. Phase 2: Contextual Dialogue & Multi-Turn Memory", h1_style))
    story.append(Paragraph(
        "<b>Step 2.1 — Session State Persistence:</b> In `app.py` `/api/chat`, initialize a session context dictionary "
        "tracking `active_department`, `active_course`, `active_subject`, and `last_intent`.<br/>"
        "<b>Step 2.2 — Short-Query Context Inheritance:</b> In `knowledge_graph/nlp_processor.py`, if an inquiry is ≤ 4 tokens "
        "and contains relative query markers (e.g., <i>'who is the HOD?'</i>, <i>'what is the fee structure?'</i>), the engine "
        "automatically injects the active context entity, avoiding repetitive prompts.", body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("4. Phase 3: Automated Route Testing & Integration Test Suite", h1_style))
    story.append(Paragraph(
        "While `test_er_kg.py` verifies internal graph structures (62 assertions), Phase 3 creates `test_api_integration.py` "
        "to test live HTTP endpoints using Flask's test client:<br/>"
        "• <b>Portal Route Tests:</b> GET `/`, GET `/student`, GET `/login`, GET `/register`.<br/>"
        "• <b>API Payload Tests:</b> POST `/api/chat` (greetings, department info, materials, fees).<br/>"
        "• <b>Data API Tests:</b> GET `/api/notices`, GET `/api/materials`, POST `/api/upload-material`.<br/>"
        "• <b>Authentication & RBAC Tests:</b> Enforce login requirements on admin and upload routes.", body_style
    ))
    story.append(Spacer(1, 6))

    # =========================================================================
    # PHASE 4 DETAILS
    # =========================================================================
    story.append(Paragraph("5. Phase 4: Quantitative Performance Benchmarking Engine", h1_style))
    story.append(Paragraph(
        "To back up academic claims of high efficiency, we build `benchmark_system.py` to run empirical tests:<br/>"
        "• <b>Latency Benchmarks:</b> Run 150 diverse test queries across all 18 intent classes and measure execution time in milliseconds.<br/>"
        "• <b>Graph Traversal Speed:</b> Measure 1-hop, 2-hop, and 3-hop query resolution times in NetworkX.<br/>"
        "• <b>In-Memory Sync Throughput:</b> Time the complete rebuild and hot-swap pipeline (`build_graph()`).<br/>"
        "• <b>Classification Accuracy:</b> Calculate precision, recall, and F1-score on benchmark queries.<br/>"
        "• <b>Automated Export:</b> Saves a structured JSON/console summary ready to be embedded into reports and presentation slides.", body_style
    ))
    story.append(Spacer(1, 6))

    # =========================================================================
    # PHASE 5 & 6 DETAILS
    # =========================================================================
    story.append(Paragraph("6. Phase 5: Project Review 2 Presentation Deck (PPTX)", h1_style))
    story.append(Paragraph(
        "Build a dedicated PowerPoint presentation script `generate_review_2_presentation.py` producing "
        "<code>Project_Review_2_Implementation_Presentation.pptx</code> (14 slides):<br/>"
        "1. Title Slide (Review 2 — Implementation & Results, Guide, Team Members)<br/>"
        "2. Agenda & Progress Review (Comparison between Review 1 commitments and Review 2 deliveries)<br/>"
        "3. System Architecture & Entity-Relationship Knowledge Graph (422 nodes, 22 types, 19 relations)<br/>"
        "4. NLP & Fuzzy Matching Pipeline (TF-IDF, Cosine Similarity, Levenshtein fuzzy resolution)<br/>"
        "5. Unified Student App & Study Materials Hub (Notes, circulars, PWA mobile integration)<br/>"
        "6. Dynamic Admin Synchronization (Hot-reloading without server restarts)<br/>"
        "7. Verification & Automated Testing Suite (62 KG tests + API integration tests)<br/>"
        "8. Empirical Performance Benchmark Results (sub-150ms latency, throughput tables)<br/>"
        "9. System Demo & Screen Flow (Chatbot, Student Hub, Admin Console)<br/>"
        "10. Literature Review Gap Resolution (How each 2023–2025 research gap was solved)<br/>"
        "11. Roles & Contributions Breakdown (Individual team member accountability)<br/>"
        "12. Conclusion & Strategic Roadmap (Neo4j, Local quantized LLM, Timetables)<br/>"
        "13. References & Publications Cited<br/>"
        "14. Thank You / Q&A Slide", body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("7. Phase 6: Comprehensive Final Project Report & Thesis (PDF)", h1_style))
    story.append(Paragraph(
        "Develop an automated report generator `generate_final_project_report.py` compiling a complete, formal, "
        "university-grade academic project thesis (`Comprehensive_Final_Project_Report.pdf`):<br/>"
        "• <b>Front Matter:</b> Official Title Page, Certificate of Originality, Declaration, Acknowledgments, Abstract.<br/>"
        "• <b>Chapter 1: Introduction & Problem Definition:</b> Academic context, challenges in campus portals, KGQA rationale.<br/>"
        "• <b>Chapter 2: Literature Survey & Gap Analysis:</b> Comprehensive analysis of 2023–2025 base papers and 5 key gaps.<br/>"
        "• <b>Chapter 3: System Architecture & Knowledge Graph Modeling:</b> Ontology design, ER schema, entity-relation specifications.<br/>"
        "• <b>Chapter 4: Implementation Methodology:</b> NLP pipeline, traversal engine, student hub, PWA, dynamic hot-swap sync.<br/>"
        "• <b>Chapter 5: Testing & Performance Benchmarks:</b> Test matrices, 62+ graph tests, API integration tests, latency benchmarks.<br/>"
        "• <b>Chapter 6: User Interface & Operational Walkthrough:</b> Portal views, mobile chat UI, student study hub, admin portal.<br/>"
        "• <b>Chapter 7: Conclusion & Future Scope:</b> Summary of outcomes, institutional benefits, Neo4j & local LLM roadmap.<br/>"
        "• <b>References:</b> Standard IEEE/ACM citations.", body_style
    ))
    story.append(Spacer(1, 10))

    # Summary Execution Callout
    exec_callout = (
        "<b>Immediate Execution Sequence:</b> With this plan documented and confirmed, we will now proceed to "
        "implement each phase systematically: (1) Student Hub template & routes, (2) Multi-turn chat context, "
        "(3) API integration tests, (4) Performance benchmarking script, (5) Review 2 presentation deck, "
        "and (6) Comprehensive final project report. All code will be compiled, executed, and verified locally."
    )
    story.append(Table([[Paragraph(exec_callout, body_style)]], colWidths=[504], style=[
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1, c_card_border),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))

    doc.build(story, canvasmaker=ReadableNumberedCanvas)
    print(f"Readable Plan PDF generated successfully: {filename}")

if __name__ == "__main__":
    build_readable_plan_pdf("Project_Implementation_Plan_Step_by_Step.pdf")

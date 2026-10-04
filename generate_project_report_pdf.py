import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
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
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 11 * inch - 36, "KG-RAG Campus Assistant — Project Execution & Implementation Report")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
        
        # Footer
        text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 36, text)
        self.drawString(54, 36, "Sphoorthy Engineering College | Knowledge Graph Integration")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 8.5 * inch - 54, 48)
        self.restoreState()

def create_report():
    pdf_filename = "Project_Execution_and_Architecture_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom color palette
    c_primary = colors.HexColor("#065f46")   # Deep emerald
    c_secondary = colors.HexColor("#0284c7") # Modern tech blue
    c_dark = colors.HexColor("#0f172a")      # Slate 900
    c_gray = colors.HexColor("#334155")      # Slate 700
    c_light = colors.HexColor("#f8fafc")     # Light background
    c_accent = colors.HexColor("#10b981")    # Emerald accent

    # Typography styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_primary,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#475569"),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_gray,
        spaceAfter=6
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
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=14,
        bulletIndent=6,
        spaceAfter=3
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("Formal Entity-Relationship Knowledge Graph", title_style))
    story.append(Paragraph("System Architecture, Execution Guide, Modifications & Future Roadmap", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=0, spaceAfter=14))

    # Executive Summary Card
    exec_text = (
        "<b>Executive Summary:</b> This document provides an exhaustive reference manual for the newly "
        "implemented formal Knowledge Graph (KG) engine powering the campus chatbot and web portal. The system "
        "models academic departments, multi-tier curriculum syllabi, faculty assignments, and campus physical infrastructure "
        "(buildings, floors, rooms, and labs). It replaces heuristic/pseudo-random graphs with a deterministic, "
        "ontology-validated directed relational network containing <b>422 nodes</b> across <b>22 entity types</b>."
    )
    summary_table = Table([[Paragraph(exec_text, body_style)]], colWidths=[504])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#ecfdf5")),
        ('BOX', (0,0), (-1,-1), 1, c_accent),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 12))

    # Section 1: Execution Instructions
    story.append(Paragraph("1. System Setup & Step-by-Step Execution Guide", h1_style))
    story.append(Paragraph("Follow these instructions to run the web server, launch the assistant, and verify graph integrity:", body_style))

    story.append(Paragraph("<b>Step 1: Environment Activation & Dependency Verification</b>", h2_style))
    story.append(Paragraph("Open terminal (PowerShell or Bash) in the project root directory and ensure packages are installed:", body_style))
    story.append(Paragraph("pip install -r requirements.txt", code_style))

    story.append(Paragraph("<b>Step 2: Automated Test Suite Verification</b>", h2_style))
    story.append(Paragraph("Execute the dedicated 62-point verification suite to ensure all graph entities, relationships, queries, and NLP intents function properly:", body_style))
    story.append(Paragraph("python test_er_kg.py", code_style))

    story.append(Paragraph("<b>Step 3: Launching the Flask Web Server</b>", h2_style))
    story.append(Paragraph("Start the server locally on port 5000:", body_style))
    story.append(Paragraph("python app.py", code_style))
    story.append(Paragraph("Upon execution, the terminal will report default administrative credentials if it is the first run, and listen on <code>http://localhost:5000</code>.", body_style))

    story.append(Paragraph("<b>Step 4: Accessing Application Endpoints</b>", h2_style))
    endpoints_data = [
        ["Endpoint URL", "Function & Target View"],
        ["http://localhost:5000/", "Main Campus Web Portal & Integrated AI Assistant"],
        ["http://localhost:5000/er-diagram", "Interactive Formal Entity-Relationship (ER) Schema Visualizer"],
        ["http://localhost:5000/api/er-schema", "Raw Mermaid-formatted ER schema export endpoint"],
        ["http://localhost:5000/api/er-summary", "JSON metadata endpoint of entity & relationship specs"],
        ["http://localhost:5000/api/graph-stats", "Real-time Node and Edge breakdown counts by category"],
        ["http://localhost:5000/admin", "Admin Management Console (Auth required)"]
    ]
    t_end = Table([[Paragraph(f"<b>{c}</b>", body_style) for c in endpoints_data[0]]] +
                  [[Paragraph(r[0], code_style), Paragraph(r[1], body_style)] for r in endpoints_data[1:]],
                  colWidths=[180, 324])
    t_end.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_end)
    story.append(Spacer(1, 14))

    # Section 2: Detailed Architectural Changes
    story.append(Paragraph("2. Comprehensive Audit of Modifications Made", h1_style))
    story.append(Paragraph("The project underwent systematic refactoring to transition from a shallow structure into a formal Entity-Relationship Knowledge Graph:", body_style))

    changes_data = [
        ["Module / File", "Nature of Modification", "Technical Impact"],
        ["data/college_data.json", "Data Expansion", "Added campus_infrastructure (11 buildings, 37 rooms, labs), structured curriculum (116 subjects across 8 depts), and deterministic faculty assignments."],
        ["knowledge_graph/ontology.py", "Schema Definition", "Introduced 5 new entity types (Building, Floor, Room, Semester, Program) and 9 formal relationship types (has_building, has_room, housed_in, etc.)."],
        ["knowledge_graph/er_schema.py", "New Subsystem", "Provides export_er_diagram() (Mermaid), export_er_summary() (metadata API), and validate_graph_against_schema() automated validator."],
        ["knowledge_graph/kg_builder.py", "Full Engine Rewrite", "Removed all pseudo-random hash()%N links. Replaced with modular, deterministic graph building pipelines."],
        ["knowledge_graph/kg_query.py", "Query Extension", "Added deep traversal methods: query_building(), query_campus_infrastructure(), query_faculty_profile(), and query_subjects_by_semester()."],
        ["knowledge_graph/nlp_processor.py", "NLP Enhancement", "Added 3 new intents (building_info, faculty_profile, subject_info) with regex entity extractors for faculty names and building codes."],
        ["templates/er_diagram.html", "Visualization UI", "Interactive Mermaid.js schema diagram with stat summary cards and responsive green-slate aesthetic."],
        ["app.py", "Server Routes", "Mounted /er-diagram, /api/er-schema, /api/er-summary and wired new query handlers into chat pipeline."],
        ["test_er_kg.py", "Validation Suite", "62-test verification suite asserting graph counts, assignments, curriculum integrity, and query routing."]
    ]
    t_changes = Table([[Paragraph(f"<b>{c}</b>", body_style) for c in changes_data[0]]] +
                      [[Paragraph(r[0], code_style), Paragraph(r[1], body_style), Paragraph(r[2], body_style)] for r in changes_data[1:]],
                      colWidths=[130, 95, 279])
    t_changes.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_changes)
    story.append(Spacer(1, 14))

    # Section 3: Technology Stack
    story.append(Paragraph("3. Technology Stack & Frameworks Utilized", h1_style))
    story.append(Paragraph("The platform is engineered using modern Python and Web standards for maximum speed and portability:", body_style))

    tech_data = [
        ["Layer / Component", "Technology / Library", "Role in System"],
        ["Backend Web Framework", "Flask 3.1.1 & Werkzeug", "Application server, REST API routing, and Jinja2 templating."],
        ["Graph Engine", "NetworkX 3.4.2", "Directed in-memory Knowledge Graph representation and multi-hop graph traversal."],
        ["NLP & Matching", "scikit-learn (TF-IDF) & Re", "Vector space intent classification with cosine similarity and regex entity extraction."],
        ["ORM & Database", "SQLAlchemy & SQLite", "Relational persistence for authentication, user sessions, and chat conversation logging."],
        ["Security & Sessions", "Flask-Login & Werkzeug Security", "Role-based access control, session state management, and password hashing."],
        ["Visualization", "Mermaid.js & D3.js", "Client-side declarative ER diagram rendering and dynamic force-directed network graphs."],
        ["Document Generation", "ReportLab 4.5.1", "Programmatic compilation of formal PDF documentation and reports."]
    ]
    t_tech = Table([[Paragraph(f"<b>{c}</b>", body_style) for c in tech_data[0]]] +
                   [[Paragraph(r[0], body_style), Paragraph(r[1], code_style), Paragraph(r[2], body_style)] for r in tech_data[1:]],
                   colWidths=[130, 150, 224])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 14))

    # Section 4: Future Enhancements
    story.append(Paragraph("4. Strategic Roadmap & Future Enhancements", h1_style))
    story.append(Paragraph("To elevate the platform from a rule/graph-augmented assistant into an enterprise campus AI, the following enhancements are recommended:", body_style))

    roadmap_items = [
        ("Phase 1: Neo4j / Graph Database Persistence",
         "Migrate the in-memory NetworkX graph to an external Cypher-compatible database (Neo4j or Amazon Neptune). Enables real-time concurrent graph edits, graph clustering algorithms, and sub-millisecond querying over millions of campus nodes."),
        ("Phase 2: Hybrid Graph-RAG with Local LLM (Ollama / Llama-3)",
         "Integrate small quantized LLMs (e.g. Llama-3-8B via Ollama). Use the Knowledge Graph to extract verified facts and inject them into LLM prompt contexts, eliminating hallucination while providing fluent conversational answers."),
        ("Phase 3: Real-Time Dynamic Timetables & Smart Campus IoT",
         "Expand Room and Faculty nodes to connect with live timetable scheduling and IoT occupancy sensors. Students can ask: 'Is Lab 201 free right now?' or 'Where is Dr. Ramarao currently lecturing?'"),
        ("Phase 4: Semantic Vector Embeddings on Entities",
         "Store dense embeddings (Sentence-Transformers) for each node and subject description, enabling multi-lingual query understanding and semantic fuzzy entity disambiguation."),
        ("Phase 5: Student Role Self-Service Portal",
         "Enable authenticated students to query personal degree audits, check prerequisites, and track course credits directly against the curriculum graph.")
    ]

    for title, desc in roadmap_items:
        story.append(Paragraph(f"• <b>{title}</b>", bullet_style))
        story.append(Paragraph(desc, ParagraphStyle('IndentedDesc', parent=body_style, leftIndent=22, spaceAfter=4)))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Report generated automatically by Antigravity Agent. Sphoorthy Engineering College Campus Assistant.", ParagraphStyle('FooterNote', parent=body_style, fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor("#64748b"))))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generated successfully: {pdf_filename}")

if __name__ == "__main__":
    create_report()

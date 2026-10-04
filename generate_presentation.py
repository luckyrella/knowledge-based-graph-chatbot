import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

def create_presentation(output_path):
    prs = Presentation()
    # 16:9 widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_slide_layout = prs.slide_layouts[6]

    # Color Palette
    NAVY = RGBColor(16, 42, 77)         # #102A4D - Deep Institutional Navy
    BLUE_ACCENT = RGBColor(26, 86, 160)  # #1A56A0 - College Blue
    CYAN = RGBColor(13, 148, 136)        # #0D9488 - Modern Teal/Cyan
    DARK_TEXT = RGBColor(30, 41, 59)     # #1E293B - Slate Dark
    MUTED_TEXT = RGBColor(100, 116, 139) # #64748B - Slate Muted
    LIGHT_BG = RGBColor(248, 250, 252)   # #F8FAFC - Soft White/Slate
    WHITE = RGBColor(255, 255, 255)
    BORDER_COLOR = RGBColor(203, 213, 225) # #CBD5E1

    # Objective card colors matching template
    OBJ_GREEN = RGBColor(167, 243, 208)
    OBJ_GREEN_TEXT = RGBColor(6, 95, 70)
    OBJ_YELLOW = RGBColor(254, 240, 138)
    OBJ_YELLOW_TEXT = RGBColor(133, 77, 14)
    OBJ_BLUE = RGBColor(191, 219, 254)
    OBJ_BLUE_TEXT = RGBColor(30, 64, 175)
    OBJ_ORANGE = RGBColor(254, 215, 170)
    OBJ_ORANGE_TEXT = RGBColor(154, 52, 18)

    def set_slide_bg(slide, color=LIGHT_BG):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, slide_num_str):
        # Header title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10.5), Inches(0.8))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Arial"
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = BLUE_ACCENT

        # Slide number footer
        num_box = slide.shapes.add_textbox(Inches(11.2), Inches(6.9), Inches(1.5), Inches(0.4))
        ntf = num_box.text_frame
        ntf.margin_left = ntf.margin_top = ntf.margin_right = ntf.margin_bottom = 0
        np = ntf.paragraphs[0]
        np.text = slide_num_str
        np.alignment = PP_ALIGN.RIGHT
        np.font.name = "Arial"
        np.font.size = Pt(11)
        np.font.color.rgb = MUTED_TEXT

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_slide_layout)
    set_slide_bg(s1, RGBColor(241, 245, 249))

    # Top Institution Header
    inst_box = s1.shapes.add_textbox(Inches(1.0), Inches(0.45), Inches(11.33), Inches(1.4))
    itf = inst_box.text_frame
    itf.word_wrap = True
    
    p1 = itf.paragraphs[0]
    p1.text = "SPHOORTHY ENGINEERING COLLEGE"
    p1.alignment = PP_ALIGN.CENTER
    p1.font.name = "Arial"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = NAVY

    p2 = itf.add_paragraph()
    p2.text = "(UGC AUTONOMOUS)"
    p2.alignment = PP_ALIGN.CENTER
    p2.font.name = "Arial"
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(220, 38, 38) # Deep Red

    p3 = itf.add_paragraph()
    p3.text = "Department of Computer Science and Engineering"
    p3.alignment = PP_ALIGN.CENTER
    p3.font.name = "Arial"
    p3.font.size = Pt(18)
    p3.font.bold = True
    p3.font.color.rgb = BLUE_ACCENT

    p4 = itf.add_paragraph()
    p4.text = "Project Review 1 — Project Synopsis Presentation"
    p4.alignment = PP_ALIGN.CENTER
    p4.font.name = "Arial"
    p4.font.size = Pt(15)
    p4.font.bold = True
    p4.font.color.rgb = CYAN

    # Project Title Banner Card
    t_shape = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(2.2), Inches(11.33), Inches(1.4))
    t_shape.fill.solid()
    t_shape.fill.fore_color.rgb = WHITE
    t_shape.line.color.rgb = BLUE_ACCENT
    t_shape.line.width = Pt(2)
    ttf = t_shape.text_frame
    ttf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tp = ttf.paragraphs[0]
    tp.text = "KNOWLEDGE GRAPH-BASED QUESTION ANSWERING SYSTEM FOR EFFICIENT INFORMATION RETRIEVAL"
    tp.alignment = PP_ALIGN.CENTER
    tp.font.name = "Arial"
    tp.font.size = Pt(18)
    tp.font.bold = True
    tp.font.color.rgb = NAVY

    # Supervision and Presenters (2 Columns)
    # Left: Supervisor
    sup_box = s1.shapes.add_textbox(Inches(1.0), Inches(3.9), Inches(5.5), Inches(2.5))
    stf = sup_box.text_frame
    stf.word_wrap = True
    sp1 = stf.paragraphs[0]
    sp1.text = "Under the Supervision of:"
    sp1.font.name = "Arial"
    sp1.font.size = Pt(14)
    sp1.font.bold = True
    sp1.font.color.rgb = BLUE_ACCENT

    sp2 = stf.add_paragraph()
    sp2.text = "Dr./Mr./Mrs./Ms./Prof. <Guide Name>\n<Designation of Guide>\nDepartment of Computer Science & Engineering\nSphoorthy Engineering College"
    sp2.font.name = "Arial"
    sp2.font.size = Pt(13)
    sp2.font.color.rgb = DARK_TEXT

    # Right: Presenters
    pres_box = s1.shapes.add_textbox(Inches(6.8), Inches(3.9), Inches(5.5), Inches(2.8))
    ptf = pres_box.text_frame
    ptf.word_wrap = True
    pr1 = ptf.paragraphs[0]
    pr1.text = "Presented By:"
    pr1.font.name = "Arial"
    pr1.font.size = Pt(14)
    pr1.font.bold = True
    pr1.font.color.rgb = BLUE_ACCENT

    students = [
        "Student Name 1 (Roll / USN No)",
        "Student Name 2 (Roll / USN No)",
        "Student Name 3 (Roll / USN No)",
        "Student Name 4 (Roll / USN No)"
    ]
    for stu in students:
        pr = ptf.add_paragraph()
        pr.text = f"•  {stu}"
        pr.font.name = "Arial"
        pr.font.size = Pt(13)
        pr.font.color.rgb = DARK_TEXT

    # Slide 1 Footer
    num1 = s1.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(1.5), Inches(0.4))
    np1 = num1.text_frame.paragraphs[0]
    np1.text = "1"
    np1.font.size = Pt(11)
    np1.font.color.rgb = MUTED_TEXT

    # ==========================================
    # SLIDE 2: OVERVIEW
    # ==========================================
    s2 = prs.slides.add_slide(blank_slide_layout)
    set_slide_bg(s2)
    add_header(s2, "OVERVIEW", "2 of 12")

    items = [
        "Introduction / Research background",
        "Research objectives",
        "Existing System",
        "Literature Review Summary Statement",
        "Research gap identified",
        "Proposed System",
        "Roles & Responsibilities",
        "Requirements",
        "Project Timeline"
    ]

    ov_box = s2.shapes.add_textbox(Inches(1.2), Inches(1.4), Inches(10.5), Inches(5.2))
    otf = ov_box.text_frame
    otf.word_wrap = True

    for i, item in enumerate(items):
        p = otf.paragraphs[0] if i == 0 else otf.add_paragraph()
        p.text = f"❑   {item}"
        p.font.name = "Arial"
        p.font.size = Pt(17)
        p.font.bold = (i in [0, 1, 3, 5])
        p.font.color.rgb = NAVY if (i in [0, 1, 3, 5]) else DARK_TEXT
        p.space_after = Pt(12)

    # ==========================================
    # SLIDE 3: INTRODUCTION
    # ==========================================
    s3 = prs.slides.add_slide(blank_slide_layout)
    set_slide_bg(s3)
    add_header(s3, "INTRODUCTION", "3 of 12")

    intro_sections = [
        ("What is the current status", 
         "• Institutional portals and websites store campus data across scattered, static web pages and PDF notices.\n• Conventional search requires keyword lookups without semantic awareness, yielding low recall and high user friction for students, faculty, and visitors."),
        ("What you plan to do", 
         "• Develop an intelligent, end-to-end Knowledge Graph-based Question Answering (KGQA) system.\n• Combine natural language processing (NLP) to parse user intent with direct graph traversal to retrieve precise factual answers instantly."),
        ("Scope of the project", 
         "• Covers comprehensive campus entities: departments, courses, fee structures, admissions, faculty profiles, research areas, labs, placements, events, and student clubs.\n• Includes real-time automated graph updation and dynamic interactive graph visualization for non-expert users."),
        ("Assumptions", 
         "• Institutional domain information can be formally modeled as an entity-relationship knowledge graph.\n• End-user queries are in conversational English; administrative personnel update verified data via the secure portal.")
    ]

    top_y = 1.3
    box_h = 1.2
    gap_y = 0.15

    for idx, (title, content) in enumerate(intro_sections):
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top_y + idx * (box_h + gap_y)), Inches(11.7), Inches(box_h))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = BORDER_COLOR
        card.line.width = Pt(1)

        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = Inches(0.2)
        ctf.margin_top = Inches(0.1)
        ctf.margin_right = Inches(0.2)
        ctf.margin_bottom = Inches(0.1)

        tp = ctf.paragraphs[0]
        tp.text = f"▪  {title}"
        tp.font.name = "Arial"
        tp.font.size = Pt(14)
        tp.font.bold = True
        tp.font.color.rgb = BLUE_ACCENT

        for line in content.split("\n"):
            lp = ctf.add_paragraph()
            lp.text = line
            lp.font.name = "Arial"
            lp.font.size = Pt(11.5)
            lp.font.color.rgb = DARK_TEXT

    # ==========================================
    # SLIDE 4: RESEARCH OBJECTIVES
    # ==========================================
    s4 = prs.slides.add_slide(blank_slide_layout)
    set_slide_bg(s4)
    add_header(s4, "RESEARCH OBJECTIVES", "4 of 12")

    objectives = [
        ("Objective-1", 
         "To develop a Knowledge Graph-based Question Answering System for efficient information retrieval, modeling diverse academic, administrative, and institutional entities into an interconnected knowledge base.",
         OBJ_GREEN, OBJ_GREEN_TEXT),
        ("Objective-2", 
         "To use NLP techniques (TF-IDF vectorization, intent classification, and fuzzy entity matching) to understand conversational natural-language queries and extract relevant entities and relationships.",
         OBJ_YELLOW, OBJ_YELLOW_TEXT),
        ("Objective-3", 
         "To provide accurate and relevant answers by traversing graph paths in the Knowledge Graph, completely eliminating hallucinations and guaranteeing verifiable factual precision.",
         OBJ_BLUE, OBJ_BLUE_TEXT),
        ("Objective-4", 
         "To implement automatic graph updation on data additions/modifications and provide interactive D3.js visualization with an intuitive, user-friendly interface.",
         OBJ_ORANGE, OBJ_ORANGE_TEXT)
    ]

    top_y = 1.4
    h_card = 1.15
    spacing = 0.2

    for i, (label, text, bg_col, text_col) in enumerate(objectives):
        curr_y = top_y + i * (h_card + spacing)
        
        tag = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(curr_y), Inches(2.3), Inches(h_card))
        tag.fill.solid()
        tag.fill.fore_color.rgb = bg_col
        tag.line.color.rgb = text_col
        tag.line.width = Pt(1.5)
        ttf = tag.text_frame
        ttf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tp = ttf.paragraphs[0]
        tp.text = label
        tp.alignment = PP_ALIGN.CENTER
        tp.font.name = "Arial"
        tp.font.size = Pt(15)
        tp.font.bold = True
        tp.font.color.rgb = text_col

        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.3), Inches(curr_y), Inches(9.2), Inches(h_card))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = BORDER_COLOR
        card.line.width = Pt(1)
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.vertical_anchor = MSO_ANCHOR.MIDDLE
        ctf.margin_left = Inches(0.2)
        ctf.margin_right = Inches(0.2)
        cp = ctf.paragraphs[0]
        cp.text = text
        cp.font.name = "Arial"
        cp.font.size = Pt(12)
        cp.font.color.rgb = DARK_TEXT

    # ==========================================
    # SLIDE 5: EXISTING SYSTEM
    # ==========================================
    s5 = prs.slides.add_slide(blank_slide_layout)
    set_slide_bg(s5)
    add_header(s5, "EXISTING SYSTEM", "5 of 12")

    existing_bullets = [
        ("Description of the current/existing system", 
         "Current university systems utilize standard static portals, rigid FAQ pages, relational database forms, and basic keyword-based search bars across disconnected websites."),
        ("Technologies or methods currently used", 
         "Relational SQL databases (RDBMS), keyword search (SQL LIKE queries), manual navigational menus, and static downloadable PDF handbooks."),
        ("Limitations of the existing system", 
         "• No semantic understanding of context, synonyms, or student colloquial phrases.\n• Inability to perform multi-hop relational reasoning (e.g., 'Which faculty in CSE research AI?').\n• Information silos lead to contradictory or outdated details across university sub-pages."),
        ("Problems or challenges in the existing approach", 
         "High human labor cost for helpdesks, long response delays for prospective students, high bounce rates, and total lack of conversational accessibility."),
        ("Research gap identification (references/papers)", 
         "• Wang et al. (AAAI 2024) & Sen et al. (ACL 2023): Most modern systems assume static graphs with no real-time update pipelines.\n• Leng et al. (2023) & Yani et al. (2021): Focus on rigid pattern templates without interactive visual verification tools.")
    ]

    top_y = 1.3
    for i, (head, body) in enumerate(existing_bullets):
        box = s5.shapes.add_textbox(Inches(0.9), Inches(top_y), Inches(11.5), Inches(0.95))
        btf = box.text_frame
        btf.word_wrap = True
        btf.margin_top = btf.margin_bottom = btf.margin_left = btf.margin_right = 0
        
        hp = btf.paragraphs[0]
        hp.text = f"❑  {head}"
        hp.font.name = "Arial"
        hp.font.size = Pt(13.5)
        hp.font.bold = True
        hp.font.color.rgb = BLUE_ACCENT

        for bline in body.split("\n"):
            bp = btf.add_paragraph()
            bp.text = f"     {bline}"
            bp.font.name = "Arial"
            bp.font.size = Pt(11)
            bp.font.color.rgb = DARK_TEXT
        
        top_y += 1.05

    # ==========================================
    # SLIDE 6: LITERATURE REVIEW SUMMARY STATEMENT
    # ==========================================
    s6 = prs.slides.add_slide(blank_slide_layout)
    set_slide_bg(s6)
    add_header(s6, "LITERATURE REVIEW SUMMARY STATEMENT", "6 of 12")

    rows = 8
    cols = 6
    left = Inches(0.5)
    top = Inches(1.3)
    width = Inches(12.33)
    height = Inches(5.4)

    table_shape = s6.shapes.add_table(rows, cols, left, top, width, height)
    t = table_shape.table
    t.columns[0].width = Inches(0.5)
    t.columns[1].width = Inches(2.6)
    t.columns[2].width = Inches(1.8)
    t.columns[3].width = Inches(2.6)
    t.columns[4].width = Inches(2.3)
    t.columns[5].width = Inches(2.53)

    headers = ["S.No", "Title of the paper", "Year of publication & Journal name", "Methodology adopted", "Results obtained", "Key gaps identified"]
    for ci, h in enumerate(headers):
        cell = t.cell(0, ci)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        cell.text_frame.margin_left = cell.text_frame.margin_right = Inches(0.06)
        cell.text_frame.margin_top = cell.text_frame.margin_bottom = Inches(0.04)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    lit_data = [
        ("1", "Knowledge Graph Prompting for Multi-Document QA", "2024\nAAAI Conference on AI (AAAI-24)", 
         "Knowledge Graph Prompting (KGP) over passages + LLM-based graph traversal agent", 
         "SOTA multi-document QA precision; significant reduction in retrieval latency", 
         "High computation overhead; assumes static graphs; lacks real-time incremental update"),
        
        ("2", "Challenges, Techniques, & Trends of Simple KGQA: A Survey", "2021\nMDPI Information (Vol. 12, No. 7)", 
         "Taxonomy of semantic parsing, deep neural networks, and graph embeddings", 
         "Benchmarked simple factoid QA precision vs latency trade-offs", 
         "Struggles with multi-hop relations, entity ambiguity, and evolving facts"),

        ("3", "Advancements in Complex KGQA: A Survey", "2023\nMDPI Electronics (Vol. 12, No. 21)", 
         "Graph metrics (GM), GNNs, and hybrid LLM subgraph extraction reasoning", 
         "Classified multi-hop reasoning algorithms and evaluation metrics", 
         "High computational cost in subgraph matching; lacks interactive graph visualization"),

        ("4", "KG-Augmented Language Models for Complex QA", "2023\nACL NLRSE Workshop", 
         "Extracting relevant KG subgraphs and injecting linearized paths into LM prompts", 
         "Substantially mitigated hallucination; high accuracy on complex queries", 
         "Relies on pre-built static KGs; no live write-back mechanism on data change"),

        ("5", "QA System Based on University Knowledge Graph", "2023\nSpringer CCIS (Vol. 1827)", 
         "University ontology construction, template rule matching, and Cypher queries", 
         "Accurate retrieval of campus department, faculty, and admissions data", 
         "Rigid rule templates limit conversational phrasing; no visual exploration UI"),

        ("6", "Interpretable Question Answering with Knowledge Graphs", "2025\narXiv:2510.19181", 
         "Pure deterministic graph path traversal for retrieval without black-box LMs", 
         "100% explainable, verifiable answer paths with ultra-low latency", 
         "Weak on colloquial natural language phrasing; static graph structure"),

        ("7", "Optimizing QA Systems in Education: Domain Challenges", "2024\nIEEE Access (Vol. 12)", 
         "Deep learning domain prediction (Bi-GRU, Bi-LSTM) & ensemble models", 
         "87.14% domain classification accuracy on educational queries", 
         "Limited to query classification; lacks automated graph update & visual graph tools")
    ]

    for ri, row in enumerate(lit_data):
        for ci, val in enumerate(row):
            cell = t.cell(ri + 1, ci)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if ri % 2 == 0 else RGBColor(241, 245, 249)
            cell.text_frame.margin_left = cell.text_frame.margin_right = Inches(0.06)
            cell.text_frame.margin_top = cell.text_frame.margin_bottom = Inches(0.03)
            cell.text_frame.word_wrap = True
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Arial"
            p.font.size = Pt(8.5)
            p.font.color.rgb = DARK_TEXT
            if ci == 0:
                p.alignment = PP_ALIGN.CENTER
                p.font.bold = True

    # ==========================================
    # SLIDE 7: CHALLENGES AND GAPS IN CURRENT RESEARCH
    # ==========================================
    s7 = prs.slides.add_slide(blank_slide_layout)
    set_slide_bg(s7)
    add_header(s7, "CHALLENGES AND GAPS IN CURRENT RESEARCH", "7 of 12")

    r7 = 6
    c7 = 4
    t7_shape = s7.shapes.add_table(r7, c7, Inches(0.8), Inches(1.4), Inches(11.73), Inches(5.2))
    t7 = t7_shape.table
    t7.columns[0].width = Inches(0.8)
    t7.columns[1].width = Inches(2.6)
    t7.columns[2].width = Inches(4.3)
    t7.columns[3].width = Inches(4.03)

    h7 = ["S.No", "Challenge", "Description", "Research Gap"]
    for ci, h in enumerate(h7):
        cell = t7.cell(0, ci)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        cell.text_frame.margin_left = cell.text_frame.margin_right = Inches(0.08)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE
        if ci == 0:
            p.alignment = PP_ALIGN.CENTER

    gaps = [
        ("1", "Semantic & Lexical Ambiguity in Campus Queries", 
         "Students ask queries with informal jargon, abbreviations ('aiml', 'btech convener fee'), and spelling errors that confound rigid databases.", 
         "Lack of robust domain-specific fuzzy entity mapping and multi-turn conversational context carryover in existing university systems."),
        
        ("2", "Multi-Hop Relational Knowledge Traversal", 
         "Answering questions like 'Which professor teaches Data Science and what are their qualifications?' spans multiple entity layers.", 
         "Existing campus bots only answer single-relation factoids; complex graph traversal methods suffer from high computational latency."),

        ("3", "Stale Data & Lack of Automatic Graph Updates", 
         "Institutional data (intake, fees, faculty, placement metrics) changes frequently across semesters.", 
         "Most KGQA research assumes static pre-indexed graphs, lacking automated live synchronization when database records are updated."),

        ("4", "Black-Box Hallucinations vs. Opaque Graph Answers", 
         "Pure LLMs fabricate statistics, while traditional SPARQL/Cypher query results produce rigid tabular dumps without natural phrasing.", 
         "Need for verified, grounded graph traversal paired with natural language synthesis and zero hallucination."),

        ("5", "Absence of Intuitive Graph Visualizations", 
         "Non-technical students and administrators cannot inspect relationships, explore prerequisite connections, or verify knowledge nodes.", 
         "Complete omission of interactive web-based visual exploration tools (e.g., D3.js force graphs) in educational QA systems.")
    ]

    for ri, row in enumerate(gaps):
        for ci, val in enumerate(row):
            cell = t7.cell(ri + 1, ci)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if ri % 2 == 0 else RGBColor(241, 245, 249)
            cell.text_frame.margin_left = cell.text_frame.margin_right = Inches(0.08)
            cell.text_frame.word_wrap = True
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Arial"
            p.font.size = Pt(9.5)
            p.font.color.rgb = DARK_TEXT
            if ci == 0:
                p.alignment = PP_ALIGN.CENTER
                p.font.bold = True

    # ==========================================
    # SLIDE 8: PROPOSED SYSTEM
    # ==========================================
    s8 = prs.slides.add_slide(blank_slide_layout)
    set_slide_bg(s8)
    add_header(s8, "PROPOSED SYSTEM", "8 of 12")

    ov_c = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.3), Inches(11.73), Inches(1.1))
    ov_c.fill.solid()
    ov_c.fill.fore_color.rgb = WHITE
    ov_c.line.color.rgb = BLUE_ACCENT
    ov_c.line.width = Pt(1.5)
    ov_tf = ov_c.text_frame
    ov_tf.word_wrap = True
    ov_tf.margin_left = Inches(0.2)
    ov_tf.margin_right = Inches(0.2)
    p = ov_tf.paragraphs[0]
    p.text = "❑   Overview of the Proposed Solution:"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT
    p2 = ov_tf.add_paragraph()
    p2.text = "A multi-layered Knowledge Graph-based QA & Management System combining an NLP Intent/Entity Parser, a NetworkX Graph Traversal Engine, an automated live Graph Updation CRUD engine, and an interactive D3.js Force-Directed Graph visualization portal."
    p2.font.name = "Arial"
    p2.font.size = Pt(11)
    p2.font.color.rgb = DARK_TEXT

    pipe_y = Inches(2.6)
    pipe_w = Inches(2.65)
    pipe_h = Inches(3.9)
    pipe_gap = Inches(0.38)

    pipeline = [
        ("1. NLP Input & Parsing", 
         [("User Natural Query", "E.g., 'What are the fees for CSE and who is the HOD?'"),
          ("Intent Classifier", "TF-IDF + Cosine Similarity over 16+ intent classes"),
          ("Entity Extractor", "Regex patterns, keyword maps, and fuzzy alias resolution"),
          ("Context Carryover", "Multi-turn conversational state tracking")]),

        ("2. Graph Query Engine", 
         [("NetworkX DiGraph", "150+ nodes across 20 entity types & 24 formal relations"),
          ("Multi-Hop Traversal", "Resolves College ➔ Dept ➔ HOD / Courses / Labs / Faculty"),
          ("Factual Retrieval", "Extracts ground truth without generative hallucination"),
          ("Fallback Search", "General sub-string & fuzzy graph search")]),

        ("3. Dynamic Updation", 
         [("Admin Web Portal", "Role-authenticated management for college records"),
          ("Real-time Ingestion", "Live CRUD operations directly modify graph nodes/edges"),
          ("Persistence Sync", "Automatic write-back to persistent JSON and SQLite DB"),
          ("Zero Downtime", "In-memory graph reloads without restarting the server")]),

        ("4. Interactive Visual UI", 
         [("Modern Chatbot UI", "Typewriter animation, quick suggestions & feedback"),
          ("D3.js Force Graph", "Interactive entity nodes, relationship links, pan & zoom"),
          ("Filter & Search Bar", "Color-coded node groups (Faculty, Depts, Facilities)"),
          ("Multi-Role Portals", "Custom views for Students, Faculty, and Administrators")])
    ]

    for idx, (title, points) in enumerate(pipeline):
        px = Inches(0.8) + idx * (pipe_w + pipe_gap)
        pcard = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, pipe_y, pipe_w, pipe_h)
        pcard.fill.solid()
        pcard.fill.fore_color.rgb = WHITE
        pcard.line.color.rgb = BORDER_COLOR
        pcard.line.width = Pt(1)

        pctf = pcard.text_frame
        pctf.word_wrap = True
        pctf.margin_left = pctf.margin_right = Inches(0.12)
        pctf.margin_top = Inches(0.12)

        ptit = pctf.paragraphs[0]
        ptit.text = title
        ptit.font.name = "Arial"
        ptit.font.size = Pt(12)
        ptit.font.bold = True
        ptit.font.color.rgb = BLUE_ACCENT
        ptit.space_after = Pt(8)

        for phead, pdesc in points:
            ph = pctf.add_paragraph()
            ph.text = f"• {phead}:"
            ph.font.name = "Arial"
            ph.font.size = Pt(9.5)
            ph.font.bold = True
            ph.font.color.rgb = NAVY

            pd = pctf.add_paragraph()
            pd.text = f"  {pdesc}"
            pd.font.name = "Arial"
            pd.font.size = Pt(8.5)
            pd.font.color.rgb = DARK_TEXT
            pd.space_after = Pt(4)

    # ==========================================
    # SLIDE 9: ROLES & RESPONSIBILITIES
    # ==========================================
    s9 = prs.slides.add_slide(blank_slide_layout)
    set_slide_bg(s9)
    add_header(s9, "ROLES & RESPONSIBILITIES", "9 of 12")

    r9 = 7
    c9 = 2
    t9_shape = s9.shapes.add_table(r9, c9, Inches(1.2), Inches(1.5), Inches(10.93), Inches(4.8))
    t9 = t9_shape.table
    t9.columns[0].width = Inches(3.2)
    t9.columns[1].width = Inches(7.73)

    roles = [
        ("Project Leader", "Project coordination, sprint planning, architectural documentation, client/guide communication, and overall integration."),
        ("Member 1", "Comprehensive literature survey, requirement analysis, ontology specification, and dataset curation (college_data.json)."),
        ("Member 2", "System design & architecture, NetworkX knowledge graph modeling, ontology validation rules, and database schema setup."),
        ("Member 3", "NLP processor development (TF-IDF vectorizer, intent classification, fuzzy entity matching) and Flask backend API integration."),
        ("Member 4", "Frontend chatbot interface, D3.js interactive graph visualization, automated test suite execution, and validation reporting."),
        ("Guide / Supervisor", "Technical supervision, periodic milestone reviews, algorithmic guidance, and research manuscript mentorship.")
    ]

    for ri, (role, resp) in enumerate(roles):
        c0 = t9.cell(ri, 0)
        c0.fill.solid()
        c0.fill.fore_color.rgb = NAVY if ri == 0 or ri == 5 else WHITE
        c0.text_frame.margin_left = Inches(0.15)
        c0.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        p0 = c0.text_frame.paragraphs[0]
        p0.text = role
        p0.font.name = "Arial"
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = WHITE if ri == 0 or ri == 5 else BLUE_ACCENT

        c1 = t9.cell(ri, 1)
        c1.fill.solid()
        c1.fill.fore_color.rgb = RGBColor(241, 245, 249) if ri % 2 == 1 else WHITE
        c1.text_frame.margin_left = Inches(0.15)
        c1.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        p1 = c1.text_frame.paragraphs[0]
        p1.text = resp
        p1.font.name = "Arial"
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = DARK_TEXT

    # ==========================================
    # SLIDE 10: REQUIREMENTS
    # ==========================================
    s10 = prs.slides.add_slide(blank_slide_layout)
    set_slide_bg(s10)
    add_header(s10, "REQUIREMENTS", "10 of 12")

    req_cols = [
        ("Hardware Requirements", 
         [("Processor", "Intel Core i5 / AMD Ryzen 5 or higher"),
          ("RAM", "8 GB minimum (16 GB recommended)"),
          ("Storage", "256 GB SSD (500 MB for app & DB)"),
          ("Internet", "High-speed broadband for cloud/CDN"),
          ("Other", "Standard monitor with 1080p display")]),

        ("Software Requirements", 
         [("Operating System", "Windows 10/11, Linux, or macOS"),
          ("Language", "Python 3.11+ & JavaScript ES6+"),
          ("Frameworks", "Flask 3.1, NetworkX 3.4, Scikit-learn"),
          ("Database", "SQLite with Flask-SQLAlchemy 3.1"),
          ("Environment", "VS Code, Git, python-dotenv"),
          ("Deployment", "Gunicorn 23.0 & Render Cloud")]),

        ("Functional Requirements", 
         [("User Auth", "Registration, login & role-based approval"),
          ("Data Ingestion", "Admin CRUD for adding entities & edges"),
          ("Core QA Engine", "NLP intent routing & graph traversal"),
          ("Real-Time Update", "Instant graph sync without server reboot"),
          ("Interactive Graph", "D3.js dynamic graph visual exploration"),
          ("Feedback System", "Message rating & conversation analytics")]),

        ("Non-Functional Requirements", 
         [("Performance", "Sub-150ms query response time"),
          ("Accuracy", "Zero hallucination on factual queries"),
          ("Reliability", "99.9% uptime with graceful fallbacks"),
          ("Scalability", "Easily extends to 10,000+ graph nodes"),
          ("Usability", "Responsive UI, dark/light theme support"),
          ("Maintainability", "Modular separation of graph & web views")])
    ]

    col_w = Inches(2.75)
    col_gap = Inches(0.24)
    col_top = Inches(1.35)
    col_h = Inches(5.3)

    for ci, (title, items) in enumerate(req_cols):
        cx = Inches(0.8) + ci * (col_w + col_gap)
        card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, col_top, col_w, col_h)
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = BORDER_COLOR
        card.line.width = Pt(1)

        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_right = Inches(0.12)
        ctf.margin_top = Inches(0.15)

        tp = ctf.paragraphs[0]
        tp.text = title
        tp.font.name = "Arial"
        tp.font.size = Pt(12)
        tp.font.bold = True
        tp.font.color.rgb = BLUE_ACCENT
        tp.space_after = Pt(10)

        for label, val in items:
            lp = ctf.add_paragraph()
            lp.text = f"• {label}:"
            lp.font.name = "Arial"
            lp.font.size = Pt(9.5)
            lp.font.bold = True
            lp.font.color.rgb = NAVY

            vp = ctf.add_paragraph()
            vp.text = f"  {val}"
            vp.font.name = "Arial"
            vp.font.size = Pt(8.5)
            vp.font.color.rgb = DARK_TEXT
            vp.space_after = Pt(4)

    # ==========================================
    # SLIDE 11: TIMELINE / PROJECT SCHEDULE
    # ==========================================
    s11 = prs.slides.add_slide(blank_slide_layout)
    set_slide_bg(s11)
    add_header(s11, "TIMELINE / PROJECT SCHEDULE", "11 of 12")

    r11 = 17
    c11 = 3
    t11_shape = s11.shapes.add_table(r11, c11, Inches(0.8), Inches(1.3), Inches(11.73), Inches(5.4))
    t11 = t11_shape.table
    t11.columns[0].width = Inches(1.6)
    t11.columns[1].width = Inches(7.53)
    t11.columns[2].width = Inches(2.6)

    for ci, h in enumerate(["Phase", "Activities", "Month"]):
        cell = t11.cell(0, ci)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        cell.text_frame.margin_left = Inches(0.1)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = WHITE
        if ci in [0, 2]:
            p.alignment = PP_ALIGN.CENTER

    timeline_data = [
        ("SEM-I", "FIRST SEMESTER MILESTONES", "2026", True, False),
        ("Phase 1", "Problem identification & topic finalization", "AUG", False, False),
        ("Phase 2", "Literature survey & existing-system study", "AUG & SEP", False, False),
        ("Phase 3", "Requirement analysis & specification", "SEP", False, False),
        ("Milestone", "Review paper write up and submit to journals", "(Oct)", False, True),
        ("Phase 4", "System design, ontology formalization & architecture", "Sep & Oct", False, False),
        ("Phase 5", "Implementation & development (NLP + KG + Flask)", "Sep & Oct", False, False),
        ("Phase 6", "Testing, debugging & graph validation", "Sep & Oct", False, False),
        ("Phase 7", "Results compilation & performance evaluation", "Oct & Nov", False, False),
        ("Milestone", "Full paper write up and submit to journals / IEEE conferences", "(Dec-26)", False, True),
        ("SEM-II", "SECOND SEMESTER MILESTONES", "2027", True, False),
        ("Phase 8", "Deploy the project in cloud (Render / Production Web Server)", "Jan, Feb-27", False, False),
        ("Phase 9", "Comprehensive documentation & final major project report", "Feb, Mar-27", False, False),
        ("Phase 10", "Attending conferences / paper publication acceptance", "(1st Week of Mar)", False, False),
        ("Final", "Final review & viva presentation", "1st Week of April-27", False, True),
    ]

    for ri, (ph, act, mn, is_hdr, is_hl) in enumerate(timeline_data):
        row_idx = ri + 1
        for ci, val in enumerate([ph, act, mn]):
            cell = t11.cell(row_idx, ci)
            cell.fill.solid()
            if is_hdr:
                cell.fill.fore_color.rgb = BLUE_ACCENT
            elif is_hl:
                cell.fill.fore_color.rgb = RGBColor(254, 240, 138)
            else:
                cell.fill.fore_color.rgb = WHITE if row_idx % 2 == 0 else RGBColor(241, 245, 249)
            
            cell.text_frame.margin_left = cell.text_frame.margin_right = Inches(0.08)
            cell.text_frame.margin_top = cell.text_frame.margin_bottom = Inches(0.02)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Arial"
            p.font.size = Pt(8.5)
            if is_hdr:
                p.font.bold = True
                p.font.color.rgb = WHITE
            elif is_hl:
                p.font.bold = True
                p.font.color.rgb = RGBColor(146, 64, 14)
            else:
                p.font.color.rgb = DARK_TEXT
                if ci == 0:
                    p.font.bold = True
            if ci in [0, 2]:
                p.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 12: REFERENCES
    # ==========================================
    s12 = prs.slides.add_slide(blank_slide_layout)
    set_slide_bg(s12)
    add_header(s12, "REFERENCES", "12 of 12")

    ref_box = s12.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.73), Inches(5.1))
    rtf = ref_box.text_frame
    rtf.word_wrap = True

    references = [
        "1.  Y. Wang, N. Lipka, R. A. Rossi, A. Siu, R. Zhang, and T. Derr, \"Knowledge Graph Prompting for Multi-Document Question Answering,\" in Proceedings of the AAAI Conference on Artificial Intelligence (AAAI-24), vol. 38, no. 17, pp. 19206–19214, 2024. [https://ojs.aaai.org/index.php/AAAI/article/view/29889]",
        "2.  M. Yani and A. A. Krisnadhi, \"Challenges, Techniques, and Trends of Simple Knowledge Graph Question Answering: A Survey,\" Information (MDPI), vol. 12, no. 7, art. no. 271, 2021. [https://www.mdpi.com/2078-2489/12/7/271]",
        "3.  Y. Song, W. Li, G. Dai, and X. Shang, \"Advancements in Complex Knowledge Graph Question Answering: A Survey,\" Electronics (MDPI), vol. 12, no. 21, art. no. 4395, 2023. [https://www.mdpi.com/2079-9292/12/21/4395]",
        "4.  P. Sen, S. Mavadia, and A. Saffari, \"Knowledge Graph-augmented Language Models for Complex Question Answering,\" in Proceedings of the 1st Workshop on Natural Language Reasoning and Structured Explanations (NLRSE @ ACL 2023), pp. 45–54, 2023.",
        "5.  J. Leng, Y. Yang, R. Lin, and Y. Tang, \"Question Answering System Based on University Knowledge Graph,\" in Computer Supported Cooperative Work and Social Computing (CCIS), vol. 1827, Springer, pp. 164–174, 2023. [DOI: 10.1007/978-981-99-2385-4_12]",
        "6.  K. Aneja, M. Srivastava, S. Das, and N. Aneja, \"Interpretable Question Answering with Knowledge Graphs,\" arXiv preprint arXiv:2510.19181, 2025. [https://arxiv.org/abs/2510.19181]",
        "7.  B. P. Swathi, M. Geetha, G. Attigeri, M. V. Suhas, and S. Halaharvi, \"Optimizing Question Answering Systems in Education: Addressing Domain-Specific Challenges,\" IEEE Access, vol. 12, pp. 156572–156587, 2024."
    ]

    for ri, ref in enumerate(references):
        p = rtf.paragraphs[0] if ri == 0 else rtf.add_paragraph()
        p.text = ref
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(6)

    note_box = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.5), Inches(11.73), Inches(0.5))
    note_box.fill.solid()
    note_box.fill.fore_color.rgb = RGBColor(254, 240, 138)
    note_box.line.color.rgb = RGBColor(202, 138, 4)
    note_box.line.width = Pt(1)
    np = note_box.text_frame.paragraphs[0]
    np.text = "Note: Order of references strictly matches with the Literature review summary order (Slide no: 6)"
    np.alignment = PP_ALIGN.CENTER
    np.font.name = "Arial"
    np.font.size = Pt(11)
    np.font.bold = True
    np.font.color.rgb = RGBColor(133, 77, 14)

    # ==========================================
    # SLIDE 13: THANK YOU..!
    # ==========================================
    s13 = prs.slides.add_slide(blank_slide_layout)
    set_slide_bg(s13, RGBColor(241, 245, 249))

    ty_box = s13.shapes.add_textbox(Inches(1.5), Inches(2.3), Inches(10.33), Inches(2.8))
    ty_tf = ty_box.text_frame
    ty_tf.word_wrap = True

    p = ty_tf.paragraphs[0]
    p.text = "THANK YOU..!"
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Arial"
    p.font.size = Pt(46)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p2 = ty_tf.add_paragraph()
    p2.text = "Questions & Feedback"
    p2.alignment = PP_ALIGN.CENTER
    p2.font.name = "Arial"
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = CYAN
    p2.space_after = Pt(20)

    p3 = ty_tf.add_paragraph()
    p3.text = "Department of Computer Science and Engineering\nSphoorthy Engineering College (UGC Autonomous), Hyderabad"
    p3.alignment = PP_ALIGN.CENTER
    p3.font.name = "Arial"
    p3.font.size = Pt(14)
    p3.font.color.rgb = MUTED_TEXT

    num13 = s13.shapes.add_textbox(Inches(11.2), Inches(6.9), Inches(1.5), Inches(0.4))
    np13 = num13.text_frame.paragraphs[0]
    np13.text = "(#) of 12"
    np13.alignment = PP_ALIGN.RIGHT
    np13.font.size = Pt(11)
    np13.font.color.rgb = MUTED_TEXT

    # Save presentation
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == '__main__':
    out_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "Project_Review_1_Synopsis_Presentation.pptx")
    create_presentation(out_file)

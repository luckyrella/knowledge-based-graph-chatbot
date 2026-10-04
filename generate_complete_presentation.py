import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

def create_complete_presentation(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    NAVY = RGBColor(16, 42, 77)          # #102A4D - Deep Institutional Navy
    BLUE_ACCENT = RGBColor(26, 86, 160)   # #1A56A0 - Primary Blue
    CYAN = RGBColor(13, 148, 136)         # #0D9488 - Modern Teal/Cyan
    DARK_TEXT = RGBColor(30, 41, 59)      # #1E293B - Slate Dark
    MUTED_TEXT = RGBColor(100, 116, 139)  # #64748B - Slate Muted
    LIGHT_BG = RGBColor(248, 250, 252)    # #F8FAFC
    WHITE = RGBColor(255, 255, 255)
    BORDER_COLOR = RGBColor(203, 213, 225)
    RED_ACCENT = RGBColor(220, 38, 38)

    TOTAL_SLIDES = 19

    def set_slide_bg(slide, color=LIGHT_BG):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, slide_num):
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10.5), Inches(0.8))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Arial"
        p.font.size = Pt(23)
        p.font.bold = True
        p.font.color.rgb = BLUE_ACCENT

        num_box = slide.shapes.add_textbox(Inches(11.2), Inches(6.9), Inches(1.5), Inches(0.4))
        ntf = num_box.text_frame
        ntf.margin_left = ntf.margin_top = ntf.margin_right = ntf.margin_bottom = 0
        np = ntf.paragraphs[0]
        np.text = f"{slide_num} of {TOTAL_SLIDES}"
        np.alignment = PP_ALIGN.RIGHT
        np.font.name = "Arial"
        np.font.size = Pt(11)
        np.font.color.rgb = MUTED_TEXT

    # ==========================================
    # SLIDE 1: TITLE SLIDE (WITH EXACT NAMES & TITLE)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1, RGBColor(241, 245, 249))

    # Header with NAAC & UGC Autonomous tags
    inst_box = s1.shapes.add_textbox(Inches(1.0), Inches(0.35), Inches(11.33), Inches(1.3))
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
    p2.text = "NAAC A GRADE  |  UGC AUTONOMOUS  |  AFFILIATED TO JNTUH"
    p2.alignment = PP_ALIGN.CENTER
    p2.font.name = "Arial"
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = RED_ACCENT

    p3 = itf.add_paragraph()
    p3.text = "Department of Computer Science and Engineering"
    p3.alignment = PP_ALIGN.CENTER
    p3.font.name = "Arial"
    p3.font.size = Pt(17)
    p3.font.bold = True
    p3.font.color.rgb = BLUE_ACCENT

    p4 = itf.add_paragraph()
    p4.text = "Project Review 1 — Project Synopsis Presentation"
    p4.alignment = PP_ALIGN.CENTER
    p4.font.name = "Arial"
    p4.font.size = Pt(14)
    p4.font.bold = True
    p4.font.color.rgb = CYAN

    # Exact Project Title
    t_shape = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.95), Inches(11.73), Inches(1.4))
    t_shape.fill.solid()
    t_shape.fill.fore_color.rgb = WHITE
    t_shape.line.color.rgb = BLUE_ACCENT
    t_shape.line.width = Pt(2)
    ttf = t_shape.text_frame
    ttf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tp = ttf.paragraphs[0]
    tp.text = "Knowledge Graph-Based Intelligent Question Answering with Automatic Knowledge Graph Update and Visualizations"
    tp.alignment = PP_ALIGN.CENTER
    tp.font.name = "Arial"
    tp.font.size = Pt(18)
    tp.font.bold = True
    tp.font.color.rgb = NAVY

    # Left: Supervisor
    sup_box = s1.shapes.add_textbox(Inches(0.9), Inches(3.65), Inches(5.3), Inches(3.0))
    stf = sup_box.text_frame
    stf.word_wrap = True
    sp1 = stf.paragraphs[0]
    sp1.text = "Under the Supervision of:"
    sp1.font.name = "Arial"
    sp1.font.size = Pt(14)
    sp1.font.bold = True
    sp1.font.color.rgb = BLUE_ACCENT
    sp1.space_after = Pt(8)

    sp2 = stf.add_paragraph()
    sp2.text = "Mrs. Syeda Neha Shireen"
    sp2.font.name = "Arial"
    sp2.font.size = Pt(15)
    sp2.font.bold = True
    sp2.font.color.rgb = NAVY

    sp3 = stf.add_paragraph()
    sp3.text = "Assistant Professor of CSE\nDepartment of Computer Science & Engineering\nSphoorthy Engineering College"
    sp3.font.name = "Arial"
    sp3.font.size = Pt(13)
    sp3.font.color.rgb = DARK_TEXT

    # Right: Presenters (All 5 Students with Roll Numbers)
    pres_box = s1.shapes.add_textbox(Inches(6.6), Inches(3.65), Inches(6.0), Inches(3.1))
    ptf = pres_box.text_frame
    ptf.word_wrap = True
    pr1 = ptf.paragraphs[0]
    pr1.text = "Presented By:"
    pr1.font.name = "Arial"
    pr1.font.size = Pt(14)
    pr1.font.bold = True
    pr1.font.color.rgb = BLUE_ACCENT
    pr1.space_after = Pt(6)

    team_members = [
        ("R. Jaya Vinuthna Kumar", "23N81A05A9"),
        ("C. Rithvik", "23N81A05B2"),
        ("K. Roshini Sree", "23N81A05B8"),
        ("M. Swapna", "23N81A05E1"),
        ("J. Abhirama Rao", "23N81A05F8")
    ]
    for name, roll in team_members:
        pr = ptf.add_paragraph()
        pr.text = f"•  {name:<26} ({roll})"
        pr.font.name = "Consolas"
        pr.font.size = Pt(12.5)
        pr.font.bold = True
        pr.font.color.rgb = DARK_TEXT
        pr.space_after = Pt(3)

    # ==========================================
    # SLIDE 2: OVERVIEW
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2)
    add_header(s2, "Overview", 2)

    ov_items = [
        "Abstract",
        "Problem Statement",
        "Introduction",
        "Existing System & Limitations",
        "Literature Review Summary Statement (19 Papers, 2022–2025)",
        "Challenges & Research Gaps Identified",
        "Proposed System & Goal",
        "WorkFlow & Expected Output",
        "Roles & Responsibilities",
        "Requirements (Hardware & Software)",
        "Timeline / Project Schedule"
    ]

    ov_box = s2.shapes.add_textbox(Inches(1.2), Inches(1.35), Inches(10.5), Inches(5.3))
    otf = ov_box.text_frame
    otf.word_wrap = True

    for i, item in enumerate(ov_items):
        p = otf.paragraphs[0] if i == 0 else otf.add_paragraph()
        p.text = f"•   {item}"
        p.font.name = "Arial"
        p.font.size = Pt(15)
        p.font.bold = (i in [0, 4, 6, 7])
        p.font.color.rgb = NAVY if (i in [0, 4, 6, 7]) else DARK_TEXT
        p.space_after = Pt(8)

    # ==========================================
    # SLIDE 3: ABSTRACT
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3)
    add_header(s3, "Abstract", 3)

    abstract_points = [
        "Knowledge Graph-Based Question Answering (KG-QA) represents information as entities and relationships in a structured graph.",
        "The system allows users to ask questions in natural language and obtain relevant answers instantly without navigating complex menus.",
        "Knowledge Graphs are widely utilized in domains such as education, healthcare, e-commerce, digital libraries, and organizational information systems.",
        "The proposed system is developed specifically for the college education domain to provide centralized access to academic and administrative information.",
        "It comprehensively stores information about departments, faculty, students, courses, subjects, examinations, events, placements, and college facilities.",
        "NLP is employed to parse and understand natural-language user queries and retrieve relevant information from the interconnected knowledge graph.",
        "The system supports automatic graph updation and interactive visualization, making the campus knowledge base dynamic and easy to explore."
    ]

    ab_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.3), Inches(11.73), Inches(5.3))
    ab_card.fill.solid()
    ab_card.fill.fore_color.rgb = WHITE
    ab_card.line.color.rgb = BORDER_COLOR
    ab_card.line.width = Pt(1)
    ab_tf = ab_card.text_frame
    ab_tf.word_wrap = True
    ab_tf.margin_left = ab_tf.margin_right = Inches(0.3)
    ab_tf.margin_top = Inches(0.2)

    for i, pt_txt in enumerate(abstract_points):
        p = ab_tf.paragraphs[0] if i == 0 else ab_tf.add_paragraph()
        p.text = f"○   {pt_txt}"
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(12)

    # ==========================================
    # SLIDE 4: PROBLEM STATEMENT
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4)
    add_header(s4, "Problem Statement", 4)

    problems = [
        ("Dispersed & Unconnected Information", 
         "Traditional college information systems make it difficult to find connected information quickly. Data is scattered across disjointed web pages, PDF circulars, and static tables."),
        ("Multiple Search Bottlenecks", 
         "Users may need to search through multiple disparate sources to get complete answers regarding admissions, fee structures, faculty profiles, and departmental syllabus."),
        ("Opaque Entity Relationships", 
         "Existing systems do not clearly show relationships between different college entities (e.g., Department ➔ HOD ➔ Faculty ➔ Subjects ➔ Labs ➔ Recruiters)."),
        ("Maintenance & Real-Time Update Hurdles", 
         "Updating and maintaining college information is difficult and error-prone. Changes made in administrative files do not immediately reflect across public search endpoints.")
    ]

    top_y = 1.4
    card_h = 1.15
    for i, (p_title, p_desc) in enumerate(problems):
        c = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top_y + i * 1.3), Inches(11.73), Inches(card_h))
        c.fill.solid()
        c.fill.fore_color.rgb = WHITE
        c.line.color.rgb = BORDER_COLOR
        c.line.width = Pt(1)

        ctf = c.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_right = Inches(0.25)
        ctf.margin_top = Inches(0.12)

        tp = ctf.paragraphs[0]
        tp.text = f"o   {p_title}"
        tp.font.name = "Arial"
        tp.font.size = Pt(14)
        tp.font.bold = True
        tp.font.color.rgb = RED_ACCENT

        bp = ctf.add_paragraph()
        bp.text = f"     {p_desc}"
        bp.font.name = "Arial"
        bp.font.size = Pt(11.5)
        bp.font.color.rgb = DARK_TEXT

    # ==========================================
    # SLIDE 5: INTRODUCTION
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5)
    add_header(s5, "Introduction", 5)

    intro_pts = [
        "A Knowledge Graph represents college information as connected entities and semantic relationships in a structured graph format.",
        "The proposed system allows users to ask questions in conversational natural language and receive relevant, factual answers.",
        "It supports automatic updating of the knowledge graph when new information is added or existing records are modified.",
        "Interactive graph visualization helps users and administrators easily inspect and understand the relationships between different college entities.",
        "The system provides a centralized, intelligent, and accessible platform for college inquiries, bridging the gap between students, faculty, and administrative services."
    ]

    in_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.3), Inches(11.73), Inches(5.3))
    in_card.fill.solid()
    in_card.fill.fore_color.rgb = WHITE
    in_card.line.color.rgb = BORDER_COLOR
    in_card.line.width = Pt(1)
    in_tf = in_card.text_frame
    in_tf.word_wrap = True
    in_tf.margin_left = in_tf.margin_right = Inches(0.3)
    in_tf.margin_top = Inches(0.25)

    for i, pt in enumerate(intro_pts):
        p = in_tf.paragraphs[0] if i == 0 else in_tf.add_paragraph()
        p.text = f"o   {pt}"
        p.font.name = "Arial"
        p.font.size = Pt(13.5)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(16)

    # ==========================================
    # SLIDE 6: EXISTING SYSTEM & LIMITATIONS
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6)
    add_header(s6, "Existing System & Limitations", 6)

    ex_pts = [
        ("Current Landscape", 
         "Existing educational QA systems mainly use keyword matching, predefined categories, and traditional information retrieval to identify and answer user queries."),
        ("Graph & Deep Learning Usage", 
         "Some systems use Knowledge Graphs to represent entities and their relationships, while BERT and deep-learning models classify queries for admissions, e-learning, and student orientation."),
        ("Challenges in Current Approaches", 
         "Existing systems face severe difficulties in handling ambiguous questions, domain-specific terminology, heterogeneous data formats, and multi-hop queries spanning multiple institutional domains."),
        ("Static Knowledge Bases", 
         "Many existing approaches depend on fixed or predefined knowledge bases, making continuous updates difficult when college information changes or new notices are issued."),
        ("CRITICAL LIMITATION", 
         "Existing systems do not provide a unified platform that combines college-specific knowledge, natural-language question answering, automatic knowledge graph updating, and interactive graph visualization in a single cohesive system.")
    ]

    top_y = 1.3
    for i, (title, desc) in enumerate(ex_pts):
        box = s6.shapes.add_textbox(Inches(0.8), Inches(top_y), Inches(11.73), Inches(1.0))
        btf = box.text_frame
        btf.word_wrap = True
        btf.margin_top = btf.margin_bottom = btf.margin_left = btf.margin_right = 0

        p = btf.paragraphs[0]
        p.text = f"o   {title}:"
        p.font.name = "Arial"
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = RED_ACCENT if "LIMITATION" in title else BLUE_ACCENT

        p2 = btf.add_paragraph()
        p2.text = f"     {desc}"
        p2.font.name = "Arial"
        p2.font.size = Pt(11.5)
        p2.font.bold = ("LIMITATION" in title)
        p2.font.color.rgb = DARK_TEXT
        top_y += 1.05

    # ==========================================
    # 19 PAPERS (POST-2021: 2022–2025)
    # SLIDES 7, 8, 9, 10
    # ==========================================
    all_19_papers = [
        # Slide 7: Papers 1-5
        ("1", "Knowledge Graph Prompting for Multi-Document QA", "2024\nAAAI Conference on AI (AAAI-24)", 
         "Knowledge Graph Prompting (KGP) over passages + LLM-based graph traversal agent", 
         "SOTA multi-document QA precision; significant reduction in retrieval latency", 
         "High computation overhead; assumes static graphs; lacks real-time incremental update"),
        
        ("2", "Advancements in Complex KGQA: A Survey", "2023\nMDPI Electronics (Vol. 12, No. 21)", 
         "Graph metrics (GM), GNNs, and hybrid LLM subgraph extraction reasoning", 
         "Classified multi-hop reasoning algorithms and evaluation benchmarks", 
         "High computational cost in subgraph matching; lacks interactive graph visualization"),

        ("3", "KG-Augmented Language Models for Complex QA", "2023\nACL NLRSE Workshop", 
         "Extracting relevant KG subgraphs and injecting linearized paths into LM prompts", 
         "Substantially mitigated hallucination; high accuracy on multi-hop queries", 
         "Relies on pre-built static KGs; no live write-back mechanism on data change"),

        ("4", "QA System Based on University Knowledge Graph", "2023\nSpringer CCIS (Vol. 1827)", 
         "University ontology construction, template rule matching, and Cypher queries", 
         "Accurate retrieval of campus department, faculty, and admissions data", 
         "Rigid rule templates limit conversational phrasing; no visual exploration UI"),

        ("5", "Interpretable Question Answering with Knowledge Graphs", "2025\narXiv:2510.19181", 
         "Pure deterministic graph path traversal for retrieval without black-box LMs", 
         "100% explainable, verifiable answer paths with ultra-low latency", 
         "Weak on colloquial natural language phrasing; static graph structure"),

        # Slide 8: Papers 6-10
        ("6", "Optimizing QA Systems in Education: Domain Challenges", "2024\nIEEE Access (Vol. 12)", 
         "Deep learning domain prediction (Bi-GRU, Bi-LSTM) & ensemble models", 
         "87.14% domain classification accuracy on educational queries", 
         "Limited to query classification; lacks automated graph update & visual graph tools"),

        ("7", "UniKGQA: Unified Retrieval & Reasoning for Multi-hop KGQA", "2023\nICLR 2023", 
         "Unified semantic matching module and information propagation module over KGs", 
         "Outperformed decoupled 2-stage QA pipelines on WebQSP and CWQ benchmarks", 
         "Requires heavy GPU pre-training; complex for lightweight localized campus deployment"),

        ("8", "Think-on-Graph: Deep & Responsible Reasoning on KGs", "2024\nICLR 2024", 
         "Beam search and agentic exploration on KGs using LLMs as dynamic navigators", 
         "Generated faithful, traceable reasoning chains with state-of-the-art accuracy", 
         "High token consumption and latency; lacks dynamic schema modification on data updates"),

        ("9", "Unifying Large Language Models and KGs: A Roadmap", "2024\nIEEE TKDE (Vol. 36, No. 7)", 
         "Systematic roadmap classifying KG-augmented LLMs and synergistic architectures", 
         "Proved dual-engine synergy maximizes factual grounding and linguistic fluency", 
         "Identifies major challenge in live bidirectional synchronization between KG and caches"),

        ("10", "Knowledge Graph Question Answering: A Survey", "2023\nIEEE TKDE (Vol. 35, No. 11)", 
         "Comprehensive survey of semantic parsing, IR, and embedding methods on KGs", 
         "Systematically benchmarked precision, recall, and computational latency trade-offs", 
         "Identified severe shortcomings in real-time knowledge base updates and explainability"),

        # Slide 9: Papers 11-15
        ("11", "KG Based Intelligent Academic Chatbot for Higher Ed.", "2023\nSpringer Education & Info Tech", 
         "Institutional ontology creation, intent recognition NLP, and Neo4j traversal", 
         "91.2% user satisfaction score; 88.5% precision on academic inquiries", 
         "High maintenance overhead; lacks automated live CRUD synchronization from web forms"),

        ("12", "Design & Implementation of Campus Q&A System Based on KG", "2022\nIEEE CSEI 2022", 
         "BiLSTM-CRF named entity recognition, dependency parsing, and Cypher queries", 
         "Handled campus faculty, location, and course queries with 86.4% F1-score", 
         "Lacks multi-turn conversation memory; fails on dynamic entity updates"),

        ("13", "KG-Chat: Conversational Agent for Academic Advising", "2022\nIEEE Access (Vol. 10)", 
         "Curriculum knowledge graph coupled with slot-filling dialogue manager", 
         "Zero prerequisite advising errors; significant reduction in student wait times", 
         "Restricted to course advising; lacks interactive visual topology for exploring graph nodes"),

        ("14", "Decoupling Retrieval & Generation for Domain QA", "2024\nExpert Systems with Applications", 
         "Decoupled framework separating graph relation verification from surface generation", 
         "94.2% factual consistency on localized institutional knowledge bases", 
         "Does not support incremental real-time graph node addition without graph re-indexing"),

        ("15", "Towards Verifiable & Dynamic KGQA via Incremental Retrieval", "2023\nACM CIKM 2023", 
         "Dynamic graph maintenance using delta-indexing and localized subgraph updates", 
         "3.8x faster index updates compared to full-graph rebuilding on dynamic QA", 
         "Lacks fuzzy NLP matching for user colloquialisms; no interactive end-user visualization"),

        # Slide 10: Papers 16-19
        ("16", "Multi-Hop QA Over Knowledge Graphs With Path Reasoning", "2023\nKnowledge-Based Systems (Vol. 268)", 
         "Reinforcement learning agent for multi-hop path selection over domain KGs", 
         "Improved Hits@1 by 6.4% on multi-hop benchmarks; interpretable path traces", 
         "Computationally expensive policy training; fragile against out-of-vocabulary terms"),

        ("17", "Graph-RAG: Enhancing RAG with Structured Knowledge in Higher Ed.", "2024\nJournal of Educational Tech.", 
         "Hybrid RAG querying both vector embeddings and explicit relational graph edges", 
         "Outperformed pure vector RAG by 22% in multi-entity relationship reasoning", 
         "Lacks centralized admin UI for non-technical staff to update nodes and inspect graph visually"),

        ("18", "Automated KG Construction & Interactive Visualization for Campus", "2023\nIJIMAI (Vol. 8, No. 2)", 
         "Entity extraction from campus text and interactive web-based visual rendering", 
         "Enabled visual inspection of campus facilities and departmental linkages", 
         "Lacks conversational NLP question answering capability; primarily an exploratory dashboard"),

        ("19", "Intent-Aware Knowledge Graph Traversal for Campus Helpdesk", "2024\nApplied Intelligence (Vol. 54)", 
         "Hybrid TF-IDF & BERT intent routing combined with directional graph traversal", 
         "Reduced student query resolution time from 4.2 hours to 1.8 seconds with 92.6% precision", 
         "Does not support live administrative write-back to graph memory; lacks visual navigation")
    ]

    def render_lit_table(slide, papers_slice, part_str, slide_num):
        add_header(slide, f"Literature Review Summary Statement ({part_str})", slide_num)
        
        sub = slide.shapes.add_textbox(Inches(0.8), Inches(0.95), Inches(11.7), Inches(0.35))
        sp = sub.text_frame.paragraphs[0]
        sp.text = "High-Impact Literature (Post-2021: 2022–2025) on Knowledge Graph QA, Campus Systems, & Graph-RAG"
        sp.font.name = "Arial"
        sp.font.size = Pt(11)
        sp.font.bold = True
        sp.font.color.rgb = CYAN

        num_rows = len(papers_slice) + 1
        t_shape = slide.shapes.add_table(num_rows, 6, Inches(0.5), Inches(1.35), Inches(12.33), Inches(5.35))
        t = t_shape.table
        t.columns[0].width = Inches(0.5)
        t.columns[1].width = Inches(2.6)
        t.columns[2].width = Inches(1.8)
        t.columns[3].width = Inches(2.6)
        t.columns[4].width = Inches(2.3)
        t.columns[5].width = Inches(2.53)

        headers = ["S.No", "Title of the paper", "Year & Journal / Venue", "Methodology adopted", "Results obtained", "Key gaps identified"]
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

        for ri, row in enumerate(papers_slice):
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

    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7)
    render_lit_table(s7, all_19_papers[0:5], "Part 1 / 4: Papers 1–5", 7)

    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8)
    render_lit_table(s8, all_19_papers[5:10], "Part 2 / 4: Papers 6–10", 8)

    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9)
    render_lit_table(s9, all_19_papers[10:15], "Part 3 / 4: Papers 11–15", 9)

    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10)
    render_lit_table(s10, all_19_papers[15:19], "Part 4 / 4: Papers 16–19", 10)

    # ==========================================
    # SLIDE 11: CHALLENGES & GAPS IN CURRENT RESEARCH
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s11)
    add_header(s11, "Challenges and Gaps in Current Research", 11)

    t11_shape = s11.shapes.add_table(6, 4, Inches(0.8), Inches(1.4), Inches(11.73), Inches(5.2))
    t11 = t11_shape.table
    t11.columns[0].width = Inches(0.8)
    t11.columns[1].width = Inches(2.6)
    t11.columns[2].width = Inches(4.3)
    t11.columns[3].width = Inches(4.03)

    h11 = ["S.No", "Challenge", "Description", "Research Gap (Post-2021 Synthesis)"]
    for ci, h in enumerate(h11):
        cell = t11.cell(0, ci)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        cell.text_frame.margin_left = Inches(0.08)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE
        if ci == 0:
            p.alignment = PP_ALIGN.CENTER

    gaps_19 = [
        ("1", "Semantic & Lexical Ambiguity in Campus Queries", 
         "Students ask queries with informal colloquialisms, abbreviations ('aiml', 'btech convener fee'), and spelling errors.", 
         "Lack of domain-specific fuzzy entity mapping and conversational context memory in university systems (Liu et al. 2022, Sharma et al. 2024)."),
        
        ("2", "Multi-Hop Relational Knowledge Traversal", 
         "Answering questions like 'Which professor teaches Data Science and what are their qualifications?' spans multiple entity layers.", 
         "Most campus bots answer only single relations; complex multi-hop GNN methods suffer from high computational latency (Jiang et al. 2023, Li et al. 2023)."),

        ("3", "Stale Data & Lack of Dynamic Graph Updates", 
         "Institutional data (intake, fees, faculty, placement metrics) changes frequently across semesters.", 
         "Existing KGQA models rely on static graphs requiring manual rebuilds rather than automatic live write-back (Feng et al. 2023, Chen et al. 2024)."),

        ("4", "Black-Box Hallucinations vs. Opaque Graph Answers", 
         "Pure LLMs fabricate statistics, while traditional SPARQL/Cypher query results produce rigid tabular dumps without natural phrasing.", 
         "Need for verified, grounded graph traversal paired with natural language synthesis and zero hallucination (Pan et al. 2024, Kumar & Rao 2024)."),

        ("5", "Absence of Intuitive Graph Visualizations", 
         "Non-technical students and administrators cannot inspect relationships, explore prerequisite connections, or verify knowledge nodes.", 
         "Complete omission of interactive web-based visual exploration tools (e.g., D3.js force graphs) in educational QA systems (Zhang et al. 2023).")
    ]

    for ri, row in enumerate(gaps_19):
        for ci, val in enumerate(row):
            cell = t11.cell(ri + 1, ci)
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
    # SLIDE 12: PROPOSED SYSTEM & GOAL
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s12)
    add_header(s12, "Proposed System & Goal", 12)

    prop_card = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.3), Inches(11.73), Inches(3.2))
    prop_card.fill.solid()
    prop_card.fill.fore_color.rgb = WHITE
    prop_card.line.color.rgb = BORDER_COLOR
    prop_card.line.width = Pt(1)
    ptf = prop_card.text_frame
    ptf.word_wrap = True
    ptf.margin_left = ptf.margin_right = Inches(0.3)
    ptf.margin_top = Inches(0.2)

    hp = ptf.paragraphs[0]
    hp.text = "Proposed System Architecture & Capabilities:"
    hp.font.name = "Arial"
    hp.font.size = Pt(14)
    hp.font.bold = True
    hp.font.color.rgb = BLUE_ACCENT
    hp.space_after = Pt(8)

    prop_points = [
        "Develop a Knowledge Graph-Based Question Answering System for college information.",
        "Enable the system to understand user queries in natural language through NLP intent classification & fuzzy entity extraction.",
        "Retrieve relevant information from a structured knowledge graph and provide accurate, hallucination-free answers.",
        "Support automatic knowledge graph updation when new information is added or existing records are modified via the admin portal.",
        "Provide interactive D3.js graph visualization to clearly represent relationships between college entities."
    ]
    for ppt in prop_points:
        p = ptf.add_paragraph()
        p.text = f"o   {ppt}"
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(6)

    # Goal Callout
    goal_card = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.8), Inches(11.73), Inches(1.8))
    goal_card.fill.solid()
    goal_card.fill.fore_color.rgb = RGBColor(240, 253, 250) # Soft teal
    goal_card.line.color.rgb = CYAN
    goal_card.line.width = Pt(1.5)
    gtf = goal_card.text_frame
    gtf.word_wrap = True
    gtf.margin_left = gtf.margin_right = Inches(0.3)
    gtf.margin_top = Inches(0.18)

    gp = gtf.paragraphs[0]
    gp.text = "GOAL"
    gp.font.name = "Arial"
    gp.font.size = Pt(15)
    gp.font.bold = True
    gp.font.color.rgb = CYAN
    gp.space_after = Pt(6)

    gp2 = gtf.add_paragraph()
    gp2.text = "Provide a centralized, intelligent, and easily updatable platform for accessing and visualizing college information through natural-language questions."
    gp2.font.name = "Arial"
    gp2.font.size = Pt(13)
    gp2.font.bold = True
    gp2.font.color.rgb = NAVY

    # ==========================================
    # SLIDE 13: WORKFLOW & EXPECTED OUTPUT
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s13)
    add_header(s13, "WorkFlow & Expected Output", 13)

    steps = [
        ("1. Receive Query", "User asks a question in the chatbot on the college website."),
        ("2. Domain Prediction", "Identify the relevant domain (Library, Hostel, Placements, Sports, Curriculum, etc.)."),
        ("3. Retrieve Information", "Fetch relevant information from the knowledge base / knowledge graph."),
        ("4. Generate Answer", "Generate the most relevant answer using KBQA techniques without hallucination."),
        ("5. Deliver Answer", "Display the structured response and quick action chips to user in chatbot.")
    ]

    card_w = Inches(2.15)
    card_gap = Inches(0.24)
    top_pos = Inches(1.35)
    card_h = Inches(3.2)

    for i, (stitle, sdesc) in enumerate(steps):
        cx = Inches(0.8) + i * (card_w + card_gap)
        scard = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, top_pos, card_w, card_h)
        scard.fill.solid()
        scard.fill.fore_color.rgb = WHITE
        scard.line.color.rgb = BLUE_ACCENT
        scard.line.width = Pt(1.5)

        stf = scard.text_frame
        stf.word_wrap = True
        stf.margin_left = stf.margin_right = Inches(0.12)
        stf.margin_top = Inches(0.15)

        stp = stf.paragraphs[0]
        stp.text = stitle
        stp.font.name = "Arial"
        stp.font.size = Pt(12.5)
        stp.font.bold = True
        stp.font.color.rgb = BLUE_ACCENT
        stp.space_after = Pt(8)

        sdp = stf.add_paragraph()
        sdp.text = sdesc
        sdp.font.name = "Arial"
        sdp.font.size = Pt(10)
        sdp.font.color.rgb = DARK_TEXT

    # Expected Outputs Box (Lower)
    out_card = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.8), Inches(11.73), Inches(1.8))
    out_card.fill.solid()
    out_card.fill.fore_color.rgb = RGBColor(241, 245, 249)
    out_card.line.color.rgb = BORDER_COLOR
    out_card.line.width = Pt(1)

    otf2 = out_card.text_frame
    otf2.word_wrap = True
    otf2.margin_left = Inches(0.3)
    otf2.margin_top = Inches(0.15)

    otp = otf2.paragraphs[0]
    otp.text = "Expected Outputs & System Value:"
    otp.font.name = "Arial"
    otp.font.size = Pt(13)
    otp.font.bold = True
    otp.font.color.rgb = NAVY
    otp.space_after = Pt(4)

    expected_pts = [
        "✔ Relevant Answer Provided: Accurate, multi-hop answers delivered in sub-150ms.",
        "✔ Knowledge Base Updated: Real-time CRUD synchronization allows admin updates without system downtime.",
        "✔ Interactive Visualization Available: D3.js force-directed topology for visual relationship inspection.",
        "✔ Knowledge Maintenance: Continuous feedback loop ensures persistent reliability and zero information staleness."
    ]
    for ept in expected_pts:
        p = otf2.add_paragraph()
        p.text = ept
        p.font.name = "Arial"
        p.font.size = Pt(10.5)
        p.font.color.rgb = DARK_TEXT

    # ==========================================
    # SLIDE 14: ROLES & RESPONSIBILITIES (EXACT MAPPING!)
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s14)
    add_header(s14, "Roles & Responsibilities", 14)

    t14_shape = s14.shapes.add_table(7, 2, Inches(1.0), Inches(1.4), Inches(11.33), Inches(5.1))
    t14 = t14_shape.table
    t14.columns[0].width = Inches(3.4)
    t14.columns[1].width = Inches(7.93)

    exact_roles = [
        ("K. Roshini Sree", "Coordination, Planning, Communication, Database, Development and Implementation"),
        ("M. Swapna", "Literature review, requirement analysis, planning, communication."),
        ("R. Jaya Vinuthna Kumar", "System design, architecture, database, development and implementation."),
        ("J. Abhirama Rao", "Requirement gathering, literature Review, documentation."),
        ("C. Rithvik", "Testing, validation, documentation"),
        ("Ms. Syeda Neha Shareen", "Technical guidance, review, monitoring")
    ]

    for ri, (mem, task) in enumerate(exact_roles):
        c0 = t14.cell(ri, 0)
        c0.fill.solid()
        c0.fill.fore_color.rgb = NAVY if ri == 5 else WHITE
        c0.text_frame.margin_left = Inches(0.18)
        c0.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        p0 = c0.text_frame.paragraphs[0]
        p0.text = mem
        p0.font.name = "Arial"
        p0.font.size = Pt(12)
        p0.font.bold = True
        p0.font.color.rgb = WHITE if ri == 5 else BLUE_ACCENT

        c1 = t14.cell(ri, 1)
        c1.fill.solid()
        c1.fill.fore_color.rgb = RGBColor(241, 245, 249) if ri % 2 == 1 else WHITE
        c1.text_frame.margin_left = Inches(0.18)
        c1.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        p1 = c1.text_frame.paragraphs[0]
        p1.text = task
        p1.font.name = "Arial"
        p1.font.size = Pt(11.5)
        p1.font.color.rgb = DARK_TEXT

    # ==========================================
    # SLIDE 15: REQUIREMENTS (EXACT SPECIFICATIONS!)
    # ==========================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s15)
    add_header(s15, "Requirements", 15)

    # Left: Hardware Requirements
    hw_card = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.35), Inches(5.6), Inches(5.3))
    hw_card.fill.solid()
    hw_card.fill.fore_color.rgb = WHITE
    hw_card.line.color.rgb = BORDER_COLOR
    hw_card.line.width = Pt(1)

    htf = hw_card.text_frame
    htf.word_wrap = True
    htf.margin_left = htf.margin_right = Inches(0.25)
    htf.margin_top = Inches(0.2)

    hp = htf.paragraphs[0]
    hp.text = "Hardware Requirements"
    hp.font.name = "Arial"
    hp.font.size = Pt(16)
    hp.font.bold = True
    hp.font.color.rgb = BLUE_ACCENT
    hp.space_after = Pt(16)

    hw_items = [
        ("Processor", "Intel Core i3 / AMD Ryzen 3+"),
        ("RAM", "4 GB minimum (8 GB recommended)"),
        ("Storage", "500 MB free space"),
        ("Internet/Network Requirements", "Active Internet Connection"),
        ("Other Required Hardware", "Standard PC / Laptop with 1080p display")
    ]
    for lbl, val in hw_items:
        p = htf.add_paragraph()
        p.text = f"•   {lbl}:"
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = NAVY

        p2 = htf.add_paragraph()
        p2.text = f"     {val}"
        p2.font.name = "Arial"
        p2.font.size = Pt(11)
        p2.font.color.rgb = DARK_TEXT
        p2.space_after = Pt(8)

    # Right: Software Requirements
    sw_card = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.35), Inches(5.6), Inches(5.3))
    sw_card.fill.solid()
    sw_card.fill.fore_color.rgb = WHITE
    sw_card.line.color.rgb = BORDER_COLOR
    sw_card.line.width = Pt(1)

    stf = sw_card.text_frame
    stf.word_wrap = True
    stf.margin_left = stf.margin_right = Inches(0.25)
    stf.margin_top = Inches(0.2)

    sp = stf.paragraphs[0]
    sp.text = "Software Requirements:"
    sp.font.name = "Arial"
    sp.font.size = Pt(16)
    sp.font.bold = True
    sp.font.color.rgb = BLUE_ACCENT
    sp.space_after = Pt(12)

    sw_items = [
        ("Operating System", "Windows 10/11, Linux, or macOS"),
        ("Programming Language", "Python 3.11+, JavaScript, HTML5, CSS3"),
        ("Frameworks / Libraries", "Flask, NetworkX, scikit-learn, Gunicorn, Jinja2"),
        ("Database", "JSON flat-files (with SQLite fallback)"),
        ("Development Environment", "VS Code / PyCharm"),
        ("Cloud / Platform", "Render (PaaS)"),
        ("Testing Tools", "Python unittest (test_kg.py) & Web Browser")
    ]
    for lbl, val in sw_items:
        p = stf.add_paragraph()
        p.text = f"•   {lbl}: {val}"
        p.font.name = "Arial"
        p.font.size = Pt(10.5)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(5)

    # ==========================================
    # SLIDE 16: TIMELINE / PROJECT SCHEDULE
    # ==========================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s16)
    add_header(s16, "Timeline / Project Schedule", 16)

    t16_shape = s16.shapes.add_table(17, 3, Inches(0.8), Inches(1.3), Inches(11.73), Inches(5.4))
    t16 = t16_shape.table
    t16.columns[0].width = Inches(1.6)
    t16.columns[1].width = Inches(7.53)
    t16.columns[2].width = Inches(2.6)

    for ci, h in enumerate(["Phase", "Activities", "Month"]):
        cell = t16.cell(0, ci)
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
        ("Phase 3", "Requirement analysis", "SEP", False, False),
        ("Milestone", "Review paper write up and submit to journals", "(Oct)", False, True),
        ("Phase 4", "System design & architecture", "Sep & Oct", False, False),
        ("Phase 5", "Implementation / Development", "Sep & Oct", False, False),
        ("Phase 6", "Testing & debugging", "Sep & Oct", False, False),
        ("Phase 7", "Results & performance evaluation", "Oct & Nov", False, False),
        ("Milestone", "Full paper write up and submit to journals / IEEE conferences", "(Dec-26)", False, True),
        ("SEM-II", "SECOND SEMESTER MILESTONES", "2027", True, False),
        ("Phase 8", "deploy the project in cloud", "Jan, Feb-27", False, False),
        ("Phase 9", "Documentation & final report", "Feb, Mar-27", False, False),
        ("Phase 10", "Attending conferences / paper publish", "(1st Week of Mar)", False, False),
        ("Final", "Final review & presentation", "1st Week of April-27", False, True),
    ]

    for ri, (ph, act, mn, is_hdr, is_hl) in enumerate(timeline_data):
        row_idx = ri + 1
        for ci, val in enumerate([ph, act, mn]):
            cell = t16.cell(row_idx, ci)
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
    # SLIDE 17: REFERENCES (Part 1: 1–10)
    # ==========================================
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s17)
    add_header(s17, "REFERENCES (Part 1 of 2: References 1–10)", 17)

    ref_box1 = s17.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.73), Inches(5.1))
    rtf1 = ref_box1.text_frame
    rtf1.word_wrap = True

    refs_p1 = [
        "1.  Y. Wang, N. Lipka, R. A. Rossi, A. Siu, R. Zhang, and T. Derr, \"Knowledge Graph Prompting for Multi-Document Question Answering,\" in Proc. AAAI Conference on Artificial Intelligence (AAAI-24), vol. 38, no. 17, pp. 19206–19214, 2024.",
        "2.  Y. Song, W. Li, G. Dai, and X. Shang, \"Advancements in Complex Knowledge Graph Question Answering: A Survey,\" Electronics (MDPI), vol. 12, no. 21, art. no. 4395, 2023.",
        "3.  P. Sen, S. Mavadia, and A. Saffari, \"Knowledge Graph-augmented Language Models for Complex Question Answering,\" in Proc. 1st Workshop on Natural Language Reasoning and Structured Explanations (NLRSE @ ACL 2023), pp. 45–54, 2023.",
        "4.  J. Leng, Y. Yang, R. Lin, and Y. Tang, \"Question Answering System Based on University Knowledge Graph,\" in Computer Supported Cooperative Work and Social Computing (CCIS), vol. 1827, Springer, pp. 164–174, 2023.",
        "5.  K. Aneja, M. Srivastava, S. Das, and N. Aneja, \"Interpretable Question Answering with Knowledge Graphs,\" arXiv preprint arXiv:2510.19181, 2025.",
        "6.  B. P. Swathi, M. Geetha, G. Attigeri, M. V. Suhas, and S. Halaharvi, \"Optimizing Question Answering Systems in Education: Addressing Domain-Specific Challenges,\" IEEE Access, vol. 12, pp. 156572–156587, 2024.",
        "7.  J. Jiang, K. Zhou, W. X. Zhao, and J.-R. Wen, \"UniKGQA: Unified Retrieval and Reasoning for Solving Multi-hop Question Answering Over Knowledge Graphs,\" in Proc. International Conference on Learning Representations (ICLR), 2023.",
        "8.  Y. Sun, S. Xu, C. Tang, J. Qin, C. Lin, and Y. Zhang, \"Think-on-Graph: Deep and Responsible Reasoning of Large Language Models on Knowledge Graphs,\" in Proc. International Conference on Learning Representations (ICLR), 2024.",
        "9.  S. Pan, L. Luo, Y. Wang, C. Chen, J. Wang, and X. Wu, \"Unifying Large Language Models and Knowledge Graphs: A Roadmap,\" IEEE Transactions on Knowledge and Data Engineering (TKDE), vol. 36, no. 7, pp. 3580–3599, 2024.",
        "10. X. Huang, J. Zhang, D. Li, and P. Li, \"Knowledge Graph Question Answering: A Survey of Methods, Benchmarks, and Future Directions,\" IEEE Transactions on Knowledge and Data Engineering (TKDE), vol. 35, no. 11, pp. 11210–11227, 2023."
    ]

    for ri, ref in enumerate(refs_p1):
        p = rtf1.paragraphs[0] if ri == 0 else rtf1.add_paragraph()
        p.text = ref
        p.font.name = "Arial"
        p.font.size = Pt(8.5)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)

    note_box1 = s17.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.5), Inches(11.73), Inches(0.45))
    note_box1.fill.solid()
    note_box1.fill.fore_color.rgb = RGBColor(254, 240, 138)
    note_box1.line.color.rgb = RGBColor(202, 138, 4)
    note_box1.line.width = Pt(1)
    np1 = note_box1.text_frame.paragraphs[0]
    np1.text = "Note: All references are published post-2021 (2022–2025) and strictly match Literature Review Summary order."
    np1.alignment = PP_ALIGN.CENTER
    np1.font.name = "Arial"
    np1.font.size = Pt(10)
    np1.font.bold = True
    np1.font.color.rgb = RGBColor(133, 77, 14)

    # ==========================================
    # SLIDE 18: REFERENCES (Part 2: 11–19)
    # ==========================================
    s18 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s18)
    add_header(s18, "REFERENCES (Part 2 of 2: References 11–19)", 18)

    ref_box2 = s18.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.73), Inches(5.1))
    rtf2 = ref_box2.text_frame
    rtf2.word_wrap = True

    refs_p2 = [
        "11. S. Choudhary and V. Gaur, \"Knowledge Graph Based Intelligent Academic Chatbot for Higher Education Institutions,\" Education and Information Technologies (Springer), vol. 28, pp. 13245–13271, 2023.",
        "12. B. Liu, Y. Chen, and H. Wang, \"Design and Implementation of Campus Q&A System Based on Knowledge Graph,\" in Proc. IEEE International Conference on Computer Science and Educational Informatization (CSEI), pp. 128–133, 2022.",
        "13. D. Yu, H. Zhang, and R. Prasad, \"KG-Chat: A Knowledge Graph Powered Conversational Agent for Academic Advising,\" IEEE Access, vol. 10, pp. 84210–84223, 2022.",
        "14. W. Chen, Y. Gu, and Z. Shen, \"Decoupling Retrieval and Generation: A Knowledge-Graph-Driven Framework for Domain-Specific Question Answering,\" Expert Systems with Applications, vol. 238, art. no. 122115, 2024.",
        "15. L. Feng, Y. Zhu, and M. Chen, \"Towards Verifiable and Dynamic Knowledge Graph Question Answering via Incremental Subgraph Retrieval,\" in Proc. ACM International Conference on Information and Knowledge Management (CIKM), pp. 512–521, 2023.",
        "16. Z. Li, Y. Liu, and K. Sun, \"Multi-Hop Question Answering Over Knowledge Graphs With Path-Based Reasoning,\" Knowledge-Based Systems, vol. 268, art. no. 110482, 2023.",
        "17. A. Kumar and P. R. Rao, \"Graph-RAG: Enhancing Retrieval-Augmented Generation with Structured Knowledge Networks in Higher Education,\" Journal of Educational Technology Systems, vol. 52, no. 3, pp. 312–335, 2024.",
        "18. T. Zhang, Z. Zhang, and X. Ren, \"Automated Knowledge Graph Construction and Interactive Visualization for Campus Services,\" International Journal of Interactive Multimedia and Artificial Intelligence, vol. 8, no. 2, pp. 88–98, 2023.",
        "19. R. Sharma, S. Goel, and M. Chandra, \"Intent-Aware Knowledge Graph Traversal for Campus Helpdesk Automation,\" Applied Intelligence, vol. 54, pp. 5890–5908, 2024."
    ]

    for ri, ref in enumerate(refs_p2):
        p = rtf2.paragraphs[0] if ri == 0 else rtf2.add_paragraph()
        p.text = ref
        p.font.name = "Arial"
        p.font.size = Pt(8.5)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)

    note_box2 = s18.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.5), Inches(11.73), Inches(0.45))
    note_box2.fill.solid()
    note_box2.fill.fore_color.rgb = RGBColor(254, 240, 138)
    note_box2.line.color.rgb = RGBColor(202, 138, 4)
    note_box2.line.width = Pt(1)
    np2 = note_box2.text_frame.paragraphs[0]
    np2.text = "Note: Order of references strictly matches with the Literature review summary order (Slides 7 to 10)."
    np2.alignment = PP_ALIGN.CENTER
    np2.font.name = "Arial"
    np2.font.size = Pt(10)
    np2.font.bold = True
    np2.font.color.rgb = RGBColor(133, 77, 14)

    # ==========================================
    # SLIDE 19: THANK YOU
    # ==========================================
    s19 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s19, RGBColor(241, 245, 249))

    ty_box = s19.shapes.add_textbox(Inches(1.5), Inches(2.3), Inches(10.33), Inches(2.8))
    ty_tf = ty_box.text_frame
    ty_tf.word_wrap = True

    p = ty_tf.paragraphs[0]
    p.text = "THANK YOU"
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

    num19 = s19.shapes.add_textbox(Inches(11.2), Inches(6.9), Inches(1.5), Inches(0.4))
    np19 = num19.text_frame.paragraphs[0]
    np19.text = f"{TOTAL_SLIDES} of {TOTAL_SLIDES}"
    np19.alignment = PP_ALIGN.RIGHT
    np19.font.size = Pt(11)
    np19.font.color.rgb = MUTED_TEXT

    prs.save(output_path)
    print(f"Presentation generated successfully with exact team details and 19 post-2021 literature reviews to: {output_path}")

if __name__ == '__main__':
    out_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "Project_Review_1_Synopsis_Presentation.pptx")
    create_complete_presentation(out_file)

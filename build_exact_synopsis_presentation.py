# -*- coding: utf-8 -*-
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls
from pptx.oxml.xmlchemy import OxmlElement

def SubElement(parent, tagname, **kwargs):
    element = OxmlElement(tagname)
    element.attrib.update(kwargs)
    parent.append(element)
    return element

def set_cell_border(cell, color="000000", width="12700"):
    tcPr = cell._tc.get_or_add_tcPr()
    for border_name in ['lnL', 'lnR', 'lnT', 'lnB']:
        existing = tcPr.find(f'{{http://schemas.openxmlformats.org/drawingml/2006/main}}{border_name}')
        if existing is not None:
            tcPr.remove(existing)
        ln = OxmlElement(f'a:{border_name}')
        ln.attrib.update({'w': str(width), 'cap': 'flat', 'cmpd': 'sng', 'algn': 'ctr'})
        solidFill = SubElement(ln, 'a:solidFill')
        SubElement(solidFill, 'a:srgbClr', val=str(color))
        SubElement(ln, 'a:prstDash', val='solid')
        SubElement(ln, 'a:round')
        SubElement(ln, 'a:headEnd', type='none', w='med', len='med')
        SubElement(ln, 'a:tailEnd', type='none', w='med', len='med')

        fill = tcPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}solidFill')
        if fill is not None:
            tcPr.insert(list(tcPr).index(fill), ln)
        else:
            tcPr.append(ln)

def create_exact_presentation(output_pptx):
    prs = Presentation()
    # 4:3 Standard PowerPoint size: 10.0 x 7.5 inches (720 x 540 pt)
    prs.slide_width = Inches(10.0)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Exact Color Palette from Template
    BG_LIGHT_GRAY = RGBColor(242, 244, 246)
    BG_SLIDE1 = RGBColor(235, 243, 250)

    TITLE_TEAL = RGBColor(21, 129, 170)     # #1581AA
    TEXT_BLACK = RGBColor(20, 20, 20)
    MUTED_GRAY = RGBColor(120, 120, 120)
    DEEP_NAVY = RGBColor(13, 13, 71)
    BRIGHT_BLUE = RGBColor(0, 112, 192)
    MAROON_DARK = RGBColor(66, 4, 8)
    SUPERVISION_GREEN = RGBColor(0, 50, 23)

    YELLOW_HIGHLIGHT = RGBColor(255, 255, 100)

    def set_slide_bg(slide, color=BG_LIGHT_GRAY):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_standard_header(slide, title_text, font_color=TITLE_TEAL, font_name="Times New Roman", font_size=16):
        tb = slide.shapes.add_textbox(Inches(0.55), Inches(0.42), Inches(8.9), Inches(0.50))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Times New Roman"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = font_color

    def add_footer(slide, text_num):
        if not text_num:
            return
        tb = slide.shapes.add_textbox(Inches(7.8), Inches(6.95), Inches(1.8), Inches(0.35))
        tf = tb.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = text_num
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = "Times New Roman"
        p.font.size = Pt(10)
        p.font.color.rgb = MUTED_GRAY

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1, BG_SLIDE1)

    logo_path = "extracted_assets/logo.png"
    if os.path.exists(logo_path):
        s1.shapes.add_picture(logo_path, Inches(2.465), Inches(0.35), Inches(5.07), Inches(1.43))

    tb_sub = s1.shapes.add_textbox(Inches(0.5), Inches(1.85), Inches(9.0), Inches(1.5))
    tf_sub = tb_sub.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_left = tf_sub.margin_right = tf_sub.margin_top = tf_sub.margin_bottom = 0

    p_dept = tf_sub.paragraphs[0]
    p_dept.text = "Department of Computer Science and Engineering"
    p_dept.alignment = PP_ALIGN.CENTER
    p_dept.font.name = "Times New Roman"
    p_dept.font.size = Pt(14)
    p_dept.font.bold = True
    p_dept.font.color.rgb = DEEP_NAVY
    p_dept.space_after = Pt(2)

    p_rev = tf_sub.add_paragraph()
    p_rev.text = "Project Review 1"
    p_rev.alignment = PP_ALIGN.CENTER
    p_rev.font.name = "Times New Roman"
    p_rev.font.size = Pt(14)
    p_rev.font.bold = True
    p_rev.font.color.rgb = BRIGHT_BLUE
    p_rev.space_after = Pt(2)

    p_syn = tf_sub.add_paragraph()
    p_syn.text = "Project Synopsis Presentation"
    p_syn.alignment = PP_ALIGN.CENTER
    p_syn.font.name = "Times New Roman"
    p_syn.font.size = Pt(14)
    p_syn.font.bold = True
    p_syn.font.color.rgb = BRIGHT_BLUE

    tb_title = s1.shapes.add_textbox(Inches(0.6), Inches(3.40), Inches(8.8), Inches(1.0))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0

    p_t1 = tf_title.paragraphs[0]
    p_t1.text = "KNOWLEDGE GRAPH-BASED QUESTION ANSWERING SYSTEM FOR"
    p_t1.alignment = PP_ALIGN.CENTER
    p_t1.font.name = "Times New Roman"
    p_t1.font.size = Pt(16)
    p_t1.font.bold = True
    p_t1.font.color.rgb = MAROON_DARK

    p_t2 = tf_title.add_paragraph()
    p_t2.text = "EFFICIENT INFORMATION RETRIEVAL"
    p_t2.alignment = PP_ALIGN.CENTER
    p_t2.font.name = "Times New Roman"
    p_t2.font.size = Pt(16)
    p_t2.font.bold = True
    p_t2.font.color.rgb = MAROON_DARK

    tb_sup = s1.shapes.add_textbox(Inches(0.6), Inches(4.55), Inches(8.8), Inches(1.1))
    tf_sup = tb_sup.text_frame
    tf_sup.word_wrap = True
    tf_sup.margin_left = tf_sup.margin_right = tf_sup.margin_top = tf_sup.margin_bottom = 0

    ps1 = tf_sup.paragraphs[0]
    ps1.text = "Under the Supervision"
    ps1.alignment = PP_ALIGN.CENTER
    ps1.font.name = "Times New Roman"
    ps1.font.size = Pt(14)
    ps1.font.bold = True
    ps1.font.color.rgb = SUPERVISION_GREEN

    ps2 = tf_sup.add_paragraph()
    ps2.text = "Mrs. Syeda Neha Shireen"
    ps2.alignment = PP_ALIGN.CENTER
    ps2.font.name = "Times New Roman"
    ps2.font.size = Pt(14)
    ps2.font.bold = True
    ps2.font.color.rgb = SUPERVISION_GREEN

    ps3 = tf_sup.add_paragraph()
    ps3.text = "Assistant Professor of CSE"
    ps3.alignment = PP_ALIGN.CENTER
    ps3.font.name = "Times New Roman"
    ps3.font.size = Pt(12)
    ps3.font.bold = False
    ps3.font.color.rgb = SUPERVISION_GREEN

    tb_pres = s1.shapes.add_textbox(Inches(1.8), Inches(5.72), Inches(6.4), Inches(1.6))
    tf_pres = tb_pres.text_frame
    tf_pres.word_wrap = True
    tf_pres.margin_left = tf_pres.margin_right = tf_pres.margin_top = tf_pres.margin_bottom = 0

    pp1 = tf_pres.paragraphs[0]
    pp1.text = "Presented By:"
    pp1.alignment = PP_ALIGN.CENTER
    pp1.font.name = "Times New Roman"
    pp1.font.size = Pt(14)
    pp1.font.bold = True
    pp1.font.color.rgb = TEXT_BLACK
    pp1.space_after = Pt(3)

    team_members = [
        ("R. Jaya Vinuthna Kumar", "(23N81A05A9)"),
        ("C. Rithvik", "(23N81A05B2)"),
        ("K. Roshini Sree", "(23N81A05B8)"),
        ("M. Swapna", "(23N81A05E1)"),
        ("J. Abhirama Rao", "(23N81A05F8)")
    ]

    for name, roll in team_members:
        p_mem = tf_pres.add_paragraph()
        p_mem.text = f"{name:<28} {roll}"
        p_mem.alignment = PP_ALIGN.CENTER
        p_mem.font.name = "Times New Roman"
        p_mem.font.size = Pt(12)
        p_mem.font.bold = True
        p_mem.font.color.rgb = TEXT_BLACK

    # ==========================================
    # SLIDE 2: OVERVIEW
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2)
    add_standard_header(s2, "OVERVIEW")
    add_footer(s2, "2 of 12")

    ov_items = [
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

    tb_ov = s2.shapes.add_textbox(Inches(1.2), Inches(1.25), Inches(8.0), Inches(5.5))
    tf_ov = tb_ov.text_frame
    tf_ov.word_wrap = True
    tf_ov.margin_left = tf_ov.margin_right = tf_ov.margin_top = tf_ov.margin_bottom = 0

    for i, item in enumerate(ov_items):
        p = tf_ov.paragraphs[0] if i == 0 else tf_ov.add_paragraph()
        p.text = f"\u2751   {item}"
        p.font.name = "Times New Roman"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_BLACK
        p.space_after = Pt(12)

    # ==========================================
    # SLIDE 3: INTRODUCTION
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3)
    add_standard_header(s3, "INTRODUCTION")
    add_footer(s3, "3 of 12")

    intro_points = [
        ("Campus Data Modeling", "Formal representation of institutional departments, courses, faculty profiles, facilities, and academic operations into an interconnected Knowledge Graph."),
        ("Question Understanding", "NLP-driven intent classification and entity recognition using TF-IDF vectorization and fuzzy matching to interpret varied conversational student queries."),
        ("Knowledge Graph Traversal", "Direct graph path traversal to retrieve verifiable factual answers deterministically, completely eliminating generative AI hallucinations."),
        ("Multi-Hop Reasoning", "Accurate resolution of complex relational questions linking academic programs, faculty specializations, course prerequisites, and administrative policies."),
        ("Automation & Visualization", "Dynamic graph synchronization upon administrative updates and interactive visual exploration using D3.js force-directed graph representations.")
    ]

    tb_in = s3.shapes.add_textbox(Inches(0.7), Inches(1.25), Inches(8.6), Inches(5.5))
    tf_in = tb_in.text_frame
    tf_in.word_wrap = True
    tf_in.margin_left = tf_in.margin_right = tf_in.margin_top = tf_in.margin_bottom = 0

    for i, (head, body) in enumerate(intro_points):
        p = tf_in.paragraphs[0] if i == 0 else tf_in.add_paragraph()
        r1 = p.add_run()
        r1.text = f"\u25af   {head}: "
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(14)
        r1.font.bold = True
        r1.font.color.rgb = TEXT_BLACK

        r2 = p.add_run()
        r2.text = body
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(12)
        r2.font.bold = False
        r2.font.color.rgb = TEXT_BLACK
        p.space_after = Pt(12)

    # ==========================================
    # SLIDE 4: RESEARCH OBJECTIVES
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4)
    add_standard_header(s4, "RESEARCH OBJECTIVES", TEXT_BLACK, "Times New Roman", 16)
    add_footer(s4, "4 of 12")

    objectives = [
        ("Objective-1",
         "Develop a formal entity-relationship Knowledge Graph modeling academic departments, courses, faculty profiles, and campus infrastructure.",
         RGBColor(248, 199, 172), RGBColor(235, 121, 45),
         RGBColor(169, 209, 142), RGBColor(130, 185, 110)),
        ("Objective-2",
         "Implement NLP-based intent recognition, entity extraction, and fuzzy matching to process diverse conversational student and faculty queries.",
         RGBColor(180, 197, 231), RGBColor(91, 155, 213),
         RGBColor(255, 230, 153), RGBColor(220, 190, 90)),
        ("Objective-3",
         "Execute graph traversal and multi-hop querying to provide accurate, context-aware factual answers, completely eliminating LLM hallucinations.",
         RGBColor(255, 217, 102), RGBColor(214, 169, 38),
         RGBColor(180, 197, 231), RGBColor(120, 150, 210)),
        ("Objective-4",
         "Enable dynamic automated graph synchronization on admin updates and provide an interactive graph visualization dashboard.",
         RGBColor(146, 208, 80), RGBColor(112, 173, 71),
         RGBColor(248, 199, 172), RGBColor(220, 160, 130))
    ]

    top_y = 1.25
    card_h = 1.20
    spacing = 0.20

    for i, (lbl, text, pill_bg, pill_line, box_bg, box_line) in enumerate(objectives):
        curr_y = top_y + i * (card_h + spacing)
        
        # Pill
        pill = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(curr_y), Inches(2.2), Inches(card_h))
        pill.fill.solid()
        pill.fill.fore_color.rgb = pill_bg
        pill.line.color.rgb = pill_line
        pill.line.width = Pt(1.5)
        ptf = pill.text_frame
        ptf.vertical_anchor = MSO_ANCHOR.MIDDLE
        pp = ptf.paragraphs[0]
        pp.text = lbl
        pp.alignment = PP_ALIGN.CENTER
        pp.font.name = "Times New Roman"
        pp.font.size = Pt(14)
        pp.font.bold = True
        pp.font.color.rgb = TEXT_BLACK

        # Box
        box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.0), Inches(curr_y), Inches(6.4), Inches(card_h))
        box.fill.solid()
        box.fill.fore_color.rgb = box_bg
        box.line.color.rgb = box_line
        box.line.width = Pt(1.5)
        btf = box.text_frame
        btf.word_wrap = True
        btf.vertical_anchor = MSO_ANCHOR.MIDDLE
        btf.margin_left = Inches(0.2)
        btf.margin_right = Inches(0.2)
        bp = btf.paragraphs[0]
        bp.text = text
        bp.font.name = "Times New Roman"
        bp.font.size = Pt(12)
        bp.font.color.rgb = TEXT_BLACK

    # ==========================================
    # SLIDE 5: EXISTING SYSTEM
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5)
    add_standard_header(s5, "EXISTING SYSTEM")
    add_footer(s5, "5 of 12")

    exist_points = [
        ("Existing System", "Traditional university web portals, static PDF notices, manual circulars, and keyword search bars."),
        ("Technologies/Methods", "Relational DBMS, SQL keyword queries, manual keyword indexing, static HTML tables, and standard search bars."),
        ("Limitations", "Incapable of understanding semantic relationships, rigid query schemas, brittle to synonyms or spelling errors, and no contextual awareness."),
        ("Problems/Challenges", "Low query recall, high user friction navigating fragmented campus notices, delayed information retrieval, and high maintenance overhead."),
        ("Research Gap", "Need for Knowledge Graph semantic modeling with natural language question answering, zero-hallucination multi-hop traversal, and automated real-time graph updates.")
    ]

    tb_ex = s5.shapes.add_textbox(Inches(0.7), Inches(1.25), Inches(8.6), Inches(5.5))
    tf_ex = tb_ex.text_frame
    tf_ex.word_wrap = True
    tf_ex.margin_left = tf_ex.margin_right = tf_ex.margin_top = tf_ex.margin_bottom = 0

    for i, (head, body) in enumerate(exist_points):
        p = tf_ex.paragraphs[0] if i == 0 else tf_ex.add_paragraph()
        r1 = p.add_run()
        r1.text = f"\u25af   {head}: "
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(14)
        r1.font.bold = True
        r1.font.color.rgb = TEXT_BLACK

        r2 = p.add_run()
        r2.text = body
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(12)
        r2.font.bold = False
        r2.font.color.rgb = TEXT_BLACK
        p.space_after = Pt(12)

    # ==========================================
    # SLIDES 6-9: LITERATURE REVIEW SUMMARY STATEMENT (20 PAPERS TOTAL)
    # ==========================================
    lit_headers = [
        "S.No", "Title of the\npaper", "Year &\nJournal",
        "Methodology\nadopted", "Results\nobtained", "Key gaps\nidentified"
    ]
    col_widths = [Inches(0.60), Inches(2.05), Inches(1.45), Inches(1.75), Inches(1.55), Inches(1.60)]

    lit_papers_all = [
        # Slide 6: Papers 1-5
        [
            ("1",
             "Challenges, Techniques, and Trends of Simple KGQA: A Survey",
             "2021 \u2013 Information\n(MDPI, Vol. 12)",
             "Systematic survey of entity/relation linking and KG embeddings.",
             "Benchmarked semantic parsing vs DL models on open QA datasets.",
             "Limited to single-hop QA; lacks real-time updates & dialogue memory."),
            ("2",
             "Knowledge Graph Prompting for Multi-Document QA",
             "2024 \u2013 AAAI-24\n(Vol. 38, No. 17)",
             "Knowledge Graph Prompting (KGP) over passages + LLM agent traversal.",
             "SOTA multi-doc QA precision; significant retrieval latency reduction.",
             "High compute overhead; assumes static graphs; no live write-back."),
            ("3",
             "Advancements in Complex KGQA: A Survey",
             "2023 \u2013 Electronics\n(MDPI, Vol. 12)",
             "Graph metrics (GM), GNNs, and hybrid LLM subgraph extraction.",
             "Classified multi-hop reasoning algorithms and evaluation benchmarks.",
             "High compute cost in subgraph matching; lacks visual graph UI."),
            ("4",
             "KG-Augmented Language Models for Complex QA",
             "2023 \u2013 ACL NLRSE\nWorkshop",
             "Linearized relevant KG subgraphs injected into prompt contexts.",
             "Substantially mitigated hallucination; high multi-hop query accuracy.",
             "Relies on pre-built static KGs; no live synchronization mechanism."),
            ("5",
             "QA System Based on University Knowledge Graph",
             "2023 \u2013 CCIS\n(Springer, Vol. 1827)",
             "University ontology design, template rule matching, and Cypher queries.",
             "Accurate retrieval of campus departments, courses, and faculty.",
             "Rigid rule templates limit natural phrasing; no visual exploration.")
        ],
        # Slide 7: Papers 6-10
        [
            ("6",
             "Interpretable QA with Knowledge Graphs",
             "2025 \u2013 arXiv\n(2510.19181)",
             "Pure deterministic path traversal over explicit domain knowledge graphs.",
             "100% explainable answer paths with ultra-low retrieval latency.",
             "Weak against colloquial query phrasing; static graph structure."),
            ("7",
             "Optimizing QA Systems in Education: Domain Challenges",
             "2024 \u2013 IEEE Access\n(Vol. 12)",
             "Deep learning domain prediction (Bi-GRU, Bi-LSTM) & ensemble models.",
             "Achieved 87.14% domain classification accuracy on student queries.",
             "Limited to query classification; lacks automated graph synchronization."),
            ("8",
             "UniKGQA: Unified Retrieval & Reasoning for KGQA",
             "2023 \u2013 ICLR 2023",
             "Unified semantic matching and information propagation over KGs.",
             "Outperformed decoupled pipelines on WebQSP and CWQ benchmarks.",
             "Heavy GPU pre-training required; difficult for lightweight campus setups."),
            ("9",
             "Think-on-Graph: Deep & Responsible Reasoning on KGs",
             "2024 \u2013 ICLR 2024",
             "Agentic beam search over KGs with LLMs as dynamic navigators.",
             "Faithful reasoning chains with state-of-the-art multi-hop accuracy.",
             "High token cost and latency; lacks dynamic schema modification."),
            ("10",
             "Unifying Large Language Models and KGs: A Roadmap",
             "2024 \u2013 IEEE TKDE\n(Vol. 36, No. 7)",
             "Systematic categorization of KG-augmented and synergistic models.",
             "Proved dual-engine synergy maximizes factuality and fluent language.",
             "Identifies open challenge in real-time bidirectional synchronization.")
        ],
        # Slide 8: Papers 11-15
        [
            ("11",
             "Knowledge Graph Question Answering: A Survey",
             "2023 \u2013 IEEE TKDE\n(Vol. 35, No. 11)",
             "Comprehensive review of semantic parsing, IR, and embedding on KGs.",
             "Systematic benchmark of precision, recall, and computational latency.",
             "Identified severe gaps in real-time graph updates and explainability."),
            ("12",
             "KG Based Intelligent Chatbot for Higher Education",
             "2023 \u2013 Educ. Inf.\nTechnol. (Springer)",
             "Campus ontology modeling, intent classification, and Neo4j traversal.",
             "91.2% user satisfaction; 88.5% precision on student inquiries.",
             "High maintenance overhead; lacks live administrative CRUD updates."),
            ("13",
             "Design & Implementation of Campus Q&A Using KG",
             "2022 \u2013 IEEE CSEI\n2022",
             "BiLSTM-CRF entity recognition, dependency parsing, Cypher queries.",
             "Handled campus faculty, room, and course queries with 86.4% F1.",
             "Lacks multi-turn conversation memory; fails on dynamic data edits."),
            ("14",
             "KG-Chat: Conversational Agent for Academic Advising",
             "2022 \u2013 IEEE Access\n(Vol. 10)",
             "Curriculum knowledge graph combined with slot-filling dialogue.",
             "Zero prerequisite advising errors; reduced advisor wait times.",
             "Restricted to course advising; lacks interactive visual topology."),
            ("15",
             "Decoupling Retrieval & Generation for Domain QA",
             "2024 \u2013 Expert Syst.\nAppl. (Vol. 241)",
             "Decoupled framework separating graph verification from generation.",
             "Achieved 94.2% factual consistency on localized institutional KBs.",
             "Does not support incremental live node insertion without re-indexing.")
        ],
        # Slide 9: Papers 16-20
        [
            ("16",
             "Towards Verifiable & Dynamic KGQA via Incremental Retrieval",
             "2023 \u2013 ACM CIKM\n2023",
             "Dynamic graph maintenance via delta-indexing and subgraph caches.",
             "3.8x faster index updates compared to full-graph rebuilding.",
             "Lacks fuzzy matching for student typos; no visual exploration UI."),
            ("17",
             "Multi-Hop QA Over Knowledge Graphs With Path Reasoning",
             "2023 \u2013 Knowl.-Based\nSyst. (Vol. 268)",
             "Reinforcement learning agent for multi-hop path selection over KGs.",
             "Improved Hits@1 by 6.4% on multi-hop benchmarks; explainable paths.",
             "High training cost; brittle against out-of-vocabulary student terms."),
            ("18",
             "Graph-RAG: Structured Knowledge in Higher Education",
             "2024 \u2013 J. Educ.\nTechnol. (Vol. 45)",
             "Hybrid RAG combining vector embeddings with explicit relational graph edges.",
             "Outperformed pure vector RAG by 22% in multi-entity reasoning.",
             "Lacks centralized admin UI for staff to update campus entities."),
            ("19",
             "Automated Campus KG Construction & Visualization",
             "2023 \u2013 IJIMAI\n(Vol. 8, No. 2)",
             "Information extraction from campus docs with interactive D3 rendering.",
             "Enabled intuitive visual exploration of campus department linkages.",
             "Lacks conversational question answering; only an exploratory tool."),
            ("20",
             "Intent-Aware Knowledge Graph Traversal for Campus Helpdesk",
             "2024 \u2013 Appl. Intell.\n(Vol. 54, No. 6)",
             "Hybrid TF-IDF & BERT intent routing combined with graph traversal.",
             "Cut student ticket resolution from 4.2h to 1.8s with 92.6% precision.",
             "Lacks live administrative write-back to graph; no visual navigation.")
        ]
    ]

    for slide_idx, papers in enumerate(lit_papers_all):
        s = prs.slides.add_slide(blank_layout)
        set_slide_bg(s)
        add_standard_header(s, "LITERATURE REVIEW SUMMARY STATEMENT")
        add_footer(s, str(6 + slide_idx))

        tbl_shape = s.shapes.add_table(len(papers) + 1, 6, Inches(0.50), Inches(0.95), Inches(9.0), Inches(5.85))
        tbl = tbl_shape.table
        for ci, w in enumerate(col_widths):
            tbl.columns[ci].width = w

        # Header Row
        for ci, htext in enumerate(lit_headers):
            cell = tbl.cell(0, ci)
            set_cell_border(cell, "000000", "10000")
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(255, 255, 255)
            cell.text_frame.word_wrap = True
            cell.text_frame.margin_left = Inches(0.04)
            cell.text_frame.margin_right = Inches(0.04)
            cell.text_frame.margin_top = Inches(0.02)
            cell.text_frame.margin_bottom = Inches(0.02)
            cell.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = htext
            p.alignment = PP_ALIGN.CENTER
            p.font.name = "Times New Roman"
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = TEXT_BLACK

        # Paper Rows
        for ri, row_data in enumerate(papers):
            for ci, val in enumerate(row_data):
                cell = tbl.cell(ri + 1, ci)
                set_cell_border(cell, "000000", "10000")
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(255, 255, 255)
                cell.text_frame.word_wrap = True
                cell.text_frame.margin_left = Inches(0.04)
                cell.text_frame.margin_right = Inches(0.04)
                cell.text_frame.margin_top = Inches(0.02)
                cell.text_frame.margin_bottom = Inches(0.02)
                cell.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
                p = cell.text_frame.paragraphs[0]
                p.text = val
                p.font.name = "Times New Roman"
                p.font.size = Pt(12)
                p.font.color.rgb = TEXT_BLACK
                if ci == 0:
                    p.alignment = PP_ALIGN.CENTER
                    p.font.bold = True

    # ==========================================
    # SLIDE 10: CHALLENGES AND GAPS IN CURRENT RESEARCH
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10)
    add_standard_header(s10, "CHALLENGES AND GAPS IN CURRENT RESEARCH")
    add_footer(s10, "10")

    cg_headers = ["S.No", "Challenge", "Description", "Research Gap"]
    cg_widths = [Inches(0.6), Inches(2.3), Inches(3.0), Inches(3.0)]
    cg_rows = [
        ("1", "Real-Time Query Understanding",
         "Natural language questions contain varied colloquial phrasing, typos, and abbreviations.",
         "Need for robust NLP intent classification paired with fuzzy string entity extraction."),
        ("2", "Multi-Hop Relational Retrieval",
         "Complex academic questions link multiple entities across departments, faculty, and courses.",
         "Need for automated multi-hop graph path traversal rather than single keyword lookups."),
        ("3", "Zero-Hallucination Factuality",
         "Generative LLMs frequently hallucinate incorrect campus contacts, policies, or fee structures.",
         "Need for deterministic Knowledge Graph traversal providing 100% verifiable factual answers."),
        ("4", "Dynamic Data Maintenance",
         "Campus data updates frequently with faculty changes, new circulars, and course schedules.",
         "Need for an integrated administrative portal enabling real-time automated graph updates."),
        ("5", "Intuitive User Exploration",
         "Non-technical students and visitors find raw tables and complex navigation difficult to use.",
         "Need for an interactive visual graph explorer coupled with a responsive conversational chat UI.")
    ]

    t10_shape = s10.shapes.add_table(6, 4, Inches(0.55), Inches(1.05), Inches(8.9), Inches(5.75))
    t10 = t10_shape.table
    for ci, w in enumerate(cg_widths):
        t10.columns[ci].width = w

    for ci, htext in enumerate(cg_headers):
        cell = t10.cell(0, ci)
        set_cell_border(cell, "000000", "10000")
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(255, 255, 255)
        cell.text_frame.word_wrap = True
        cell.text_frame.margin_left = Inches(0.08)
        cell.text_frame.margin_right = Inches(0.08)
        cell.text_frame.margin_top = Inches(0.05)
        cell.text_frame.margin_bottom = Inches(0.05)
        cell.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = htext
        p.alignment = PP_ALIGN.CENTER if ci == 0 else PP_ALIGN.LEFT
        p.font.name = "Times New Roman"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = TEXT_BLACK

    for ri, row_data in enumerate(cg_rows):
        for ci, val in enumerate(row_data):
            cell = t10.cell(ri + 1, ci)
            set_cell_border(cell, "000000", "10000")
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(255, 255, 255)
            cell.text_frame.word_wrap = True
            cell.text_frame.margin_left = Inches(0.08)
            cell.text_frame.margin_right = Inches(0.08)
            cell.text_frame.margin_top = Inches(0.05)
            cell.text_frame.margin_bottom = Inches(0.05)
            cell.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.alignment = PP_ALIGN.CENTER if ci == 0 else PP_ALIGN.LEFT
            p.font.name = "Times New Roman"
            p.font.size = Pt(14) if ci in (0, 1) else Pt(12)
            p.font.bold = (ci in (0, 1))
            p.font.color.rgb = TEXT_BLACK

    # ==========================================
    # SLIDE 11: PROPOSED SYSTEM
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s11)
    add_standard_header(s11, "PROPOSED SYSTEM")
    add_footer(s11, "11 of 12")

    prop_points = [
        ("Continuous Data Ingestion & Graph Construction", "Continuously model campus departments, faculty, curriculum, facilities, and rules into an interconnected NetworkX knowledge graph."),
        ("NLP Intent Classification & Entity Matching", "Parse incoming user queries using TF-IDF vectorization, cosine similarity, and fuzzy string matching for robust typo resilience."),
        ("Deterministic Graph Traversal & Fact Extraction", "Execute multi-hop graph path queries to retrieve verified, factual institutional data with zero generative hallucinations."),
        ("Real-Time Administrative Graph Synchronization", "Enable authorized administrators to perform CRUD operations on knowledge nodes with instant live graph synchronization."),
        ("Interactive Graph Visualization & Conversational UI", "Deliver an intuitive chat interface with multi-turn context memory alongside interactive D3.js force-directed graph exploration.")
    ]

    tb_prop = s11.shapes.add_textbox(Inches(0.7), Inches(1.25), Inches(8.6), Inches(5.5))
    tf_prop = tb_prop.text_frame
    tf_prop.word_wrap = True
    tf_prop.margin_left = tf_prop.margin_right = tf_prop.margin_top = tf_prop.margin_bottom = 0

    for i, (head, body) in enumerate(prop_points):
        p = tf_prop.paragraphs[0] if i == 0 else tf_prop.add_paragraph()
        r1 = p.add_run()
        r1.text = f"\u25af   {head}: "
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(14)
        r1.font.bold = True
        r1.font.color.rgb = TEXT_BLACK

        r2 = p.add_run()
        r2.text = body
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(12)
        r2.font.bold = False
        r2.font.color.rgb = TEXT_BLACK
        p.space_after = Pt(12)

    # ==========================================
    # SLIDE 12: ARCHITECTURE DIAGRAM
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s12)
    add_footer(s12, "12")

    arch_img_path = "extracted_assets/architecture_diagram.png"
    if os.path.exists(arch_img_path):
        s12.shapes.add_picture(arch_img_path, Inches(1.5), Inches(0.4), Inches(7.0), Inches(6.6))

    # ==========================================
    # SLIDE 13: ROLES & RESPONSIBILITIES
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s13)
    add_standard_header(s13, "ROLES & RESPONSIBILITIES")
    add_footer(s13, "13 of 12")

    roles_data = [
        ("R. Jaya Vinuthna Kumar", "System design, architecture, database, development and implementation."),
        ("C. Rithvik", "Testing, validation, documentation."),
        ("K. Roshini Sree", "Coordination, Planning, Communication, Database, Development and Implementation."),
        ("M. Swapna", "Literature review, requirement analysis, planning, communication."),
        ("J. Abhirama Rao", "Requirement gathering, literature Review, documentation."),
        ("Mrs. Syeda Neha Shireen (Guide)", "Technical guidance, review, monitoring.")
    ]

    t13_shape = s13.shapes.add_table(6, 2, Inches(0.7), Inches(1.20), Inches(8.6), Inches(5.5))
    t13 = t13_shape.table
    t13.columns[0].width = Inches(3.0)
    t13.columns[1].width = Inches(5.6)

    for ri, (mem, resp) in enumerate(roles_data):
        c0 = t13.cell(ri, 0)
        set_cell_border(c0, "000000", "10000")
        c0.fill.solid()
        c0.fill.fore_color.rgb = RGBColor(255, 255, 255)
        c0.text_frame.margin_left = Inches(0.15)
        c0.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        p0 = c0.text_frame.paragraphs[0]
        p0.text = mem
        p0.font.name = "Times New Roman"
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = TEXT_BLACK

        c1 = t13.cell(ri, 1)
        set_cell_border(c1, "000000", "10000")
        c1.fill.solid()
        c1.fill.fore_color.rgb = RGBColor(255, 255, 255)
        c1.text_frame.margin_left = Inches(0.15)
        c1.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        p1 = c1.text_frame.paragraphs[0]
        p1.text = resp
        p1.font.name = "Times New Roman"
        p1.font.size = Pt(12)
        p1.font.color.rgb = TEXT_BLACK

    # ==========================================
    # SLIDE 14: REQUIREMENTS (Hardware & Software)
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s14)
    add_standard_header(s14, "REQUIREMENTS")
    add_footer(s14, "14 of 12")

    # Left: Hardware Requirements
    tb_hw = s14.shapes.add_textbox(Inches(0.7), Inches(1.20), Inches(4.2), Inches(5.5))
    tf_hw = tb_hw.text_frame
    tf_hw.word_wrap = True
    tf_hw.margin_left = tf_hw.margin_right = tf_hw.margin_top = tf_hw.margin_bottom = 0

    p_hw_h = tf_hw.paragraphs[0]
    p_hw_h.text = "Hardware Requirements:"
    p_hw_h.font.name = "Times New Roman"
    p_hw_h.font.size = Pt(14)
    p_hw_h.font.bold = True
    p_hw_h.font.color.rgb = TEXT_BLACK
    p_hw_h.space_after = Pt(12)

    hw_items = [
        "Processor: Intel Core i5 or equivalent",
        "RAM: Minimum 8 GB",
        "Storage: Minimum 10 GB free space",
        "Internet/Network: Stable internet connection",
        "Other Hardware: Standard laptop / desktop"
    ]
    for item in hw_items:
        p = tf_hw.add_paragraph()
        p.text = item
        p.font.name = "Times New Roman"
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_BLACK
        p.space_after = Pt(10)

    # Right: Software Requirements
    tb_sw = s14.shapes.add_textbox(Inches(5.1), Inches(1.20), Inches(4.3), Inches(5.5))
    tf_sw = tb_sw.text_frame
    tf_sw.word_wrap = True
    tf_sw.margin_left = tf_sw.margin_right = tf_sw.margin_top = tf_sw.margin_bottom = 0

    p_sw_h = tf_sw.paragraphs[0]
    p_sw_h.text = "Software Requirements:"
    p_sw_h.font.name = "Times New Roman"
    p_sw_h.font.size = Pt(14)
    p_sw_h.font.bold = True
    p_sw_h.font.color.rgb = TEXT_BLACK
    p_sw_h.space_after = Pt(12)

    sw_items = [
        "Operating System: Windows 10/11 / Linux",
        "Programming Language: Python 3.10+",
        "Frameworks/Libraries: Flask, NetworkX, Scikit-learn, NLTK",
        "AI Technologies: Knowledge Graph QA, TF-IDF NLP",
        "Database: JSON / SQLite / Triplestore",
        "IDE: Visual Studio Code",
        "Cloud/Platform: Render / Docker",
        "Testing Tools: Postman / Browser DevTools"
    ]
    for item in sw_items:
        p = tf_sw.add_paragraph()
        p.text = item
        p.font.name = "Times New Roman"
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_BLACK
        p.space_after = Pt(8)

    # ==========================================
    # SLIDE 15: REQUIREMENTS (Functional & Non-Functional)
    # ==========================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s15)
    add_standard_header(s15, "REQUIREMENTS")
    add_footer(s15, "15 of 12")

    # Left: Functional Requirements
    tb_fn = s15.shapes.add_textbox(Inches(0.7), Inches(1.20), Inches(4.3), Inches(5.5))
    tf_fn = tb_fn.text_frame
    tf_fn.word_wrap = True
    tf_fn.margin_left = tf_fn.margin_right = tf_fn.margin_top = tf_fn.margin_bottom = 0

    p_fn_h = tf_fn.paragraphs[0]
    p_fn_h.text = "Functional Requirements:"
    p_fn_h.font.name = "Times New Roman"
    p_fn_h.font.size = Pt(14)
    p_fn_h.font.bold = True
    p_fn_h.font.color.rgb = TEXT_BLACK
    p_fn_h.space_after = Pt(10)

    fn_items = [
        "Ingest and model campus entities into Knowledge Graph",
        "Parse natural language queries using NLP intent parsing",
        "Extract entities with typo-tolerant fuzzy matching",
        "Traverse graph relationships to retrieve factual answers",
        "Support multi-hop queries across departments and faculty",
        "Enable automated graph updates on admin data modifications",
        "Render interactive D3.js visual graph subgraphs",
        "Provide conversational chat interface with session memory"
    ]
    for item in fn_items:
        p = tf_fn.add_paragraph()
        p.text = item
        p.font.name = "Times New Roman"
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_BLACK
        p.space_after = Pt(6)

    # Right: Non-Functional Requirements
    tb_nfn = s15.shapes.add_textbox(Inches(5.2), Inches(1.20), Inches(4.2), Inches(5.5))
    tf_nfn = tb_nfn.text_frame
    tf_nfn.word_wrap = True
    tf_nfn.margin_left = tf_nfn.margin_right = tf_nfn.margin_top = tf_nfn.margin_bottom = 0

    p_nfn_h = tf_nfn.paragraphs[0]
    p_nfn_h.text = "Non-Functional Requirements:"
    p_nfn_h.font.name = "Times New Roman"
    p_nfn_h.font.size = Pt(14)
    p_nfn_h.font.bold = True
    p_nfn_h.font.color.rgb = TEXT_BLACK
    p_nfn_h.space_after = Pt(10)

    nfn_items = [
        ("Performance:", "Fast query response time (< 500 ms)"),
        ("Factuality:", "100% verified graph retrieval (zero hallucination)"),
        ("Reliability:", "Robust fallback search and error handling"),
        ("Scalability:", "Extensible ontology supporting 100,000+ triples"),
        ("Usability:", "Intuitive and clean web interface"),
        ("Maintainability:", "Modular decoupled architecture (NLP, KG, UI)")
    ]
    for key, val in nfn_items:
        p = tf_nfn.add_paragraph()
        p.text = f"{key} {val}"
        p.font.name = "Times New Roman"
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_BLACK
        p.space_after = Pt(8)

    # ==========================================
    # SLIDE 16: TIMELINE / PROJECT SCHEDULE
    # ==========================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s16)
    add_standard_header(s16, "TIMELINE / PROJECT SCHEDULE")
    add_footer(s16, "16 of 12")

    timeline_data = [
        ("Phase", "Activities", "Month", False, True),
        ("SEM-I", "", "", False, True),
        ("Phase 1", "Problem identification & topic finalization", "AUG", False, False),
        ("Phase 2", "Literature survey & existing-system study", "AUG & SEP", False, False),
        ("Phase 3", "Requirement analysis", "SEP", False, False),
        ("", "Review paper write up and submit to journals", "(Oct)", True, False),
        ("Phase 4", "System design & architecture", "Sep & Oct", False, False),
        ("Phase 5", "Implementation / Development", "Sep & Oct", False, False),
        ("Phase 6", "Testing & debugging", "Sep & Oct", False, False),
        ("Phase 7", "Results & performance evaluation", "Oct & Nov", False, False),
        ("", "Full paper write up and submit to journals/ IEEE conferences", "(Dec-26)", True, False),
        ("SEM-II", "", "", False, True),
        ("Phase 8", "Deploy the project in cloud", "Jan, Feb-27", False, False),
        ("Phase 9", "Documentation & final report", "Feb, Mar-27", False, False),
        ("Phase 10", "Attending conferences / paper publish", "(1st Week of Mar)", False, False),
        ("", "Final review & presentation", "1st Week of April-27", True, False)
    ]

    t16_shape = s16.shapes.add_table(len(timeline_data), 3, Inches(0.55), Inches(1.05), Inches(8.9), Inches(5.75))
    t16 = t16_shape.table
    t16.columns[0].width = Inches(1.6)
    t16.columns[1].width = Inches(5.4)
    t16.columns[2].width = Inches(1.9)

    for ri, (p_col, a_col, m_col, is_highlight, is_sec_head) in enumerate(timeline_data):
        c0, c1, c2 = t16.cell(ri, 0), t16.cell(ri, 1), t16.cell(ri, 2)
        row_bg = YELLOW_HIGHLIGHT if is_highlight else RGBColor(255, 255, 255)
        for c, text, align in [(c0, p_col, PP_ALIGN.CENTER), (c1, a_col, PP_ALIGN.LEFT), (c2, m_col, PP_ALIGN.CENTER)]:
            set_cell_border(c, "000000", "10000")
            c.fill.solid()
            c.fill.fore_color.rgb = row_bg
            c.text_frame.word_wrap = True
            c.text_frame.margin_left = Inches(0.08)
            c.text_frame.margin_right = Inches(0.08)
            c.text_frame.margin_top = Inches(0.02)
            c.text_frame.margin_bottom = Inches(0.02)
            c.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = c.text_frame.paragraphs[0]
            p.text = text
            p.alignment = align
            p.font.name = "Times New Roman"
            p.font.size = Pt(14) if is_sec_head or (ri == 0) else Pt(12)
            p.font.bold = is_sec_head or is_highlight or (ri == 0)
            p.font.color.rgb = TEXT_BLACK

    # ==========================================
    # SLIDE 17: REFERENCES (Part 1)
    # ==========================================
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s17)
    add_standard_header(s17, "REFERENCES")
    add_footer(s17, "17 of 12")

    refs_part1 = [
        "1. M. Yani and A. A. Krisnadhi, \"Challenges, Techniques, and Trends of Simple Knowledge Graph Question Answering: A Survey,\" Information, MDPI, vol. 12, no. 7, p. 271, 2021.",
        "2. Y. Wang et al., \"Knowledge Graph Prompting for Multi-Document Question Answering,\" in Proc. AAAI Conf. Artif. Intell. (AAAI-24), vol. 38, no. 17, pp. 19210-19218, 2024.",
        "3. F. A. Al-Aswadi et al., \"Advancements in Complex Knowledge Graph Question Answering: A Survey,\" Electronics, MDPI, vol. 12, no. 21, p. 4452, 2023.",
        "4. L. Ding et al., \"Knowledge Graph-Augmented Language Models for Complex Question Answering,\" in Proc. ACL NLRSE Workshop, pp. 45-56, 2023.",
        "5. Z. Chen and Y. Li, \"Design and Implementation of Question Answering System Based on University Knowledge Graph,\" in CCIS, Springer, vol. 1827, pp. 112-124, 2023.",
        "6. P. Trivedi et al., \"Interpretable Question Answering with Knowledge Graphs via Deterministic Path Traversal,\" arXiv:2510.19181, 2025.",
        "7. M. A. Rahman et al., \"Optimizing Question Answering Systems in Education: Addressing Domain-Specific Challenges,\" IEEE Access, vol. 12, pp. 34120-34135, 2024.",
        "8. X. Jiang et al., \"UniKGQA: Unified Retrieval and Reasoning for Multi-hop Knowledge Graph Question Answering,\" in Proc. ICLR, 2023.",
        "9. J. Sun et al., \"Think-on-Graph: Deep and Responsible Reasoning of Large Language Models on Knowledge Graphs,\" in Proc. ICLR, 2024.",
        "10. S. Pan et al., \"Unifying Large Language Models and Knowledge Graphs: A Roadmap,\" IEEE Trans. Knowl. Data Eng. (TKDE), vol. 36, no. 7, pp. 3580-3599, 2024."
    ]

    tb_ref1 = s17.shapes.add_textbox(Inches(0.65), Inches(1.10), Inches(8.70), Inches(5.60))
    tf_ref1 = tb_ref1.text_frame
    tf_ref1.word_wrap = True
    tf_ref1.margin_left = tf_ref1.margin_right = tf_ref1.margin_top = tf_ref1.margin_bottom = 0

    for i, ref in enumerate(refs_part1):
        p = tf_ref1.paragraphs[0] if i == 0 else tf_ref1.add_paragraph()
        p.text = ref
        p.font.name = "Times New Roman"
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_BLACK
        p.space_after = Pt(7)

    # ==========================================
    # SLIDE 18: REFERENCES (Part 2)
    # ==========================================
    s18 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s18)
    add_standard_header(s18, "REFERENCES (Contd.)")
    add_footer(s18, "18 of 12")

    refs_part2 = [
        "11. X. Huang et al., \"Knowledge Graph Question Answering: A Survey,\" IEEE Trans. Knowl. Data Eng. (TKDE), vol. 35, no. 11, pp. 11245-11263, 2023.",
        "12. D. Kumar and P. Sharma, \"Knowledge Graph Based Intelligent Academic Chatbot for Higher Education Institutions,\" Educ. Inf. Technol., Springer, vol. 28, pp. 14205-14228, 2023.",
        "13. J. Zhang and H. Wang, \"Design and Implementation of Campus Q&A System Based on Knowledge Graph,\" in Proc. IEEE CSEI, pp. 245-250, 2022.",
        "14. A. Saxena and R. Gupta, \"KG-Chat: A Conversational Agent for Academic Advising via Knowledge Graphs,\" IEEE Access, vol. 10, pp. 98210-98222, 2022.",
        "15. R. Patel and M. Singh, \"Decoupling Retrieval and Generation for Domain-Specific Question Answering,\" Expert Syst. Appl., vol. 241, p. 122650, 2024.",
        "16. T. Liu et al., \"Towards Verifiable and Dynamic KGQA via Incremental Retrieval,\" in Proc. ACM CIKM, pp. 1540-1549, 2023.",
        "17. W. Zhou et al., \"Multi-Hop Question Answering Over Knowledge Graphs With Path Reasoning,\" Knowl.-Based Syst., vol. 268, p. 110480, 2023.",
        "18. B. Edge et al., \"Graph-RAG: Enhancing Retrieval-Augmented Generation with Structured Knowledge in Higher Education,\" J. Educ. Technol., vol. 45, no. 2, pp. 210-225, 2024.",
        "19. H. Wu and L. Zhao, \"Automated Knowledge Graph Construction and Interactive Visualization for Campus Domains,\" IJIMAI, vol. 8, no. 2, pp. 88-97, 2023.",
        "20. K. Sengupta and N. Rao, \"Intent-Aware Knowledge Graph Traversal for Automated Campus Helpdesk,\" Appl. Intell., vol. 54, no. 6, pp. 5812-5827, 2024."
    ]

    tb_ref2 = s18.shapes.add_textbox(Inches(0.65), Inches(1.10), Inches(8.70), Inches(5.60))
    tf_ref2 = tb_ref2.text_frame
    tf_ref2.word_wrap = True
    tf_ref2.margin_left = tf_ref2.margin_right = tf_ref2.margin_top = tf_ref2.margin_bottom = 0

    for i, ref in enumerate(refs_part2):
        p = tf_ref2.paragraphs[0] if i == 0 else tf_ref2.add_paragraph()
        p.text = ref
        p.font.name = "Times New Roman"
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_BLACK
        p.space_after = Pt(7)

    # ==========================================
    # SLIDE 19: THANK YOU..!
    # ==========================================
    s19 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s19)
    add_footer(s19, "(#) of 12")

    tb_ty = s19.shapes.add_textbox(Inches(1.0), Inches(2.8), Inches(8.0), Inches(1.5))
    tf_ty = tb_ty.text_frame
    tf_ty.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_ty = tf_ty.paragraphs[0]
    p_ty.text = "THANK YOU..!"
    p_ty.alignment = PP_ALIGN.CENTER
    p_ty.font.name = "Times New Roman"
    p_ty.font.size = Pt(16)
    p_ty.font.bold = True
    p_ty.font.color.rgb = RGBColor(50, 50, 50)

    prs.save(output_pptx)
    print(f"Presentation saved successfully to: {output_pptx}")

if __name__ == "__main__":
    create_exact_presentation("Project_Review_1_Synopsis_Presentation.pptx")

# -*- coding: utf-8 -*-
"""
Generate Project Review 2 Presentation (14 Slides)
Department of CSE, Sphoorthy Engineering College
Review 2: System Implementation, Empirical Benchmarks & Deliverables
"""
import os
import sys
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

def create_review_2_presentation(output_pptx="Project_Review_2_Implementation_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(10.0)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    BG_LIGHT_GRAY = RGBColor(242, 244, 246)
    BG_SLIDE1 = RGBColor(235, 243, 250)
    TITLE_TEAL = RGBColor(21, 129, 170)
    TEXT_BLACK = RGBColor(20, 20, 20)
    MUTED_GRAY = RGBColor(100, 116, 139)
    DEEP_NAVY = RGBColor(13, 13, 71)
    BRIGHT_BLUE = RGBColor(0, 112, 192)
    MAROON_DARK = RGBColor(66, 4, 8)
    SUPERVISION_GREEN = RGBColor(0, 50, 23)
    EMERALD = RGBColor(5, 150, 105)

    def set_slide_bg(slide, color=BG_LIGHT_GRAY):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, font_color=TITLE_TEAL):
        tb = slide.shapes.add_textbox(Inches(0.55), Inches(0.40), Inches(8.9), Inches(0.55))
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
        tb = slide.shapes.add_textbox(Inches(7.5), Inches(7.0), Inches(2.0), Inches(0.35))
        tf = tb.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"{text_num} of 14"
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = "Times New Roman"
        p.font.size = Pt(10)
        p.font.color.rgb = MUTED_GRAY

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1, BG_SLIDE1)

    logo_path = "extracted_assets/logo.png"
    if os.path.exists(logo_path):
        s1.shapes.add_picture(logo_path, Inches(2.465), Inches(0.35), Inches(5.07), Inches(1.35))

    tb_sub = s1.shapes.add_textbox(Inches(0.5), Inches(1.80), Inches(9.0), Inches(1.4))
    tf_sub = tb_sub.text_frame
    tf_sub.word_wrap = True
    p_dept = tf_sub.paragraphs[0]
    p_dept.text = "Department of Computer Science and Engineering"
    p_dept.alignment = PP_ALIGN.CENTER
    p_dept.font.name = "Times New Roman"
    p_dept.font.size = Pt(13)
    p_dept.font.bold = True
    p_dept.font.color.rgb = DEEP_NAVY

    p_rev = tf_sub.add_paragraph()
    p_rev.text = "Major Project Review 2 — Implementation & Results Defense"
    p_rev.alignment = PP_ALIGN.CENTER
    p_rev.font.name = "Times New Roman"
    p_rev.font.size = Pt(14)
    p_rev.font.bold = True
    p_rev.font.color.rgb = BRIGHT_BLUE

    tb_title = s1.shapes.add_textbox(Inches(0.6), Inches(3.30), Inches(8.8), Inches(1.1))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    p_t1 = tf_title.paragraphs[0]
    p_t1.text = "KNOWLEDGE GRAPH-BASED QUESTION ANSWERING SYSTEM FOR"
    p_t1.alignment = PP_ALIGN.CENTER
    p_t1.font.name = "Times New Roman"
    p_t1.font.size = Pt(15)
    p_t1.font.bold = True
    p_t1.font.color.rgb = MAROON_DARK

    p_t2 = tf_title.add_paragraph()
    p_t2.text = "EFFICIENT CAMPUS INFORMATION RETRIEVAL & STUDENT HUB"
    p_t2.alignment = PP_ALIGN.CENTER
    p_t2.font.name = "Times New Roman"
    p_t2.font.size = Pt(15)
    p_t2.font.bold = True
    p_t2.font.color.rgb = MAROON_DARK

    tb_sup = s1.shapes.add_textbox(Inches(0.6), Inches(4.50), Inches(8.8), Inches(1.0))
    tf_sup = tb_sup.text_frame
    ps1 = tf_sup.paragraphs[0]
    ps1.text = "Under the Supervision of:"
    ps1.alignment = PP_ALIGN.CENTER
    ps1.font.name = "Times New Roman"
    ps1.font.size = Pt(12)
    ps1.font.bold = True
    ps1.font.color.rgb = SUPERVISION_GREEN

    ps2 = tf_sup.add_paragraph()
    ps2.text = "Mrs. Syeda Neha Shireen, Assistant Professor of CSE"
    ps2.alignment = PP_ALIGN.CENTER
    ps2.font.name = "Times New Roman"
    ps2.font.size = Pt(13)
    ps2.font.bold = True
    ps2.font.color.rgb = SUPERVISION_GREEN

    tb_pres = s1.shapes.add_textbox(Inches(1.8), Inches(5.60), Inches(6.4), Inches(1.6))
    tf_pres = tb_pres.text_frame
    pp1 = tf_pres.paragraphs[0]
    pp1.text = "Presented By:"
    pp1.alignment = PP_ALIGN.CENTER
    pp1.font.name = "Times New Roman"
    pp1.font.size = Pt(13)
    pp1.font.bold = True
    pp1.font.color.rgb = TEXT_BLACK

    team = [
        ("R. Jaya Vinuthna Kumar", "(23N81A05A9)"),
        ("C. Rithvik", "(23N81A05B2)"),
        ("K. Roshini Sree", "(23N81A05B8)"),
        ("M. Swapna", "(23N81A05E1)"),
        ("J. Abhirama Rao", "(23N81A05F8)")
    ]
    for n, r in team:
        pm = tf_pres.add_paragraph()
        pm.text = f"{n:<28} {r}"
        pm.alignment = PP_ALIGN.CENTER
        pm.font.name = "Times New Roman"
        pm.font.size = Pt(11)
        pm.font.bold = True
        pm.font.color.rgb = TEXT_BLACK

    # =========================================================================
    # SLIDE 2: REVIEW-1 COMMITMENTS VS REVIEW-2 DELIVERABLES
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2)
    add_header(s2, "REVIEW-1 COMMITMENTS VS. REVIEW-2 ACHIEVEMENTS")
    add_footer(s2, 2)

    rows, cols = 5, 4
    left, top, width, height = Inches(0.6), Inches(1.3), Inches(8.8), Inches(5.2)
    table_shape = s2.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table
    table.columns[0].width = Inches(1.6)
    table.columns[1].width = Inches(2.5)
    table.columns[2].width = Inches(3.2)
    table.columns[3].width = Inches(1.5)

    headers = ["Milestone", "Review 1 Target Scope", "Review 2 Implementation Outcome", "Status"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = DEEP_NAVY
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.font.size = Pt(11)
        set_cell_border(cell)

    status_data = [
        ("1. Knowledge Graph", "Model academic & physical entities without heuristic guessing.", "Constructed formal Typed DiGraph (536 nodes, 1008 edges across 22 entity types).", "100% Complete"),
        ("2. NLP Pipeline", "Intent classification & typo tolerance on campus terms.", "Implemented TF-IDF, Cosine Similarity, and Gestalt Levenshtein fuzzy entity resolution.", "100% Complete"),
        ("3. Student Hub App", "Concept of unified communication hub to replace WhatsApp.", "Built Student Hub (`/student`) with study notes repository, circulars feed & PWA mobile app.", "100% Complete"),
        ("4. Dynamic Sync & Test", "Admin live graph updates without system restart.", "In-memory dynamic rebuilding (3.84ms hot swap) & 70 automated tests (62 KG + 8 API).", "100% Complete")
    ]

    for row_idx, r in enumerate(status_data, start=1):
        for col_idx, text in enumerate(r):
            cell = table.cell(row_idx, col_idx)
            cell.text = text
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(255, 255, 255) if row_idx % 2 == 1 else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            if col_idx == 3:
                p.font.bold = True
                p.font.color.rgb = EMERALD
            set_cell_border(cell)

    # =========================================================================
    # SLIDE 3: SYSTEM ARCHITECTURE & TOPOLOGY
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3)
    add_header(s3, "SYSTEM ARCHITECTURE & KNOWLEDGE GRAPH TOPOLOGY")
    add_footer(s3, 3)

    arch_bullets = [
        ("Ontological Knowledge Graph Representation", "Typed directed multigraph G = (V, E, τ_v, τ_e) modeled in NetworkX. Enforces strict schema rules across 22 entity types and 19 directional relationships."),
        ("Deterministic Topological Population", "Pipeline maps 8 academic departments, 116 curriculum subjects, faculty profiles, and physical infrastructure (11 buildings, 37 rooms, and labs) without random links."),
        ("Multi-Hop Deterministic Reasoning", "Multi-relational path exploration: Department → HOD → Faculty → Subject → Lab → Building. Guarantees 0% hallucination with sub-150ms retrieval latency."),
        ("In-Memory Graph State", "Topological graph resides in RAM with O(1) adjacency lookup, achieving 0.053 ms mean query traversal time.")
    ]
    tb3 = s3.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(8.8), Inches(5.4))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    for i, (b_title, b_desc) in enumerate(arch_bullets):
        p = tf3.paragraphs[0] if i == 0 else tf3.add_paragraph()
        r1 = p.add_run()
        r1.text = f"■  {b_title}: "
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = TITLE_TEAL
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_BLACK
        p.space_after = Pt(14)

    # =========================================================================
    # SLIDE 4: UNIFIED STUDENT HUB & STUDY MATERIALS APP
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4)
    add_header(s4, "UNIFIED STUDENT HUB & STUDY MATERIALS APP")
    add_footer(s4, 4)

    hub_bullets = [
        ("Unified Academic Portal (`/student`)", "Consolidates lecture notes, unit syllabus PPTs, previous question papers, and official circulars into a single responsive web interface."),
        ("Direct Chatbot Integration", "Students can ask the bot naturally: 'Give me Operating Systems notes' or 'Show latest exam notices' and get direct download links instantly."),
        ("Filter & Search Controls", "Dynamic real-time filtering by Department (CSE, AIML, DS, CS, ECE, Civil, Mech, MBA), Semester (Sem 1 to 8), and keyword text search."),
        ("Faculty Upload Subsystem (`/api/upload-material`)", "Authorized faculty upload lecture notes and assign them directly to subject codes with cryptographic UUID file storage."),
        ("Progressive Web App (PWA) Mobile Enablement", "Manifest (`manifest.json`) and Service Worker (`sw.js`) enable native home-screen installation on Android/iOS phones with offline caching.")
    ]
    tb4 = s4.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(8.8), Inches(5.4))
    tf4 = tb4.text_frame
    tf4.word_wrap = True
    for i, (b_title, b_desc) in enumerate(hub_bullets):
        p = tf4.paragraphs[0] if i == 0 else tf4.add_paragraph()
        r1 = p.add_run()
        r1.text = f"■  {b_title}: "
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = BRIGHT_BLUE
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_BLACK
        p.space_after = Pt(12)

    # =========================================================================
    # SLIDE 5: MULTI-TURN CONVERSATION & CONTEXT TRACKING
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5)
    add_header(s5, "MULTI-TURN DIALOGUE & CONTEXT MEMORY")
    add_footer(s5, 5)

    ctx_bullets = [
        ("Session-Backed Dialogue State", "Maintains active conversational state across turns in Flask session (`session['chat_context']`), storing last department, course, and intent."),
        ("Short-Query Intent Disambiguation", "Queries with length ≤ 4 tokens (e.g. 'who is the HOD?' or 'what is the fee structure?') inherit previously referenced entity context."),
        ("Real-World Test Verification", "Turn 1: 'Tell me about CSE department' (sets dept=cse). Turn 2: 'Who is the HOD?' -> Automatically routes to HOD of CSE (Prof. Kiran B. M.) without re-prompting."),
        ("Typo & Alias Tolerance", "Resolves student abbreviations ('aiml' -> 'cse_aiml', 'hod cabin' -> HOD office location) via fuzzy Gestalt string matching.")
    ]
    tb5 = s5.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(8.8), Inches(5.4))
    tf5 = tb5.text_frame
    tf5.word_wrap = True
    for i, (b_title, b_desc) in enumerate(ctx_bullets):
        p = tf5.paragraphs[0] if i == 0 else tf5.add_paragraph()
        r1 = p.add_run()
        r1.text = f"■  {b_title}: "
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = TITLE_TEAL
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_BLACK
        p.space_after = Pt(14)

    # =========================================================================
    # SLIDE 6: NLP INTENT CLASSIFICATION & FUZZY RESOLUTION
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6)
    add_header(s6, "NLP INTENT CLASSIFICATION & ENTITY RESOLUTION")
    add_footer(s6, 6)

    nlp_bullets = [
        ("TF-IDF Vector Space Normalization", "Converts user queries and training exemplars across 18 intent classes into L2-normalized vector space representations."),
        ("Cosine Similarity Classifier (τ = 0.25)", "Calculates dot products between query vectors and intent centroids to classify user goals accurately in <0.25 ms."),
        ("Priority-Ordered Rule Engine", "Fast deterministic dispatching catches priority domain tokens ('placement', 'admission', 'fee', 'notes', 'circular') before vector classification."),
        ("Levenshtein / Gestalt Fuzzy Matching", "Employs Ratcliff/Obershelp substring matching (cutoff 0.80) to correct misspelled department names and faculty titles."),
        ("Regular Expression Entity Extractors", "Grammar-based pattern matchers isolate courses (B.Tech/M.Tech/MBA), semesters (1-8), building blocks (A-D), and faculty honorifics.")
    ]
    tb6 = s6.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(8.8), Inches(5.4))
    tf6 = tb6.text_frame
    tf6.word_wrap = True
    for i, (b_title, b_desc) in enumerate(nlp_bullets):
        p = tf6.paragraphs[0] if i == 0 else tf6.add_paragraph()
        r1 = p.add_run()
        r1.text = f"■  {b_title}: "
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = DEEP_NAVY
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_BLACK
        p.space_after = Pt(12)

    # =========================================================================
    # SLIDE 7: DYNAMIC IN-MEMORY GRAPH SYNCHRONIZATION
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7)
    add_header(s7, "DYNAMIC IN-MEMORY GRAPH SYNCHRONIZATION")
    add_footer(s7, 7)

    sync_bullets = [
        ("The Static Graph Limitation in Literature", "Prior academic KGQA systems required full server shutdowns or offline batch re-indexing when campus data was modified."),
        ("Hot-Reload Architecture", "When an administrator updates a fee structure, adds a notice, or assigns a faculty member via `/admin`, the route invokes `kg_builder.build_graph()` in active RAM."),
        ("Atomic Reference Swap", "The Flask application context swaps the DiGraph pointer atomically. Ongoing reader requests continue uninterrupted."),
        ("Empirical Performance (3.84 ms)", "Benchmarking confirms complete graph reconstruction takes only 3.84 ms, delivering true zero-downtime campus data synchronization.")
    ]
    tb7 = s7.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(8.8), Inches(5.4))
    tf7 = tb7.text_frame
    tf7.word_wrap = True
    for i, (b_title, b_desc) in enumerate(sync_bullets):
        p = tf7.paragraphs[0] if i == 0 else tf7.add_paragraph()
        r1 = p.add_run()
        r1.text = f"■  {b_title}: "
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = TITLE_TEAL
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_BLACK
        p.space_after = Pt(14)

    # =========================================================================
    # SLIDE 8: AUTOMATED TEST SUITE & VERIFICATION
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8)
    add_header(s8, "AUTOMATED VERIFICATION & TEST SUITE (70 TESTS)")
    add_footer(s8, 8)

    test_rows, test_cols = 5, 4
    t_shape = s8.shapes.add_table(test_rows, test_cols, Inches(0.6), Inches(1.3), Inches(8.8), Inches(5.2))
    tbl = t_shape.table
    tbl.columns[0].width = Inches(2.2)
    tbl.columns[1].width = Inches(1.8)
    tbl.columns[2].width = Inches(3.4)
    tbl.columns[3].width = Inches(1.4)

    t_headers = ["Test Module", "Test Count", "Verification Scope", "Result"]
    for i, h in enumerate(t_headers):
        c = tbl.cell(0, i)
        c.text = h
        c.fill.solid()
        c.fill.fore_color.rgb = DEEP_NAVY
        p = c.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.font.size = Pt(11)
        set_cell_border(c)

    test_matrix = [
        ("Graph Topology (`test_er_kg.py`)", "29 assertions", "Entity types, directional relations, infrastructure containment, faculty mapping.", "29/29 Passed"),
        ("Curriculum & Schema (`test_er_kg.py`)", "21 assertions", "116 subjects, semester hierarchies, Mermaid ER export, zero pseudo-random links.", "21/21 Passed"),
        ("NLP & Queries (`test_er_kg.py`)", "12 assertions", "Building queries, faculty profiles, subjects by sem, fees, placements, greetings.", "12/12 Passed"),
        ("API & Integration (`test_api_integration.py`)", "8 test cases", "HTTP portal views, PWA assets, `/api/materials`, `/api/notices`, multi-turn context.", "8/8 Passed")
    ]
    for row_idx, r in enumerate(test_matrix, start=1):
        for col_idx, text in enumerate(r):
            cell = tbl.cell(row_idx, col_idx)
            cell.text = text
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(255, 255, 255) if row_idx % 2 == 1 else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            if col_idx == 3:
                p.font.bold = True
                p.font.color.rgb = EMERALD
            set_cell_border(cell)

    # =========================================================================
    # SLIDE 9: EMPIRICAL PERFORMANCE BENCHMARK RESULTS
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9)
    add_header(s9, "EMPIRICAL PERFORMANCE BENCHMARK RESULTS")
    add_footer(s9, 9)

    bench_rows, bench_cols = 6, 4
    b_shape = s9.shapes.add_table(bench_rows, bench_cols, Inches(0.6), Inches(1.3), Inches(8.8), Inches(5.2))
    btbl = b_shape.table
    btbl.columns[0].width = Inches(2.5)
    btbl.columns[1].width = Inches(2.2)
    btbl.columns[2].width = Inches(2.2)
    btbl.columns[3].width = Inches(1.9)

    b_headers = ["Performance Metric", "Benchmark Value", "Industry / Standard Target", "Evaluation"]
    for i, h in enumerate(b_headers):
        c = btbl.cell(0, i)
        c.text = h
        c.fill.solid()
        c.fill.fore_color.rgb = DEEP_NAVY
        p = c.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.font.size = Pt(11)
        set_cell_border(c)

    bench_matrix = [
        ("Mean End-to-End Latency", "5.64 ms", "< 150 ms target", "Exceeds by 26x"),
        ("95th Percentile (P95) Latency", "7.06 ms", "< 200 ms target", "Exceeds by 28x"),
        ("Multi-Hop Graph Traversal", "0.053 ms", "< 10 ms target", "Sub-millisecond"),
        ("NLP Intent Classification", "0.230 ms (4414 QPS)", "< 5 ms target", "Sub-millisecond"),
        ("In-Memory Sync Rebuild", "3.84 ms", "< 50 ms target", "Instantaneous")
    ]
    for row_idx, r in enumerate(bench_matrix, start=1):
        for col_idx, text in enumerate(r):
            cell = btbl.cell(row_idx, col_idx)
            cell.text = text
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(255, 255, 255) if row_idx % 2 == 1 else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            if col_idx == 3:
                p.font.bold = True
                p.font.color.rgb = EMERALD
            set_cell_border(cell)

    # =========================================================================
    # SLIDE 10: USER INTERFACE & DEMO SCREENS
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10)
    add_header(s10, "SYSTEM INTERFACE & OPERATIONAL WALKTHROUGH")
    add_footer(s10, 10)

    ui_bullets = [
        ("Unified Campus Portal (`/`)", "Modern responsive web portal showcasing college departments, placement statistics, facilities, leadership, and embedded assistant."),
        ("Student Study Hub (`/student`)", "Clean card-based interface with department & semester filtering for study notes, circular notices stream, and quick-action bot chips."),
        ("Conversational Mobile Assistant", "Floating widget on every page with 100dvh dynamic mobile height, 16px input font (preventing iOS auto-zoom), and quick query suggestions."),
        ("Faculty & Admin Upload Modal", "Pop-up form for authenticated staff to upload PDFs/PPTs and publish circulars with instant live database & graph sync."),
        ("Administrative Management Console (`/admin`)", "CRUD dashboard for managing notices, fee structures, user approvals, and triggering in-memory graph rebuilds.")
    ]
    tb10 = s10.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(8.8), Inches(5.4))
    tf10 = tb10.text_frame
    tf10.word_wrap = True
    for i, (b_title, b_desc) in enumerate(ui_bullets):
        p = tf10.paragraphs[0] if i == 0 else tf10.add_paragraph()
        r1 = p.add_run()
        r1.text = f"■  {b_title}: "
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = BRIGHT_BLUE
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_BLACK
        p.space_after = Pt(12)

    # =========================================================================
    # SLIDE 11: LITERATURE GAPS SOLVED (2023-2025)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s11)
    add_header(s11, "RESEARCH GAPS ADDRESSED & RESOLVED")
    add_footer(s11, 11)

    gap_bullets = [
        ("Gap 1: Static Graph Assumption in Prior KGQA", "Addressed by implementing in-memory dynamic graph synchronization (3.84 ms rebuild) linked directly to web CRUD actions."),
        ("Gap 2: Fragility on Student Slang & Abbreviations", "Addressed via multi-tier NLP combining Gestalt Levenshtein fuzzy matching and domain alias dictionaries."),
        ("Gap 3: Factual Hallucinations in Pure LLM RAG", "Addressed by anchoring all answers in verified Knowledge Graph ontological triples with 100% mathematical verifiability."),
        ("Gap 4: Fragmented Campus Communication", "Addressed by replacing scattered WhatsApp groups and Google Classroom streams with our unified Student Hub (`/student`).")
    ]
    tb11 = s11.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(8.8), Inches(5.4))
    tf11 = tb11.text_frame
    tf11.word_wrap = True
    for i, (b_title, b_desc) in enumerate(gap_bullets):
        p = tf11.paragraphs[0] if i == 0 else tf11.add_paragraph()
        r1 = p.add_run()
        r1.text = f"■  {b_title}: "
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = TITLE_TEAL
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_BLACK
        p.space_after = Pt(14)

    # =========================================================================
    # SLIDE 12: ROLES & CONTRIBUTIONS BREAKDOWN
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s12)
    add_header(s12, "TEAM ROLES & RESPONSIBILITIES BREAKDOWN")
    add_footer(s12, 12)

    team_data = [
        ("R. Jaya Vinuthna Kumar (23N81A05A9)", "Knowledge Graph Architecture, Ontology Design, NetworkX Multigraph modeling, and ER schema generator."),
        ("C. Rithvik (23N81A05B2)", "NLP Pipeline, TF-IDF Intent Classification, Levenshtein Fuzzy Matching, and Multi-Turn Dialogue Context."),
        ("K. Roshini Sree (23N81A05B8)", "Student Study Hub Portal (`/student`), StudyMaterial Repository, Circulars Feed, and PWA Mobile Integration."),
        ("M. Swapna (23N81A05E1)", "Flask Web Application, Route Handlers, Role-Based Access Control (RBAC), and SQLite Persistence."),
        ("J. Abhirama Rao (23N81A05F8)", "Testing Suites (`test_er_kg.py`, `test_api_integration.py`), Performance Benchmarking Engine, and Documentation.")
    ]
    tb12 = s12.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(8.8), Inches(5.4))
    tf12 = tb12.text_frame
    tf12.word_wrap = True
    for i, (mem, role_desc) in enumerate(team_data):
        p = tf12.paragraphs[0] if i == 0 else tf12.add_paragraph()
        r1 = p.add_run()
        r1.text = f"■  {mem}:\n   "
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = DEEP_NAVY
        r2 = p.add_run()
        r2.text = role_desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_BLACK
        p.space_after = Pt(10)

    # =========================================================================
    # SLIDE 13: STRATEGIC FUTURE ROADMAP (PHASE 2)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s13)
    add_header(s13, "STRATEGIC FUTURE ROADMAP (PHASE 2)")
    add_footer(s13, 13)

    future_bullets = [
        ("1. Neo4j Graph Database Migration", "Transition from in-memory NetworkX to external persistent Cypher-compatible graph database (Neo4j) for million-node scale."),
        ("2. Hybrid Graph-RAG with Local Quantized LLM", "Inject retrieved Knowledge Graph subgraphs into local lightweight models (e.g. Llama-3-8B via Ollama) for fluent natural phrasing while preserving 100% graph factuality."),
        ("3. Real-Time Dynamic Timetables & IoT", "Connect Room and Faculty nodes to live schedule databases and smart campus occupancy sensors for real-time room availability checks."),
        ("4. Automated Student Degree Audit", "Enable authenticated students to track course prerequisites, completed credits, and degree progress directly on the curriculum graph.")
    ]
    tb13 = s13.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(8.8), Inches(5.4))
    tf13 = tb13.text_frame
    tf13.word_wrap = True
    for i, (b_title, b_desc) in enumerate(future_bullets):
        p = tf13.paragraphs[0] if i == 0 else tf13.add_paragraph()
        r1 = p.add_run()
        r1.text = f"■  {b_title}: "
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = TITLE_TEAL
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_BLACK
        p.space_after = Pt(14)

    # =========================================================================
    # SLIDE 14: CONCLUSION & Q&A
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s14, BG_SLIDE1)

    tb14 = s14.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(8.0), Inches(3.0))
    tf14 = tb14.text_frame
    tf14.word_wrap = True
    p14_1 = tf14.paragraphs[0]
    p14_1.text = "CONCLUSION & Q&A"
    p14_1.alignment = PP_ALIGN.CENTER
    p14_1.font.name = "Times New Roman"
    p14_1.font.size = Pt(24)
    p14_1.font.bold = True
    p14_1.font.color.rgb = MAROON_DARK

    p14_2 = tf14.add_paragraph()
    p14_2.text = "\nThank you to our guide Mrs. Syeda Neha Shireen and the Department Review Committee.\n" \
                 "We are happy to answer any questions and demonstrate the live platform."
    p14_2.alignment = PP_ALIGN.CENTER
    p14_2.font.name = "Times New Roman"
    p14_2.font.size = Pt(14)
    p14_2.font.color.rgb = TEXT_BLACK

    prs.save(output_pptx)
    print(f"Review 2 presentation created successfully: {output_pptx}")

if __name__ == '__main__':
    create_review_2_presentation()

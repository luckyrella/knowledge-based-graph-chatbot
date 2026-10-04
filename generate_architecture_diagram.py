import os
from PIL import Image, ImageDraw, ImageFont

def create_architecture_diagram(output_path):
    W, H = 1800, 1820
    img = Image.new('RGB', (W, H), (242, 244, 247))
    draw = ImageDraw.Draw(img)

    try:
        f_badge = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 32)
        f_box_title = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 26)
        f_box_sub = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 20)
        f_card_title = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 22)
        f_card_sub = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 17)
    except:
        f_badge = f_box_title = f_box_sub = f_card_title = f_card_sub = ImageFont.load_default()

    def draw_rounded_card(x1, y1, x2, y2, bg_color, border_color, radius=18, border_w=3):
        draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=bg_color, outline=border_color, width=border_w)

    def draw_arrow_down(x, y1, y2, color=(100, 116, 139), width=4, head_len=14):
        draw.line([(x, y1), (x, y2)], fill=color, width=width)
        draw.polygon([(x, y2 + head_len), (x - 8, y2 - 2), (x + 8, y2 - 2)], fill=color)

    def draw_arrow_right(x1, y, x2, color=(50, 50, 50), width=4, head_len=14):
        draw.line([(x1, y), (x2, y)], fill=color, width=width)
        draw.polygon([(x2 + head_len, y), (x2 - 2, y - 8), (x2 - 2, y + 8)], fill=color)

    # 1. INPUT BADGE (Top Left)
    draw.rounded_rectangle([80, 80, 260, 145], radius=32, fill=(199, 220, 255), outline=(130, 170, 255), width=3)
    draw.text((125, 93), 'Input', fill=(20, 40, 110), font=f_badge)
    draw_arrow_right(280, 112, 370, color=(70, 80, 100), width=4)

    # 2. TOP CONTAINER: Campus Information Data
    CX1, CX2 = 400, 1680
    draw_rounded_card(CX1, 40, CX2, 200, (238, 244, 255), (180, 205, 245), radius=22, border_w=3)
    
    title_text = 'Campus Information Data'
    tb = draw.textbbox((0, 0), title_text, font=f_box_title)
    draw.text((CX1 + (CX2 - CX1 - (tb[2] - tb[0])) // 2, 52), title_text, fill=(24, 43, 90), font=f_box_title)

    sub_w = 390
    sub_h = 95
    sub_y = 92
    sub_gaps = (CX2 - CX1 - 3 * sub_w) // 4
    subs = [
        ('Academic Records', 'Departments, Courses, Fees', (255, 255, 255), (200, 215, 240)),
        ('Faculty & Staff', 'Profiles, Research, Contacts', (255, 255, 255), (200, 215, 240)),
        ('Campus Facilities', 'Labs, Library, Events, Placements', (255, 255, 255), (200, 215, 240))
    ]
    for idx, (stitle, ssub, sbg, sborder) in enumerate(subs):
        sx1 = CX1 + sub_gaps + idx * (sub_w + sub_gaps)
        sx2 = sx1 + sub_w
        draw_rounded_card(sx1, sub_y, sx2, sub_y + sub_h, sbg, sborder, radius=14, border_w=2)
        stb = draw.textbbox((0, 0), stitle, font=f_card_title)
        draw.text((sx1 + (sub_w - (stb[2] - stb[0])) // 2, sub_y + 16), stitle, fill=(30, 41, 59), font=f_card_title)
        ssb = draw.textbbox((0, 0), ssub, font=f_card_sub)
        draw.text((sx1 + (sub_w - (ssb[2] - ssb[0])) // 2, sub_y + 52), ssub, fill=(100, 116, 139), font=f_card_sub)

    CENTER_X = (CX1 + CX2) // 2
    draw_arrow_down(CENTER_X, 205, 255)

    # 3. BLOCK: Knowledge Graph Construction & Modeling
    draw_rounded_card(CX1 + 100, 275, CX2 - 100, 385, (230, 249, 238), (140, 210, 170), radius=18, border_w=3)
    t1 = 'Knowledge Graph Construction & Modeling'
    tb1 = draw.textbbox((0, 0), t1, font=f_box_title)
    draw.text((CX1 + 100 + (CX2 - CX1 - 200 - (tb1[2] - tb1[0])) // 2, 290), t1, fill=(15, 80, 45), font=f_box_title)
    s1 = 'Formal ontology design, entity-relationship extraction, and NetworkX graph mapping.'
    sb1 = draw.textbbox((0, 0), s1, font=f_box_sub)
    draw.text((CX1 + 100 + (CX2 - CX1 - 200 - (sb1[2] - sb1[0])) // 2, 335), s1, fill=(40, 95, 65), font=f_box_sub)

    draw_arrow_down(CENTER_X, 390, 440)

    # 4. BLOCK: Conversational User Query
    draw_rounded_card(CX1 + 100, 460, CX2 - 100, 570, (255, 248, 225), (245, 195, 100), radius=18, border_w=3)
    t2 = 'Conversational User Query Processing'
    tb2 = draw.textbbox((0, 0), t2, font=f_box_title)
    draw.text((CX1 + 100 + (CX2 - CX1 - 200 - (tb2[2] - tb2[0])) // 2, 475), t2, fill=(130, 75, 10), font=f_box_title)
    s2 = 'Accept natural language questions from students, faculty, or campus visitors.'
    sb2 = draw.textbbox((0, 0), s2, font=f_box_sub)
    draw.text((CX1 + 100 + (CX2 - CX1 - 200 - (sb2[2] - sb2[0])) // 2, 520), s2, fill=(140, 90, 25), font=f_box_sub)

    draw_arrow_down(CENTER_X, 575, 620)

    # 5. 4 PARALLEL PROCESSING BLOCKS
    card_w = 280
    card_h = 135
    card_y = 645
    card_gap = (CX2 - CX1 - 4 * card_w) // 5
    parallel_cards = [
        ('Intent Classification', 'TF-IDF vectorizer &\ncosine similarity', (255, 235, 238), (245, 140, 155), (150, 25, 45)),
        ('Fuzzy Entity Match', 'Levenshtein distance &\nsynonym resolution', (235, 242, 255), (140, 175, 245), (25, 65, 150)),
        ('Multi-Turn Context', 'Session memory &\nintent decay tracking', (245, 235, 255), (195, 150, 245), (85, 30, 145)),
        ('Graph Query Router', 'SPARQL / path query\nmapping & validation', (235, 255, 240), (145, 225, 170), (20, 110, 55))
    ]

    p_x_coords = []
    for i in range(4):
        p_x_coords.append(CX1 + card_gap + i * (card_w + card_gap) + card_w // 2)

    draw.line([(p_x_coords[0], 620), (p_x_coords[-1], 620)], fill=(100, 116, 139), width=3)
    for px in p_x_coords:
        draw_arrow_down(px, 620, 640, color=(100, 116, 139), width=3, head_len=10)

    for i, (ctitle, csub, cbg, cborder, ctext) in enumerate(parallel_cards):
        cx1 = CX1 + card_gap + i * (card_w + card_gap)
        cx2 = cx1 + card_w
        draw_rounded_card(cx1, card_y, cx2, card_y + card_h, cbg, cborder, radius=16, border_w=2)
        ctb = draw.textbbox((0, 0), ctitle, font=f_card_title)
        draw.text((cx1 + (card_w - (ctb[2] - ctb[0])) // 2, card_y + 14), ctitle, fill=ctext, font=f_card_title)
        
        lines = csub.split('\n')
        ly = card_y + 54
        for l in lines:
            ltb = draw.textbbox((0, 0), l, font=f_card_sub)
            draw.text((cx1 + (card_w - (ltb[2] - ltb[0])) // 2, ly), l, fill=(70, 80, 95), font=f_card_sub)
            ly += 26

    draw.line([(p_x_coords[0], 785), (p_x_coords[-1], 785)], fill=(100, 116, 139), width=3)
    for px in p_x_coords:
        draw.line([(px, card_y + card_h), (px, 785)], fill=(100, 116, 139), width=3)
    draw_arrow_down(CENTER_X, 785, 835)

    # 6. BLOCK: Knowledge Graph Traversal Engine
    draw_rounded_card(CX1 + 100, 855, CX2 - 100, 965, (244, 237, 255), (190, 155, 245), radius=18, border_w=3)
    t3 = 'Knowledge Graph Traversal Engine'
    tb3 = draw.textbbox((0, 0), t3, font=f_box_title)
    draw.text((CX1 + 100 + (CX2 - CX1 - 200 - (tb3[2] - tb3[0])) // 2, 870), t3, fill=(75, 25, 130), font=f_box_title)
    s3 = 'Deterministic graph traversal, multi-hop relationship exploration & sub-graph extraction.'
    sb3 = draw.textbbox((0, 0), s3, font=f_box_sub)
    draw.text((CX1 + 100 + (CX2 - CX1 - 200 - (sb3[2] - sb3[0])) // 2, 915), s3, fill=(85, 45, 140), font=f_box_sub)

    draw_arrow_down(CENTER_X, 970, 1020)

    # 7. BLOCK: Zero-Hallucination Factual Verification
    draw_rounded_card(CX1 + 100, 1040, CX2 - 100, 1150, (235, 244, 255), (150, 190, 245), radius=18, border_w=3)
    t4 = 'Zero-Hallucination Factual Verification'
    tb4 = draw.textbbox((0, 0), t4, font=f_box_title)
    draw.text((CX1 + 100 + (CX2 - CX1 - 200 - (tb4[2] - tb4[0])) // 2, 1055), t4, fill=(20, 60, 130), font=f_box_title)
    s4 = 'Strict factual validation against verified graph triples, ensuring 100% precision.'
    sb4 = draw.textbbox((0, 0), s4, font=f_box_sub)
    draw.text((CX1 + 100 + (CX2 - CX1 - 200 - (sb4[2] - sb4[0])) // 2, 1100), s4, fill=(40, 80, 145), font=f_box_sub)

    draw_arrow_down(CENTER_X, 1155, 1205)

    # 8. BLOCK: Dynamic Graph Synchronization & Admin CRUD
    draw_rounded_card(CX1 + 100, 1225, CX2 - 100, 1335, (255, 242, 230), (245, 165, 100), radius=18, border_w=3)
    t5 = 'Dynamic Graph Synchronization & Admin CRUD'
    tb5 = draw.textbbox((0, 0), t5, font=f_box_title)
    draw.text((CX1 + 100 + (CX2 - CX1 - 200 - (tb5[2] - tb5[0])) // 2, 1240), t5, fill=(140, 60, 10), font=f_box_title)
    s5 = 'Real-time incremental updates, automated schema synchronization & live JSON persistence.'
    sb5 = draw.textbbox((0, 0), s5, font=f_box_sub)
    draw.text((CX1 + 100 + (CX2 - CX1 - 200 - (sb5[2] - sb5[0])) // 2, 1285), s5, fill=(145, 75, 20), font=f_box_sub)

    draw_arrow_down(CENTER_X, 1340, 1390)

    # 9. BLOCK: Response Synthesis & Interactive Visualization
    draw_rounded_card(CX1 + 100, 1410, CX2 - 100, 1520, (230, 249, 242), (135, 215, 180), radius=18, border_w=3)
    t6 = 'Response Synthesis & Interactive Visualization'
    tb6 = draw.textbbox((0, 0), t6, font=f_box_title)
    draw.text((CX1 + 100 + (CX2 - CX1 - 200 - (tb6[2] - tb6[0])) // 2, 1425), t6, fill=(10, 90, 55), font=f_box_title)
    s6 = 'Synthesize natural conversational responses and generate interactive D3.js subgraphs.'
    sb6 = draw.textbbox((0, 0), s6, font=f_box_sub)
    draw.text((CX1 + 100 + (CX2 - CX1 - 200 - (sb6[2] - sb6[0])) // 2, 1470), s6, fill=(25, 105, 65), font=f_box_sub)

    draw_arrow_down(CENTER_X, 1525, 1575)

    # 10. OUTPUT BADGE (Bottom Left)
    draw.rounded_rectangle([80, 1610, 270, 1675], radius=32, fill=(205, 200, 255), outline=(150, 140, 245), width=3)
    draw.text((115, 1622), 'Output', fill=(55, 35, 125), font=f_badge)
    draw_arrow_right(290, 1642, 370, color=(70, 80, 100), width=4)

    # 11. BOTTOM OUTPUTS (4 Cards)
    out_w = 280
    out_h = 100
    out_y = 1595
    out_gap = (CX2 - CX1 - 4 * out_w) // 5
    outputs = [
        ('Instant Factual Answer', 'Direct response', (255, 235, 238), (245, 140, 155), (150, 25, 45)),
        ('Interactive Subgraph', 'Entity network view', (230, 249, 238), (140, 210, 170), (15, 85, 45)),
        ('Related Suggestions', 'Follow-up topics', (235, 242, 255), (140, 175, 245), (25, 65, 150)),
        ('Admin Audit & Stats', 'Log tracking & stats', (245, 235, 255), (195, 150, 245), (85, 30, 145))
    ]

    out_x_coords = []
    for i in range(4):
        out_x_coords.append(CX1 + out_gap + i * (out_w + out_gap) + out_w // 2)

    draw.line([(out_x_coords[0], 1575), (out_x_coords[-1], 1575)], fill=(100, 116, 139), width=3)
    for ox in out_x_coords:
        draw_arrow_down(ox, 1575, 1592, color=(100, 116, 139), width=3, head_len=8)

    for i, (otitle, osub, obg, oborder, otext) in enumerate(outputs):
        ox1 = CX1 + out_gap + i * (out_w + out_gap)
        ox2 = ox1 + out_w
        draw_rounded_card(ox1, out_y, ox2, out_y + out_h, obg, oborder, radius=16, border_w=2)
        otb = draw.textbbox((0, 0), otitle, font=f_card_title)
        draw.text((ox1 + (out_w - (otb[2] - otb[0])) // 2, out_y + 18), otitle, fill=otext, font=f_card_title)
        osb = draw.textbbox((0, 0), osub, font=f_card_sub)
        draw.text((ox1 + (out_w - (osb[2] - osb[0])) // 2, out_y + 54), osub, fill=(80, 90, 105), font=f_card_sub)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, quality=95)
    print('Generated architecture diagram successfully at:', output_path)

if __name__ == '__main__':
    create_architecture_diagram('extracted_assets/architecture_diagram.png')

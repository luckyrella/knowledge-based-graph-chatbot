import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_activity_diagram():
    fig, ax = plt.subplots(figsize=(16, 20), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # Title
    ax.text(50, 98.5, "UML ACTIVITY DIAGRAM: CHAT QUERY PROCESSING PIPELINE",
            fontsize=15, fontweight='bold', ha='center', va='center', color='#1A365D')
    ax.text(50, 96.8, "Natural Language Understanding (NLP) → Knowledge Graph Traversal → Asynchronous Logging",
            fontsize=10.5, fontstyle='italic', ha='center', va='center', color='#4A5568')

    def draw_action(x, y, w, h, text, color="#EBF8FF", border="#3182CE"):
        box = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.3,rounding_size=0.8",
                                     facecolor=color, edgecolor=border, linewidth=1.6, zorder=3)
        ax.add_patch(box)
        ax.text(x, y, text, fontsize=8.5, ha='center', va='center', color='#1A202C', fontweight='semibold', zorder=4)
        return (x, y + h/2), (x, y - h/2), (x - w/2, y), (x + w/2, y) # top, bottom, left, right

    def draw_decision(x, y, size, text):
        diamond = patches.RegularPolygon((x, y), numVertices=4, radius=size, orientation=0,
                                         facecolor='#FFF5F5', edgecolor='#E53E3E', linewidth=1.6, zorder=3)
        ax.add_patch(diamond)
        ax.text(x, y, text, fontsize=7.5, ha='center', va='center', color='#9B2C2C', fontweight='bold', zorder=4)
        return (x, y + size*0.7), (x, y - size*0.7), (x - size*0.7, y), (x + size*0.7, y)

    # 1. Start Node
    start_circle = patches.Circle((50, 94), 1.2, facecolor='#1A202C', edgecolor='#1A202C', zorder=4)
    ax.add_patch(start_circle)
    ax.text(50, 94, "", ha='center')

    # Flow connections
    # Node 1: User Types Message
    t, b, l, r = draw_action(50, 89.5, 34, 3.2, "User types question in web chat widget\n(Sends HTTP POST /api/chat with message & context)")
    ax.annotate("", xy=t, xytext=(50, 92.8), arrowprops=dict(arrowstyle="->", color="#2D3748", lw=1.5))

    # Decision 1: Is message empty?
    d1_t, d1_b, d1_l, d1_r = draw_decision(50, 83.5, 3.2, "Message\nEmpty?")
    ax.annotate("", xy=d1_t, xytext=b, arrowprops=dict(arrowstyle="->", color="#2D3748", lw=1.5))

    # Branch: Empty -> Return prompt -> Stop
    err_t, err_b, err_l, err_r = draw_action(80, 83.5, 20, 2.8, "Return warning:\n'Please ask a question!'", color="#FFF5F5", border="#E53E3E")
    ax.annotate("", xy=err_l, xytext=d1_r, arrowprops=dict(arrowstyle="->", color="#E53E3E", lw=1.5))
    ax.text(67, 84.3, "[Yes]", fontsize=8, color="#E53E3E", fontweight='bold')

    # Stop circle for error branch
    end_out = patches.Circle((95, 83.5), 1.2, facecolor='none', edgecolor='#E53E3E', linewidth=1.5, zorder=4)
    end_in = patches.Circle((95, 83.5), 0.7, facecolor='#E53E3E', zorder=5)
    ax.add_patch(end_out)
    ax.add_patch(end_in)
    ax.annotate("", xy=(93.8, 83.5), xytext=err_r, arrowprops=dict(arrowstyle="->", color="#E53E3E", lw=1.5))

    # Branch: Not Empty -> NLP classify intent
    nlp_t, nlp_b, nlp_l, nlp_r = draw_action(50, 77.0, 36, 3.2, "NLP Processor: Normalize text aliases\n(e.g., 'b tech' → 'btech', 'ai ml' → 'cse_aiml')")
    ax.annotate("", xy=nlp_t, xytext=d1_b, arrowprops=dict(arrowstyle="->", color="#2D3748", lw=1.5))
    ax.text(50.8, 81.2, "[No]", fontsize=8, color="#2B6CB0", fontweight='bold')

    # Decision 2: Short follow-up with context?
    d2_t, d2_b, d2_l, d2_r = draw_decision(50, 70.0, 3.4, "Short query\n(<=4 words) &\nhas context?")
    ax.annotate("", xy=d2_t, xytext=nlp_b, arrowprops=dict(arrowstyle="->", color="#2D3748", lw=1.5))

    # Branch Left: Context Follow-up
    kw_c_t, kw_c_b, kw_c_l, kw_c_r = draw_action(24, 63.5, 24, 3.0, "Scan keyword rules\nfor topic override")
    ax.annotate("", xy=kw_c_t, xytext=d2_l, arrowprops=dict(arrowstyle="->", color="#2D3748", lw=1.5, connectionstyle="arc3,rad=-0.1"))
    ax.text(34, 70.8, "[Yes: Follow-up]", fontsize=8, color="#2C7A7B", fontweight='bold')

    inh_t, inh_b, inh_l, inh_r = draw_action(24, 57.0, 24, 3.0, "Inherit lastIntent\nfrom prior context turn", color="#E6FFFA", border="#319795")
    ax.annotate("", xy=inh_t, xytext=kw_c_b, arrowprops=dict(arrowstyle="->", color="#2C7A7B", lw=1.5))

    # Branch Right: Standard Intent Classification
    pri_t, pri_b, pri_l, pri_r = draw_action(76, 63.5, 28, 3.0, "Evaluate 18 Keyword Rules\nin strict priority order")
    ax.annotate("", xy=pri_t, xytext=d2_r, arrowprops=dict(arrowstyle="->", color="#2D3748", lw=1.5, connectionstyle="arc3,rad=0.1"))
    ax.text(64, 70.8, "[No: New Query]", fontsize=8, color="#2B6CB0", fontweight='bold')

    tfidf_t, tfidf_b, tfidf_l, tfidf_r = draw_action(76, 57.0, 28, 3.0, "TF-IDF Cosine Similarity\n(Fallback if threshold > 0.25)")
    ax.annotate("", xy=tfidf_t, xytext=pri_b, arrowprops=dict(arrowstyle="->", color="#2D3748", lw=1.5))

    # Join 1: Entity Extraction
    merge_t, merge_b, merge_l, merge_r = draw_action(50, 50.0, 48, 3.6, "Entity Extraction Pipeline:\nRegex Matchers for Department, Course, Semester, Faculty & Building\n+ Context Carry-Forward for missing entities", color="#FEFCBF", border="#D69E2E")
    
    ax.annotate("", xy=merge_l, xytext=inh_b, arrowprops=dict(arrowstyle="->", color="#2C7A7B", lw=1.5, connectionstyle="arc3,rad=-0.15"))
    ax.annotate("", xy=merge_r, xytext=tfidf_b, arrowprops=dict(arrowstyle="->", color="#2B6CB0", lw=1.5, connectionstyle="arc3,rad=0.15"))

    # Action: Route to KG
    route_t, route_b, route_l, route_r = draw_action(50, 43.5, 38, 3.0, "_route_intent(): Dispatch to KnowledgeGraphQuery Engine")
    ax.annotate("", xy=route_t, xytext=merge_b, arrowprops=dict(arrowstyle="->", color="#2D3748", lw=1.5))

    # Fork Bar (Parallel Graph Query Targets)
    fork_bar = patches.Rectangle((10, 38.0), 80, 0.8, facecolor='#1A202C', edgecolor='#1A202C', zorder=5)
    ax.add_patch(fork_bar)
    ax.annotate("", xy=(50, 38.8), xytext=route_b, arrowprops=dict(arrowstyle="->", color="#1A202C", lw=2))

    # Parallel Query Handlers
    handlers = [
        ("query_department()\nTraversal: College -> Dept", 18, 32.5, 17, 3.2),
        ("query_fees()\nLookup: Fees node & quota", 38, 32.5, 18, 3.2),
        ("query_placements()\nStats & Top Recruiters", 58, 32.5, 17, 3.2),
        ("query_faculty_profile()\nDept -> Staff -> Research", 78, 32.5, 18, 3.2),
    ]
    for hname, hx, hy, hw, hh in handlers:
        ht, hb, hl, hr = draw_action(hx, hy, hw, hh, hname, color="#FAF5FF", border="#6B46C1")
        ax.annotate("", xy=ht, xytext=(hx, 38.0), arrowprops=dict(arrowstyle="->", color="#1A202C", lw=1.3))

    # Join Bar
    join_bar = patches.Rectangle((10, 26.5), 80, 0.8, facecolor='#1A202C', edgecolor='#1A202C', zorder=5)
    ax.add_patch(join_bar)
    for _, hx, hy, _, hh in handlers:
        ax.annotate("", xy=(hx, 27.3), xytext=(hx, hy - hh/2), arrowprops=dict(arrowstyle="->", color="#1A202C", lw=1.3))

    # Response Assembly
    resp_t, resp_b, resp_l, resp_r = draw_action(50, 21.0, 36, 3.0, "Response Formatter: Format Markdown\n(Headers, Bullet points, Emojis, Links)")
    ax.annotate("", xy=resp_t, xytext=(50, 26.5), arrowprops=dict(arrowstyle="->", color="#1A202C", lw=2))

    # DB Logging (Asynchronous)
    db_t, db_b, db_l, db_r = draw_action(50, 14.5, 36, 3.0, "Persist Chat Telemetry (SQLite):\nInsert ChatMessage (session_id, response_time_ms, intent)", color="#EDF2F7", border="#4A5568")
    ax.annotate("", xy=db_t, xytext=resp_b, arrowprops=dict(arrowstyle="->", color="#2D3748", lw=1.5))

    # Frontend Render
    ui_t, ui_b, ui_l, ui_r = draw_action(50, 8.0, 36, 3.0, "Return JSON to Frontend Chatbot Widget\n& Animate typing response in UI")
    ax.annotate("", xy=ui_t, xytext=db_b, arrowprops=dict(arrowstyle="->", color="#2D3748", lw=1.5))

    # Final End Node (Bullseye)
    end_main_out = patches.Circle((50, 2.5), 1.4, facecolor='none', edgecolor='#1A202C', linewidth=1.8, zorder=4)
    end_main_in = patches.Circle((50, 2.5), 0.8, facecolor='#1A202C', zorder=5)
    ax.add_patch(end_main_out)
    ax.add_patch(end_main_in)
    ax.annotate("", xy=(50, 3.9), xytext=ui_b, arrowprops=dict(arrowstyle="->", color="#1A202C", lw=1.8))

    plt.tight_layout()
    out_path = "c:/Users/lucky/JC-Rella Su-6372/major project/uml_diagrams/activity_diagram.jpg"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Activity diagram generated successfully at:", out_path)

if __name__ == "__main__":
    generate_activity_diagram()

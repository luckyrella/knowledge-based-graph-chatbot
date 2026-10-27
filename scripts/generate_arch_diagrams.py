import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_component_diagram():
    fig, ax = plt.subplots(figsize=(20, 15), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # Title
    ax.text(50, 98, "UML COMPONENT DIAGRAM: 4-TIER MODULAR SYSTEM ARCHITECTURE",
            fontsize=15, fontweight='bold', ha='center', va='center', color='#1A365D')
    ax.text(50, 96, "Layered Architecture: Presentation, Application Services, Knowledge & Intelligence Engine, Data Tier",
            fontsize=10.5, fontstyle='italic', ha='center', va='center', color='#4A5568')

    def draw_package(x, y, w, h, name, color="#F7FAFC", border="#2B6CB0"):
        # Tab
        tab = patches.Rectangle((x, y + h), w*0.35, 2.2, facecolor=color, edgecolor=border, linewidth=1.5, zorder=2)
        ax.add_patch(tab)
        ax.text(x + w*0.175, y + h + 1.1, name, fontsize=8.5, fontweight='bold', ha='center', va='center', color='#2D3748', zorder=3)
        # Main box
        box = patches.Rectangle((x, y), w, h, facecolor=color, edgecolor=border, linewidth=1.5, zorder=1)
        ax.add_patch(box)

    def draw_component(x, y, w, h, name, subtitle="", color="#FFFFFF", border="#4A5568"):
        cbox = patches.FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0.2", facecolor=color, edgecolor=border, linewidth=1.4, zorder=3)
        ax.add_patch(cbox)
        # UML Component tabs on left side
        tab1 = patches.Rectangle((x - 1.2, y + h*0.65), 2.4, h*0.2, facecolor='#EDF2F7', edgecolor=border, linewidth=1.2, zorder=4)
        tab2 = patches.Rectangle((x - 1.2, y + h*0.2), 2.4, h*0.2, facecolor='#EDF2F7', edgecolor=border, linewidth=1.2, zorder=4)
        ax.add_patch(tab1)
        ax.add_patch(tab2)
        
        ax.text(x + w/2 + 0.5, y + h/2 + (0.8 if subtitle else 0), name, fontsize=8.5, fontweight='bold', ha='center', va='center', color='#1A202C', zorder=5)
        if subtitle:
            ax.text(x + w/2 + 0.5, y + h/2 - 1.0, subtitle, fontsize=7.2, fontstyle='italic', ha='center', va='center', color='#718096', zorder=5)
        return {"top": (x + w/2, y + h), "bottom": (x + w/2, y), "left": (x, y + h/2), "right": (x + w, y + h/2)}

    # Layer 1: Presentation Layer
    draw_package(4, 73, 92, 19, "Presentation Layer (Client-Side)", color="#EBF8FF", border="#3182CE")
    c_web = draw_component(7, 75, 26, 12, "College Web Portal", "Jinja2 HTML5 / Responsive CSS", color="#FFFFFF", border="#3182CE")
    c_chat = draw_component(37, 75, 26, 12, "Chatbot UI Widget", "static/js/chatbot.js", color="#FFFFFF", border="#3182CE")
    c_admin_ui = draw_component(67, 75, 26, 12, "Admin Dashboard UI", "admin_dashboard.html", color="#FFFFFF", border="#3182CE")

    # Layer 2: Application Services Layer
    draw_package(4, 50, 92, 19, "Application Layer (Flask Web Framework)", color="#E6FFFA", border="#319795")
    c_app = draw_component(7, 52, 26, 12, "Core Flask Server", "app.py (create_app factory)", color="#FFFFFF", border="#319795")
    c_auth = draw_component(37, 52, 26, 12, "Authentication Service", "Flask-Login + auth_bp", color="#FFFFFF", border="#319795")
    c_api = draw_component(67, 52, 26, 12, "API Gateway / Endpoints", "/api/chat, /api/graph-data", color="#FFFFFF", border="#319795")

    # Layer 3: Intelligence & Knowledge Graph Engine
    draw_package(4, 27, 92, 19, "Intelligence Layer (Knowledge Graph & NLP)", color="#FAF5FF", border="#805AD5")
    c_nlp = draw_component(7, 29, 26, 12, "NLP Processor", "TF-IDF + Regex Entity Parser", color="#FFFFFF", border="#805AD5")
    c_kg_q = draw_component(37, 29, 26, 12, "KG Query Engine", "kg_query.py (DiGraph Traversal)", color="#FFFFFF", border="#805AD5")
    c_kg_b = draw_component(67, 29, 26, 12, "KG Builder & Ontology", "kg_builder.py & ontology.py", color="#FFFFFF", border="#805AD5")

    # Layer 4: Data Layer
    draw_package(4, 4, 92, 19, "Persistence & Data Layer", color="#FEFCBF", border="#D69E2E")
    c_db = draw_component(17, 6, 28, 12, "SQLite Database", "instance/campus_kg.db (SQLAlchemy)", color="#FFFFFF", border="#D69E2E")
    c_json = draw_component(55, 6, 28, 12, "JSON Knowledge Base", "college_data.json & faculty_data.json", color="#FFFFFF", border="#D69E2E")

    # Connectors between components
    def link_comp(c1, c2, label=""):
        ax.annotate("", xy=c2, xytext=c1, arrowprops=dict(arrowstyle="->", linestyle="--", color="#4A5568", lw=1.5), zorder=6)
        if label:
            mx = (c1[0] + c2[0])/2
            my = (c1[1] + c2[1])/2
            ax.text(mx + 1, my, label, fontsize=7.5, color='#4A5568', fontweight='bold', zorder=7)

    # Presentation -> Application
    link_comp(c_web["bottom"], c_app["top"], "HTTP GET")
    link_comp(c_chat["bottom"], c_api["top"], "POST /api/chat")
    link_comp(c_admin_ui["bottom"], c_auth["top"], "Session Auth")

    # Application -> Intelligence
    link_comp(c_api["bottom"], c_nlp["top"], "parse()")
    link_comp(c_api["bottom"], c_kg_q["top"], "query()")
    link_comp(c_app["bottom"], c_kg_b["top"], "init_graph()")

    # Intelligence -> Data
    link_comp(c_kg_b["bottom"], c_json["top"], "load_data()")
    link_comp(c_api["bottom"], c_db["top"], "log_chat()")
    link_comp(c_auth["bottom"], c_db["top"], "query_user()")

    plt.tight_layout()
    out_path = "c:/Users/lucky/JC-Rella Su-6372/major project/uml_diagrams/component_diagram.jpg"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Component diagram generated successfully at:", out_path)

def generate_deployment_diagram():
    fig, ax = plt.subplots(figsize=(18, 13), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # Title
    ax.text(50, 97.5, "UML DEPLOYMENT DIAGRAM: PHYSICAL & RUNTIME TOPOLOGY",
            fontsize=15, fontweight='bold', ha='center', va='center', color='#1A365D')
    ax.text(50, 95.5, "Client-Server Architecture: Client Browser Node ↔ Web & Intelligence Application Server Node",
            fontsize=10.5, fontstyle='italic', ha='center', va='center', color='#4A5568')

    def draw_3d_node(x, y, w, h, depth, name, color="#F8FAFC", border="#2B6CB0"):
        # Front face
        front = patches.Rectangle((x, y), w, h, facecolor=color, edgecolor=border, linewidth=1.6, zorder=2)
        ax.add_patch(front)
        # Top face
        top_poly = patches.Polygon([[x, y + h], [x + depth, y + h + depth], [x + w + depth, y + h + depth], [x + w, y + h]],
                                   facecolor='#EDF2F7', edgecolor=border, linewidth=1.6, zorder=2)
        ax.add_patch(top_poly)
        # Right face
        right_poly = patches.Polygon([[x + w, y], [x + w + depth, y + depth], [x + w + depth, y + h + depth], [x + w, y + h]],
                                     facecolor='#E2E8F0', edgecolor=border, linewidth=1.6, zorder=2)
        ax.add_patch(right_poly)
        # Label
        ax.text(x + w/2, y + h - 2.0, f"«device»\n{name}", fontsize=10, fontweight='bold', ha='center', va='center', color='#1A365D', zorder=4)
        return (x + w + depth, y + h/2) # right connection point

    # Node 1: Client Node
    c_client = draw_3d_node(5, 30, 26, 48, 3, "Client Device\n(PC / Smartphone)", color="#EBF8FF", border="#3182CE")
    # Artifact inside Client
    art_browser = patches.Rectangle((8, 36), 20, 28, facecolor="#FFFFFF", edgecolor="#4A5568", linewidth=1.2, zorder=3)
    ax.add_patch(art_browser)
    ax.text(18, 59, "«execution environment»\nWeb Browser", fontsize=8.5, fontweight='bold', ha='center', va='center', color='#2D3748', zorder=4)
    ax.text(18, 48, "Artifacts:\n• HTML5 / CSS3 DOM\n• chatbot.js (ES6 AJAX)\n• Session Cookie Storage", fontsize=7.5, ha='center', va='center', color='#4A5568', zorder=4)

    # Node 2: Server Node
    c_server = draw_3d_node(48, 10, 46, 75, 4, "Campus Application Server\n(localhost:5000 / Production Host)", color="#F7FAFC", border="#2B6CB0")
    
    # Internal Tiers inside Server Node
    # Tier 1: WSGI & Flask
    t1 = patches.Rectangle((51, 62), 40, 14, facecolor="#FFFFFF", edgecolor="#3182CE", linewidth=1.2, zorder=3)
    ax.add_patch(t1)
    ax.text(71, 72.5, "«web container» Werkzeug WSGI Server", fontsize=8.5, fontweight='bold', ha='center', color='#2B6CB0', zorder=4)
    ax.text(71, 66.5, "Flask 3.x App (app.py) | Flask-Login 0.6 | Jinja2 Template Engine", fontsize=7.5, ha='center', color='#4A5568', zorder=4)

    # Tier 2: NLP & Graph Inference
    t2 = patches.Rectangle((51, 42), 40, 17, facecolor="#FFFFFF", edgecolor="#805AD5", linewidth=1.2, zorder=3)
    ax.add_patch(t2)
    ax.text(71, 55.5, "«execution engine» Graph & NLP Runtime", fontsize=8.5, fontweight='bold', ha='center', color='#6B46C1', zorder=4)
    ax.text(71, 47.5, "• NetworkX 3.x (In-Memory DiGraph Engine)\n• scikit-learn (TF-IDF Vectorizer + Cosine Sim)\n• Custom Ontology Validation Rules", fontsize=7.5, ha='center', color='#4A5568', zorder=4)

    # Tier 3: Storage
    t3 = patches.Rectangle((51, 16), 40, 22, facecolor="#FFFFFF", edgecolor="#D69E2E", linewidth=1.2, zorder=3)
    ax.add_patch(t3)
    ax.text(71, 33.5, "«database system» Persistence Storage", fontsize=8.5, fontweight='bold', ha='center', color='#B7791F', zorder=4)
    ax.text(71, 23.5, "• SQLite Engine: instance/campus_kg.db\n  (Users, Messages, Feedback, KG Entities)\n• JSON Flat Files: data/college_data.json\n  (Curriculum, Faculty, Infrastructure)", fontsize=7.5, ha='center', color='#4A5568', zorder=4)

    # Network Protocol Connection
    ax.plot([34, 48], [54, 54], color="#2B6CB0", lw=2.5, zorder=5)
    ax.text(41, 56.5, "«protocol»\nHTTPS / REST API\n(Port 5000)", fontsize=8, fontweight='bold', ha='center', va='center', color='#2B6CB0')

    plt.tight_layout()
    out_path = "c:/Users/lucky/JC-Rella Su-6372/major project/uml_diagrams/deployment_diagram.jpg"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Deployment diagram generated successfully at:", out_path)

def generate_state_diagram():
    fig, ax = plt.subplots(figsize=(18, 10), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # Title
    ax.text(50, 96, "UML STATE MACHINE DIAGRAM: USER ACCOUNT & SESSION LIFECYCLE",
            fontsize=15, fontweight='bold', ha='center', va='center', color='#1A365D')
    ax.text(50, 93, "States & Transitions: Registration Request → Admin Moderation → Active User Session",
            fontsize=10.5, fontstyle='italic', ha='center', va='center', color='#4A5568')

    def draw_state(x, y, w, h, name, desc="", color="#EBF8FF", border="#3182CE"):
        box = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.3,rounding_size=1.0",
                                     facecolor=color, edgecolor=border, linewidth=1.6, zorder=2)
        ax.add_patch(box)
        ax.text(x, y + (0.9 if desc else 0), name, fontsize=9.5, fontweight='bold', ha='center', va='center', color='#1A202C', zorder=3)
        if desc:
            ax.text(x, y - 1.2, desc, fontsize=7.5, fontstyle='italic', ha='center', va='center', color='#4A5568', zorder=3)
        return {"top": (x, y + h/2), "bottom": (x, y - h/2), "left": (x - w/2, y), "right": (x + w/2, y)}

    # Initial State (Filled Circle)
    start = patches.Circle((8, 70), 1.5, facecolor='#1A202C', edgecolor='#1A202C', zorder=3)
    ax.add_patch(start)

    # States
    s_unreg = draw_state(25, 70, 18, 9, "Unregistered", "Public Visitor / Guest")
    s_pending = draw_state(54, 70, 21, 9, "PendingApproval", "is_approved = False", color="#FEFCBF", border="#D69E2E")
    s_rejected = draw_state(86, 70, 18, 9, "Rejected", "Registration denied", color="#FED7D7", border="#E53E3E")

    s_active = draw_state(54, 35, 21, 9, "Active", "is_approved = True\nis_active = True", color="#C6F6D5", border="#38A169")
    s_inactive = draw_state(86, 35, 18, 9, "Inactive / Suspended", "is_active = False", color="#EDF2F7", border="#718096")
    s_auth = draw_state(25, 35, 18, 9, "Authenticated", "Flask-Login session active", color="#E9D8FD", border="#805AD5")

    # Terminal End State (Bullseye)
    end_out = patches.Circle((86, 12), 1.6, facecolor='none', edgecolor='#1A202C', linewidth=1.8, zorder=3)
    end_in = patches.Circle((86, 12), 0.9, facecolor='#1A202C', zorder=4)
    ax.add_patch(end_out)
    ax.add_patch(end_in)
    ax.text(86, 6, "Account Purged\n(Deleted from DB)", fontsize=8, ha='center', color='#718096')

    # Transitions with arrows
    def transition(p1, p2, label, color="#2D3748", rad=0.0):
        ax.annotate("", xy=p2, xytext=p1,
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.5, connectionstyle=f"arc3,rad={rad}"), zorder=4)
        mx = (p1[0] + p2[0])/2
        my = (p1[1] + p2[1])/2 + (1.2 if rad == 0 else 2.0)
        ax.text(mx, my, label, fontsize=8, fontweight='semibold', ha='center', va='center', color=color, zorder=5)

    transition((9.5, 70), s_unreg["left"], "Visits site")
    transition(s_unreg["right"], s_pending["left"], "Submit Register Form\n[New credentials]")
    transition(s_pending["right"], s_rejected["left"], "Admin Rejects", color="#E53E3E")
    transition(s_rejected["bottom"], (86, 13.6), "Delete Record", color="#E53E3E")
    
    transition(s_pending["bottom"], s_active["top"], "Admin Approves\n[is_approved = True]", color="#276749")
    
    transition((s_active["right"][0], s_active["right"][1] + 1.5), (s_inactive["left"][0], s_inactive["left"][1] + 1.5), "Deactivate", color="#718096")
    transition((s_inactive["left"][0], s_inactive["left"][1] - 1.5), (s_active["right"][0], s_active["right"][1] - 1.5), "Reactivate", color="#276749")

    transition((s_active["left"][0], s_active["left"][1] + 1.5), (s_auth["right"][0], s_auth["right"][1] + 1.5), "Login [Valid Pwd]", color="#6B46C1")
    transition((s_auth["right"][0], s_auth["right"][1] - 1.5), (s_active["left"][0], s_active["left"][1] - 1.5), "Logout / Session Expire", color="#4A5568")

    # Self loop for active session
    ax.annotate("", xy=(20, 39.5), xytext=(30, 39.5),
                arrowprops=dict(arrowstyle="->", color="#6B46C1", lw=1.3, connectionstyle="arc,angleA=90,angleB=90,armA=15,armB=15,rad=4"), zorder=4)
    ax.text(25, 45, "Interact: Chat, Manage Notices, View Stats", fontsize=7.5, color='#6B46C1', ha='center')

    plt.tight_layout()
    out_path = "c:/Users/lucky/JC-Rella Su-6372/major project/uml_diagrams/state_diagram.jpg"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("State diagram generated successfully at:", out_path)

if __name__ == "__main__":
    generate_component_diagram()
    generate_deployment_diagram()
    generate_state_diagram()

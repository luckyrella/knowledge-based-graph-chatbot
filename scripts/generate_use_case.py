import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_use_case_diagram():
    fig, ax = plt.subplots(figsize=(20, 15), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Background canvas
    fig.patch.set_facecolor('#FFFFFF')

    # Main Title
    ax.text(50, 97.8, "USE CASE DIAGRAM: KG-RAG CAMPUS KNOWLEDGE MANAGEMENT SYSTEM",
            fontsize=16, fontweight='bold', ha='center', va='center', color='#1A365D')
    ax.text(50, 95.8, "Sphoorthy Engineering College (UGC Autonomous) — Department of Computer Science & Engineering",
            fontsize=11, fontstyle='italic', ha='center', va='center', color='#4A5568')

    # Outer System Boundary Box
    boundary = patches.FancyBboxPatch((28, 2.5), 70, 91, boxstyle="round,pad=0.8,rounding_size=1.2",
                                      edgecolor='#2B6CB0', facecolor='#F8FAFC', linewidth=2.5, zorder=1)
    ax.add_patch(boundary)
    ax.text(63, 91.8, "System Boundary: KG-RAG Web Application & Campus Assistant",
            fontsize=13, fontweight='bold', ha='center', va='center', color='#2B6CB0')

    # 4 Subsystems / Packages
    subsystems = [
        {"name": "Subsystem 1: Public Information & Inquiry", "x": 30, "y": 66, "w": 33, "h": 23.5, "color": "#EBF8FF", "border": "#3182CE"},
        {"name": "Subsystem 2: Authentication & Profile", "x": 65, "y": 66, "w": 31.5, "h": 23.5, "color": "#E6FFFA", "border": "#319795"},
        {"name": "Subsystem 3: Academic & Department Portal", "x": 30, "y": 37, "w": 33, "h": 27, "color": "#FEFCBF", "border": "#D69E2E"},
        {"name": "Subsystem 4: System Administration & KG Operations", "x": 65, "y": 5, "w": 31.5, "h": 59, "color": "#FED7D7", "border": "#E53E3E"},
    ]

    for sub in subsystems:
        rect = patches.FancyBboxPatch((sub["x"], sub["y"]), sub["w"], sub["h"],
                                      boxstyle="round,pad=0.5,rounding_size=0.8",
                                      edgecolor=sub["border"], facecolor=sub["color"], linewidth=1.5, linestyle='--', zorder=2)
        ax.add_patch(rect)
        ax.text(sub["x"] + sub["w"]/2, sub["y"] + sub["h"] - 1.8, sub["name"],
                fontsize=9.5, fontweight='bold', ha='center', va='center', color='#2D3748', zorder=3)

    # Dictionary of Use Cases: (label, center_x, center_y, radius_x, radius_y)
    use_cases = {
        # Subsystem 1: Public
        "uc_browse":    ("Browse College Website", 46.5, 84.5, 12.5, 1.8),
        "uc_chat":      ("Query Chatbot (Campus Info)", 46.5, 79.5, 13.5, 1.8),
        "uc_dept":      ("View Departments & Intake", 46.5, 74.5, 13.0, 1.8),
        "uc_fees":      ("View Fee Structure & Quota", 46.5, 69.5, 13.0, 1.8),

        # Subsystem 2: Auth
        "uc_register":  ("Register User Account", 80.5, 84.5, 12.5, 1.8),
        "uc_login":     ("Login / Logout (Flask-Login)", 80.5, 79.5, 13.0, 1.8),
        "uc_profile":   ("View / Manage Profile", 80.5, 74.5, 12.0, 1.8),
        "uc_feedback":  ("Submit Chat Feedback (+/-)", 80.5, 69.5, 13.5, 1.8),

        # Subsystem 3: Academic / Dept
        "uc_curriculum":("Query Curriculum & Syllabi", 46.5, 58.5, 13.0, 1.8),
        "uc_faculty":   ("View Faculty Profiles & R&D", 46.5, 53.5, 13.5, 1.8),
        "uc_dept_dash": ("View Department Dashboard", 46.5, 48.5, 13.5, 1.8),
        "uc_notices":   ("Manage Department Notices", 46.5, 43.5, 13.5, 1.8),
        "uc_placements":("View Placement Records & Drives", 46.5, 38.5, 13.8, 1.8),

        # Subsystem 4: Admin & KG
        "uc_admin_dash":  ("View Admin Dashboard", 80.5, 59.0, 12.5, 1.8),
        "uc_manage_users":("Approve / Reject Registrations", 80.5, 53.0, 14.0, 1.8),
        "uc_kg_curate":   ("Curate KG Entities & Relations", 80.5, 47.0, 14.0, 1.8),
        "uc_kg_stats":    ("View KG Statistics & Metrics", 80.5, 41.0, 13.5, 1.8),
        "uc_kg_ingest":   ("Ingest Notices to Knowledge Graph", 80.5, 35.0, 14.2, 1.8),
        "uc_chat_logs":   ("Audit Chat Logs & Response Times", 80.5, 29.0, 14.2, 1.8),
        "uc_analytics":   ("View Intent Usage Analytics", 80.5, 23.0, 13.5, 1.8),
        "uc_er_schema":   ("Export Knowledge Graph ER Schema", 80.5, 17.0, 14.2, 1.8),
        "uc_d3_export":   ("Export Graph for D3 Visualization", 80.5, 11.0, 14.2, 1.8),
    }

    # Render Use Case Ovals
    uc_endpoints = {}
    for ucid, (label, cx, cy, rx, ry) in use_cases.items():
        ellipse = patches.Ellipse((cx, cy), rx*2, ry*2, edgecolor='#2C5282', facecolor='#FFFFFF', linewidth=1.6, zorder=4)
        ax.add_patch(ellipse)
        ax.text(cx, cy, label, fontsize=8.5, ha='center', va='center', color='#1A202C', fontweight='bold', zorder=5)
        # Store attachment points (left edge, right edge, center)
        uc_endpoints[ucid] = {
            "left": (cx - rx, cy),
            "right": (cx + rx, cy),
            "top": (cx, cy + ry),
            "bottom": (cx, cy - ry),
            "center": (cx, cy)
        }

    # Draw Stick Figures for Actors
    def draw_actor(x, y, name, subtitle):
        # Head
        head = patches.Circle((x, y + 2.8), 1.3, edgecolor='#1A365D', facecolor='#EDF2F7', linewidth=2.2, zorder=6)
        ax.add_patch(head)
        # Torso
        ax.plot([x, x], [y + 1.5, y - 1.8], color='#1A365D', linewidth=2.5, zorder=6)
        # Arms
        ax.plot([x - 2.2, x + 2.2], [y + 0.6, y + 0.6], color='#1A365D', linewidth=2.5, zorder=6)
        # Legs
        ax.plot([x, x - 2.0], [y - 1.8, y - 4.6], color='#1A365D', linewidth=2.5, zorder=6)
        ax.plot([x, x + 2.0], [y - 1.8, y - 4.6], color='#1A365D', linewidth=2.5, zorder=6)
        # Labels
        ax.text(x, y - 6.0, name, fontsize=10.5, fontweight='bold', ha='center', va='center', color='#1A365D', zorder=7)
        ax.text(x, y - 7.6, subtitle, fontsize=8, fontstyle='italic', ha='center', va='center', color='#4A5568', zorder=7)
        return (x + 2.3, y) # Output attachment anchor

    actors = {
        "visitor": (10, 84, "Visitor / Public", "Prospective Student / Parent"),
        "student": (10, 68, "Student", "Enrolled & Approved Learner"),
        "faculty": (10, 50, "Faculty", "Teaching & Research Staff"),
        "hod":     (10, 33, "HOD", "Head of Academic Department"),
        "admin":   (10, 14, "Administrator", "System & Knowledge Base Superuser")
    }

    actor_anchors = {}
    for aid, (ax_pos, ay_pos, aname, asub) in actors.items():
        actor_anchors[aid] = draw_actor(ax_pos, ay_pos, aname, asub)

    # Connections Matrix (Every Actor -> Specified Use Case)
    connections = [
        # 1. Visitor (Public inquiries)
        ("visitor", "uc_browse", "#4A5568"),
        ("visitor", "uc_chat", "#4A5568"),
        ("visitor", "uc_dept", "#4A5568"),
        ("visitor", "uc_fees", "#4A5568"),
        ("visitor", "uc_register", "#4A5568"),

        # 2. Student (Authenticated Learner)
        ("student", "uc_login", "#2B6CB0"),
        ("student", "uc_profile", "#2B6CB0"),
        ("student", "uc_chat", "#2B6CB0"),
        ("student", "uc_feedback", "#2B6CB0"),
        ("student", "uc_curriculum", "#2B6CB0"),
        ("student", "uc_faculty", "#2B6CB0"),

        # 3. Faculty (Academic Staff)
        ("faculty", "uc_login", "#2C7A7B"),
        ("faculty", "uc_profile", "#2C7A7B"),
        ("faculty", "uc_curriculum", "#2C7A7B"),
        ("faculty", "uc_dept_dash", "#2C7A7B"),
        ("faculty", "uc_notices", "#2C7A7B"),

        # 4. HOD (Department Head)
        ("hod", "uc_login", "#D69E2E"),
        ("hod", "uc_dept_dash", "#D69E2E"),
        ("hod", "uc_notices", "#D69E2E"),
        ("hod", "uc_placements", "#D69E2E"),
        ("hod", "uc_curriculum", "#D69E2E"),

        # 5. Admin (System & KG Master)
        ("admin", "uc_login", "#C53030"),
        ("admin", "uc_admin_dash", "#C53030"),
        ("admin", "uc_manage_users", "#C53030"),
        ("admin", "uc_kg_curate", "#C53030"),
        ("admin", "uc_kg_stats", "#C53030"),
        ("admin", "uc_kg_ingest", "#C53030"),
        ("admin", "uc_chat_logs", "#C53030"),
        ("admin", "uc_analytics", "#C53030"),
        ("admin", "uc_er_schema", "#C53030"),
        ("admin", "uc_d3_export", "#C53030"),
    ]

    # Draw precise connection lines
    for aid, ucid, color in connections:
        src = actor_anchors[aid]
        # Choose the closest attachment point on the oval
        dst = uc_endpoints[ucid]["left"]
        
        # Draw solid communication line
        ax.plot([src[0], dst[0]], [src[1], dst[1]], color=color, linewidth=1.5, alpha=0.85, zorder=3)

    # Actor Legend
    legend = patches.FancyBboxPatch((2, 0.8), 24, 6.0, boxstyle="round,pad=0.3,rounding_size=0.5",
                                    edgecolor='#CBD5E0', facecolor='#F7FAFC', linewidth=1, zorder=3)
    ax.add_patch(legend)
    ax.text(14, 5.5, "Actor Associations Legend", fontsize=8.5, fontweight='bold', ha='center', va='center', color='#2D3748')
    
    ax.plot([3, 6], [4.1, 4.1], color='#4A5568', lw=2)
    ax.text(6.8, 4.1, "Visitor", fontsize=8, va='center', color='#4A5568', fontweight='semibold')
    
    ax.plot([3, 6], [2.8, 2.8], color='#2B6CB0', lw=2)
    ax.text(6.8, 2.8, "Student", fontsize=8, va='center', color='#2B6CB0', fontweight='semibold')
    
    ax.plot([3, 6], [1.5, 1.5], color='#2C7A7B', lw=2)
    ax.text(6.8, 1.5, "Faculty", fontsize=8, va='center', color='#2C7A7B', fontweight='semibold')
    
    ax.plot([14, 17], [4.1, 4.1], color='#D69E2E', lw=2)
    ax.text(17.8, 4.1, "HOD", fontsize=8, va='center', color='#D69E2E', fontweight='semibold')
    
    ax.plot([14, 17], [2.8, 2.8], color='#C53030', lw=2)
    ax.text(17.8, 2.8, "Admin", fontsize=8, va='center', color='#C53030', fontweight='semibold')

    plt.tight_layout()
    out_path = "c:/Users/lucky/JC-Rella Su-6372/major project/uml_diagrams/use_case_diagram.jpg"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Use case diagram generated successfully at:", out_path)

if __name__ == "__main__":
    generate_use_case_diagram()

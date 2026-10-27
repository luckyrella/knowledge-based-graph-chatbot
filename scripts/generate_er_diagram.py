import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_er_diagram():
    fig, ax = plt.subplots(figsize=(22, 17), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # Title
    ax.text(50, 98.2, "ENTITY-RELATIONSHIP (ER) DIAGRAM: KNOWLEDGE GRAPH ONTOLOGY",
            fontsize=16, fontweight='bold', ha='center', va='center', color='#1A365D')
    ax.text(50, 96.2, "Sphoorthy Engineering College Knowledge Domain — 29 Entity Types & 28 Validated Relationship Types",
            fontsize=11, fontstyle='italic', ha='center', va='center', color='#4A5568')

    # Draw Entity Rectangle
    def draw_entity(x, y, w, h, name, attrs, color="#EBF8FF", border="#2B6CB0"):
        # Header
        head_h = 2.0
        head = patches.Rectangle((x - w/2, y + h/2 - head_h), w, head_h, facecolor=border, edgecolor='#1A202C', linewidth=1.5, zorder=3)
        ax.add_patch(head)
        ax.text(x, y + h/2 - head_h/2, name, fontsize=9.5, fontweight='bold', ha='center', va='center', color='#FFFFFF', zorder=4)

        # Body
        body = patches.Rectangle((x - w/2, y - h/2), w, h - head_h, facecolor=color, edgecolor='#1A202C', linewidth=1.5, zorder=2)
        ax.add_patch(body)

        curr_y = y + h/2 - head_h - 1.1
        for attr in attrs:
            ax.text(x - w/2 + 0.5, curr_y, attr, fontsize=7.5, va='center', color='#1A202C', fontfamily='monospace', zorder=4)
            curr_y -= 1.1

        return {
            "top": (x, y + h/2),
            "bottom": (x, y - h/2),
            "left": (x - w/2, y),
            "right": (x + w/2, y),
            "center": (x, y)
        }

    # Draw Relationship Diamond
    def draw_diamond(x, y, name, size=2.6, color="#FEFCBF", border="#D69E2E"):
        diamond = patches.RegularPolygon((x, y), numVertices=4, radius=size, orientation=0,
                                         facecolor=color, edgecolor=border, linewidth=1.5, zorder=3)
        ax.add_patch(diamond)
        ax.text(x, y, name, fontsize=7.5, fontweight='bold', ha='center', va='center', color='#744210', zorder=4)
        return (x, y)

    # ── Level 1: Root College Node ─────────────────────────────────────────────
    e_college = draw_entity(50, 86, 22, 14, "COLLEGE", [
        "name: String [PK]",
        "code: 'SPHN'",
        "established: 2004",
        "affiliation: JNTUH",
        "accreditation: NAAC A+",
        "autonomous: True",
        "campus_area: '12 Acres'"
    ], color="#EBF8FF", border="#2B6CB0")

    # ── Level 2: Primary Subsystems Connected to College ─────────────────────
    e_mgmt = draw_entity(12, 86, 17, 10, "MANAGEMENT", [
        "chairman: String",
        "principal: String",
        "director: String",
        "secretary: String"
    ], color="#EDF2F7", border="#4A5568")

    e_dept = draw_entity(50, 64, 21, 13, "DEPARTMENT", [
        "id: String [PK] (cse, ece..)",
        "name: String",
        "short: String",
        "hod: String",
        "intake: Integer"
    ], color="#EBF8FF", border="#2B6CB0")

    e_bld = draw_entity(16, 64, 18, 12, "BUILDING", [
        "id: String [PK]",
        "name: String",
        "type: String",
        "floors: Integer",
        "departments: List"
    ], color="#FEFCBF", border="#D69E2E")

    e_course = draw_entity(85, 86, 18, 11, "COURSE", [
        "name: String [PK]",
        "duration: '4 Years'",
        "level: 'UG' / 'PG'",
        "total_intake: Integer",
        "eligibility: String"
    ], color="#EDFDFD", border="#319795")

    e_place = draw_entity(85, 64, 19, 12, "PLACEMENT", [
        "highest_package: '12 LPA'",
        "average_package: '4.5 LPA'",
        "students_placed: Integer",
        "job_offers: Integer"
    ], color="#FAF5FF", border="#6B46C1")

    # ── Level 3: Academic & Facility Entities ────────────────────────────────
    e_room = draw_entity(16, 42, 18, 11, "ROOM", [
        "id: String [PK]",
        "name: String",
        "building_id: String [FK]",
        "type: Class/Lab/Hall",
        "capacity: Integer"
    ], color="#FEFCBF", border="#D69E2E")

    e_lab = draw_entity(16, 22, 18, 10, "LAB", [
        "name: String [PK]",
        "equipment: Text",
        "capacity: Integer",
        "description: Text"
    ], color="#FEFCBF", border="#D69E2E")

    e_faculty = draw_entity(40, 42, 20, 12, "FACULTY", [
        "name: String [PK]",
        "department_id: String [FK]",
        "designation: String",
        "qualification: String",
        "experience: String"
    ], color="#EBF8FF", border="#2B6CB0")

    e_prog = draw_entity(63, 42, 19, 11, "PROGRAM", [
        "code: String [PK]",
        "name: String",
        "duration: '4 Years'",
        "department_id: [FK]"
    ], color="#EDFDFD", border="#319795")

    e_recruiter = draw_entity(85, 42, 18, 9, "RECRUITER", [
        "name: String [PK]",
        "package_offered: Float",
        "sector: String"
    ], color="#FAF5FF", border="#6B46C1")

    # ── Level 4: Curriculum & Research ───────────────────────────────────────
    e_subj = draw_entity(40, 20, 20, 13, "SUBJECT", [
        "code: String [PK]",
        "name: String",
        "credits: Integer",
        "semester: Integer",
        "type: Theory/Lab",
        "department_id: [FK]"
    ], color="#EBF8FF", border="#2B6CB0")

    e_sem = draw_entity(63, 20, 19, 10, "SEMESTER", [
        "number: Integer [PK]",
        "name: 'Semester 3'",
        "year: Integer"
    ], color="#EDFDFD", border="#319795")

    e_res = draw_entity(40, 5, 20, 8, "RESEARCH_AREA", [
        "name: String [PK]",
        "domain: String"
    ], color="#E6FFFA", border="#319795")

    # ── Relationships (Connecting with Lines & Diamonds) ─────────────────────
    def link_entities(e1, e2, rel_name, c1="1", c2="N", diam_color="#FEFCBF", diam_border="#D69E2E"):
        # Midpoint for diamond
        mx = (e1[0] + e2[0]) / 2
        my = (e1[1] + e2[1]) / 2
        draw_diamond(mx, my, rel_name, color=diam_color, border=diam_border)
        # Line from e1 to diamond
        ax.plot([e1[0], mx], [e1[1], my], color="#2D3748", lw=1.3, zorder=2)
        # Line from diamond to e2
        ax.plot([mx, e2[0]], [my, e2[1]], color="#2D3748", lw=1.3, zorder=2)
        # Cardinalities
        ax.text(e1[0] + 0.8, e1[1] + 0.6, c1, fontsize=8.5, fontweight='bold', color='#1A365D')
        ax.text(e2[0] - 0.8, e2[1] + 0.6, c2, fontsize=8.5, fontweight='bold', color='#1A365D')

    # College Connections
    link_entities(e_college["left"], e_mgmt["right"], "has_mgmt", "1", "1")
    link_entities(e_college["bottom"], e_dept["top"], "has_dept", "1", "N")
    link_entities(e_college["right"], e_course["left"], "offers", "1", "N")
    link_entities((e_college["bottom"][0] - 5, e_college["bottom"][1]), e_bld["top"], "has_bld", "1", "N")
    link_entities((e_college["bottom"][0] + 5, e_college["bottom"][1]), e_place["top"], "has_stats", "1", "1")

    # Department Connections
    link_entities(e_dept["left"], e_bld["right"], "housed_in", "N", "1")
    link_entities((e_dept["bottom"][0] - 4, e_dept["bottom"][1]), e_faculty["top"], "has_staff", "1", "N")
    link_entities((e_dept["bottom"][0] + 4, e_dept["bottom"][1]), e_prog["top"], "offers", "1", "N")

    # Infrastructure Hierarchy
    link_entities(e_bld["bottom"], e_room["top"], "has_room", "1", "N")
    link_entities(e_room["bottom"], e_lab["top"], "lab_in", "1", "1")

    # Faculty & Curriculum
    link_entities(e_faculty["bottom"], e_subj["top"], "teaches", "N", "M")
    link_entities(e_prog["bottom"], e_sem["top"], "has_sem", "1", "N")
    link_entities(e_subj["right"], e_sem["left"], "offered_in", "N", "1")
    link_entities(e_subj["left"], e_lab["right"], "uses_lab", "N", "1")
    link_entities(e_faculty["left"], (e_res["left"][0], e_res["left"][1] + 4), "researches", "N", "M", diam_color="#E6FFFA", diam_border="#319795")

    # Placements
    link_entities(e_place["bottom"], e_recruiter["top"], "has_recruiter", "1", "N")

    plt.tight_layout()
    out_path = "c:/Users/lucky/JC-Rella Su-6372/major project/uml_diagrams/er_diagram.jpg"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("ER diagram generated successfully at:", out_path)

if __name__ == "__main__":
    generate_er_diagram()

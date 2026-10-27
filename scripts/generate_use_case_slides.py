import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_actor(ax, x, y, name, subtitle):
    # Head
    head = patches.Circle((x, y + 2.8), 1.3, edgecolor='black', facecolor='white', linewidth=1.5, zorder=6)
    ax.add_patch(head)
    # Torso
    ax.plot([x, x], [y + 1.5, y - 1.8], color='black', linewidth=1.5, zorder=6)
    # Arms
    ax.plot([x - 2.2, x + 2.2], [y + 0.6, y + 0.6], color='black', linewidth=1.5, zorder=6)
    # Legs
    ax.plot([x, x - 2.0], [y - 1.8, y - 4.6], color='black', linewidth=1.5, zorder=6)
    ax.plot([x, x + 2.0], [y - 1.8, y - 4.6], color='black', linewidth=1.5, zorder=6)
    # Labels
    ax.text(x, y - 6.0, name, fontsize=11, fontweight='normal', ha='center', va='center', color='black', zorder=7)
    return (x + 2.5, y)

def draw_use_case(ax, cx, cy, rx, ry, label):
    ellipse = patches.Ellipse((cx, cy), rx*2, ry*2, edgecolor='black', facecolor='white', linewidth=1.5, zorder=4)
    ax.add_patch(ellipse)
    ax.text(cx, cy, label, fontsize=9, ha='center', va='center', color='black', fontweight='normal', zorder=5)
    return (cx - rx, cy)

def generate_slide_1():
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Title
    ax.text(50, 97, "Use Case Diagram - Slide 1 (Public & Student)", fontsize=16, fontweight='bold', ha='center', color='black')
    
    # Subsystem Boxes
    rect1 = patches.Rectangle((35, 52), 60, 42, linewidth=1.5, edgecolor='black', facecolor='none', zorder=1)
    ax.add_patch(rect1)
    ax.text(65, 91, "Public Campus Information", fontsize=11, fontweight='bold', ha='center', color='black', zorder=2)

    rect2 = patches.Rectangle((35, 2), 60, 46, linewidth=1.5, edgecolor='black', facecolor='none', zorder=1)
    ax.add_patch(rect2)
    ax.text(65, 45, "Student Authenticated Services", fontsize=11, fontweight='bold', ha='center', color='black', zorder=2)

    # Actors
    anchor_visitor = draw_actor(ax, 15, 73, "Visitor / Public", "")
    anchor_student = draw_actor(ax, 15, 25, "Student", "")

    # Use Cases - Public (Single Column)
    uc_visitor = [
        draw_use_case(ax, 65, 85, 18, 2.5, "Browse College Website"),
        draw_use_case(ax, 65, 79, 18, 2.5, "Query Chatbot (Campus Info)"),
        draw_use_case(ax, 65, 73, 18, 2.5, "View Departments & Intake"),
        draw_use_case(ax, 65, 67, 18, 2.5, "View Fee Structure & Quota"),
        draw_use_case(ax, 65, 61, 18, 2.5, "View Facilities & Contact"),
        draw_use_case(ax, 65, 55, 18, 2.5, "Register User Account")
    ]
    
    for dst in uc_visitor:
        ax.plot([anchor_visitor[0], dst[0]], [anchor_visitor[1], dst[1]], color='black', linewidth=1.2, zorder=2)

    # Use Cases - Student (Single Column)
    uc_student = [
        draw_use_case(ax, 65, 39, 18, 2.5, "Login / Logout"),
        draw_use_case(ax, 65, 33, 18, 2.5, "Query Chatbot (Specifics)"),
        draw_use_case(ax, 65, 27, 18, 2.5, "View Own Profile"),
        draw_use_case(ax, 65, 21, 18, 2.5, "Submit Chat Feedback"),
        draw_use_case(ax, 65, 15, 18, 2.5, "View Course & Notes Hub"),
        draw_use_case(ax, 65, 9, 18, 2.5, "View Circulars & Notices")
    ]

    for dst in uc_student:
        ax.plot([anchor_student[0], dst[0]], [anchor_student[1], dst[1]], color='black', linewidth=1.2, zorder=2)
        
    out_path = "c:/Users/lucky/JC-Rella Su-6372/major project/uml_diagrams/use_case_slide1_bw_vertical.jpg"
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def generate_slide_2():
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    ax.text(50, 97, "Use Case Diagram - Slide 2 (Faculty, HOD & Admin)", fontsize=16, fontweight='bold', ha='center', color='black')
    
    # Subsystems
    rect1 = patches.Rectangle((35, 54), 60, 38, linewidth=1.5, edgecolor='black', facecolor='none', zorder=1)
    ax.add_patch(rect1)
    ax.text(65, 89, "Academic & Department Services", fontsize=11, fontweight='bold', ha='center', color='black', zorder=2)

    rect2 = patches.Rectangle((35, 5), 60, 45, linewidth=1.5, edgecolor='black', facecolor='none', zorder=1)
    ax.add_patch(rect2)
    ax.text(65, 47, "System Administration & KG Sync", fontsize=11, fontweight='bold', ha='center', color='black', zorder=2)

    # Actors
    anchor_faculty = draw_actor(ax, 15, 82, "Faculty", "")
    anchor_hod = draw_actor(ax, 15, 62, "HOD", "")
    anchor_admin = draw_actor(ax, 15, 25, "Administrator", "")

    # Use Cases - Faculty & HOD
    uc_shared = draw_use_case(ax, 65, 84, 18, 2.5, "Login / Update Profile")
    uc_faculty1 = draw_use_case(ax, 65, 78, 18, 2.5, "Upload Study Materials")
    uc_faculty2 = draw_use_case(ax, 65, 72, 18, 2.5, "Post Department Notices")
    uc_hod1 = draw_use_case(ax, 65, 66, 18, 2.5, "View Dept Dashboard")
    uc_hod2 = draw_use_case(ax, 65, 60, 18, 2.5, "Manage Placements")

    # Faculty edges
    for dst in [uc_shared, uc_faculty1, uc_faculty2]:
        ax.plot([anchor_faculty[0], dst[0]], [anchor_faculty[1], dst[1]], color='black', linewidth=1.2, zorder=2)
    
    # HOD edges
    for dst in [uc_shared, uc_faculty2, uc_hod1, uc_hod2]:
        ax.plot([anchor_hod[0], dst[0]], [anchor_hod[1], dst[1]], color='black', linewidth=1.2, zorder=2)
    
    # Use Cases - Admin
    uc_admin = [
        draw_use_case(ax, 65, 41, 18, 2.5, "Approve/Reject Users"),
        draw_use_case(ax, 65, 35, 18, 2.5, "Manage KG Entities"),
        draw_use_case(ax, 65, 29, 18, 2.5, "Dynamic Graph Sync"),
        draw_use_case(ax, 65, 23, 18, 2.5, "Audit Chat Logs"),
        draw_use_case(ax, 65, 17, 18, 2.5, "View System Analytics"),
        draw_use_case(ax, 65, 11, 18, 2.5, "Manage Roles & Access")
    ]

    for dst in uc_admin:
        ax.plot([anchor_admin[0], dst[0]], [anchor_admin[1], dst[1]], color='black', linewidth=1.2, zorder=2)
        
    out_path = "c:/Users/lucky/JC-Rella Su-6372/major project/uml_diagrams/use_case_slide2_bw_vertical.jpg"
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

if __name__ == "__main__":
    generate_slide_1()
    generate_slide_2()

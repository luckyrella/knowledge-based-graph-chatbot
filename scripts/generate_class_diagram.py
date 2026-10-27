import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_class_diagram():
    fig, ax = plt.subplots(figsize=(22, 16), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # Title
    ax.text(50, 98, "UML CLASS DIAGRAM: KG-RAG CAMPUS KNOWLEDGE MANAGEMENT SYSTEM",
            fontsize=16, fontweight='bold', ha='center', va='center', color='#1A365D')
    ax.text(50, 96, "Comprehensive Architecture: Database Models (SQLAlchemy ORM) + Knowledge Graph & NLP Engines",
            fontsize=11, fontstyle='italic', ha='center', va='center', color='#4A5568')

    def draw_uml_class(x, y, w, h, class_name, attributes, methods, header_color="#2B6CB0", header_text="#FFFFFF"):
        # Header box
        header_h = 2.2
        header = patches.Rectangle((x, y + h - header_h), w, header_h, facecolor=header_color, edgecolor='#2D3748', linewidth=1.5, zorder=3)
        ax.add_patch(header)
        ax.text(x + w/2, y + h - header_h/2, class_name, fontsize=9.5, fontweight='bold', ha='center', va='center', color=header_text, zorder=4)

        # Body box
        body = patches.Rectangle((x, y), w, h - header_h, facecolor='#FFFFFF', edgecolor='#2D3748', linewidth=1.5, zorder=2)
        ax.add_patch(body)

        # Calculate split between attributes and methods
        attr_h = (len(attributes) + 0.5) * 1.3
        
        # Attributes
        curr_y = y + h - header_h - 1.2
        for attr in attributes:
            ax.text(x + 0.6, curr_y, attr, fontsize=7.5, va='center', color='#1A202C', fontfamily='monospace', zorder=4)
            curr_y -= 1.2

        # Divider line
        divider_y = y + h - header_h - attr_h
        if methods:
            ax.plot([x, x + w], [divider_y, divider_y], color='#CBD5E0', linewidth=1.2, zorder=3)
            # Methods
            curr_y = divider_y - 1.2
            for m in methods:
                ax.text(x + 0.6, curr_y, m, fontsize=7.5, va='center', color='#2C5282', fontfamily='monospace', zorder=4)
                curr_y -= 1.2

        return {"top": (x + w/2, y + h), "bottom": (x + w/2, y), "left": (x, y + h/2), "right": (x + w, y + h/2)}

    # Classes definition
    # Row 1: Users & Core Entities
    c_user = draw_uml_class(4, 70, 20, 23, "User (UserMixin, db.Model)", [
        "+ id: Integer [PK]",
        "+ username: String(64) [Unique]",
        "+ email: String(120) [Unique]",
        "+ password_hash: String(256)",
        "+ role: String(32)",
        "+ department: String(128)",
        "+ is_active: Boolean",
        "+ is_approved: Boolean",
        "+ created_at: DateTime"
    ], [
        "+ set_password(pwd: str): void",
        "+ check_password(pwd: str): bool",
        "+ has_role(role_name: str): bool"
    ], header_color="#2B6CB0")

    c_chat = draw_uml_class(27, 72, 21, 21, "ChatMessage (db.Model)", [
        "+ id: Integer [PK]",
        "+ session_id: String(128)",
        "+ user_message: Text",
        "+ bot_response: Text",
        "+ intent: String(64)",
        "+ entities: Text (JSON)",
        "+ response_time_ms: Integer",
        "+ created_at: DateTime"
    ], [
        "+ __repr__(): str"
    ], header_color="#2B6CB0")

    c_fb = draw_uml_class(51, 74, 19, 19, "Feedback (db.Model)", [
        "+ id: Integer [PK]",
        "+ chat_message_id: Integer [FK]",
        "+ rating: String(16)",
        "+ comment: Text",
        "+ created_at: DateTime"
    ], [
        "+ __repr__(): str"
    ], header_color="#2B6CB0")

    c_notice = draw_uml_class(73, 73, 23, 20, "Notice (db.Model)", [
        "+ id: Integer [PK]",
        "+ title: String(256)",
        "+ content: Text",
        "+ department: String(128)",
        "+ author_id: Integer [FK]",
        "+ is_approved: Boolean",
        "+ is_ingested_to_kg: Boolean",
        "+ created_at: DateTime",
        "+ updated_at: DateTime"
    ], [], header_color="#2B6CB0")

    # Row 2: KG Persistence & Placements
    c_entity = draw_uml_class(4, 40, 20, 21, "KGEntity (db.Model)", [
        "+ id: Integer [PK]",
        "+ entity_type: String(64)",
        "+ name: String(128)",
        "+ data: Text (JSON)",
        "+ created_by: Integer [FK]",
        "+ created_at: DateTime",
        "+ updated_at: DateTime"
    ], [
        "+ __repr__(): str"
    ], header_color="#2C7A7B")

    c_rel = draw_uml_class(27, 40, 21, 21, "KGRelationship (db.Model)", [
        "+ id: Integer [PK]",
        "+ source_entity_id: Integer [FK]",
        "+ target_entity_id: Integer [FK]",
        "+ relationship_type: String(64)",
        "+ weight: Float",
        "+ metadata_: Text (JSON)",
        "+ created_at: DateTime"
    ], [
        "+ __repr__(): str"
    ], header_color="#2C7A7B")

    c_place = draw_uml_class(51, 42, 19, 19, "PlacementRecord (db.Model)", [
        "+ id: Integer [PK]",
        "+ company_name: String(128)",
        "+ package_lpa: Float",
        "+ department: String(128)",
        "+ year: Integer",
        "+ students_placed: Integer",
        "+ drive_date: DateTime",
        "+ created_by: Integer [FK]"
    ], [], header_color="#2B6CB0")

    # Row 3: Intelligence & KG Engine Classes
    c_builder = draw_uml_class(4, 5, 29, 27, "KnowledgeGraphBuilder", [
        "- college_data_path: str",
        "- faculty_data_path: str",
        "- graph: nx.DiGraph",
        "- _subject_code_map: dict"
    ], [
        "+ load_data(): dict",
        "+ build_graph(): DiGraph",
        "+ _build_departments(): dict",
        "+ _build_curriculum(): void",
        "+ _build_campus_infrastructure(): void",
        "+ _build_faculty(): dict",
        "+ get_graph(): DiGraph",
        "+ get_graph_stats(): dict",
        "+ export_for_visualization(): str",
        "+ get_er_diagram(): str"
    ], header_color="#4C51BF")

    c_query = draw_uml_class(36, 5, 30, 27, "KnowledgeGraphQuery", [
        "- graph: nx.DiGraph"
    ], [
        "+ query_department(dept: str): str",
        "+ query_course(course: str): str",
        "+ query_fees(course, dept): str",
        "+ query_admission(course): str",
        "+ query_placements(): str",
        "+ query_facilities(): str",
        "+ query_building(building: str): str",
        "+ query_faculty_profile(name: str): str",
        "+ query_subjects_by_department(): str",
        "+ query_subjects_by_semester(): str",
        "+ search_general(query: str): str"
    ], header_color="#4C51BF")

    c_nlp = draw_uml_class(69, 5, 27, 27, "NLPProcessor", [
        "- intent_examples: dict",
        "- vectorizer: TfidfVectorizer",
        "- tfidf_matrix: csr_matrix",
        "- dept_mapping: dict",
        "- _keyword_rules: list"
    ], [
        "+ classify_intent(text, ctx): str",
        "+ extract_entities(text, ctx): dict",
        "+ process(text, context): dict"
    ], header_color="#7B341E")

    # Draw Relationship Connectors
    # 1. ChatMessage --< Feedback (1 to *)
    ax.annotate("", xy=c_fb["left"], xytext=c_chat["right"],
                arrowprops=dict(arrowstyle="->", color="#2D3748", lw=1.8))
    ax.text(c_chat["right"][0] + 0.5, c_chat["right"][1] + 0.8, "1", fontsize=9, fontweight='bold')
    ax.text(c_fb["left"][0] - 1.2, c_fb["left"][1] + 0.8, "*", fontsize=10, fontweight='bold')

    # 2. User --> KGEntity (1 to *)
    ax.annotate("", xy=c_entity["top"], xytext=c_user["bottom"],
                arrowprops=dict(arrowstyle="->", color="#2D3748", lw=1.8))
    ax.text(c_user["bottom"][0] + 0.6, c_user["bottom"][1] - 1.5, "1", fontsize=9, fontweight='bold')
    ax.text(c_entity["top"][0] + 0.6, c_entity["top"][1] + 0.5, "*", fontsize=10, fontweight='bold')

    # 3. User --> Notice (1 to *)
    ax.annotate("", xy=(c_notice["bottom"][0] - 8, c_notice["bottom"][1]), xytext=(c_user["right"][0], c_user["right"][1] - 4),
                arrowprops=dict(arrowstyle="->", color="#2D3748", lw=1.5, connectionstyle="arc3,rad=-0.15"))
    ax.text(c_notice["bottom"][0] - 7, c_notice["bottom"][1] - 2, "* (authors)", fontsize=8, color='#4A5568')

    # 4. KGEntity --< KGRelationship (Source & Target 1 to *)
    ax.annotate("", xy=c_rel["left"], xytext=c_entity["right"],
                arrowprops=dict(arrowstyle="->", color="#2D3748", lw=1.8))
    ax.text(c_entity["right"][0] + 0.6, c_entity["right"][1] + 0.8, "1", fontsize=9, fontweight='bold')
    ax.text(c_rel["left"][0] - 1.2, c_rel["left"][1] + 0.8, "* (source/target)", fontsize=8, fontweight='bold')

    # 5. User --> PlacementRecord
    ax.annotate("", xy=c_place["left"], xytext=c_user["right"],
                arrowprops=dict(arrowstyle="->", color="#2D3748", lw=1.5, connectionstyle="arc3,rad=0.15"))

    # 6. Builder --> Query (provides graph)
    ax.annotate("", xy=c_query["left"], xytext=c_builder["right"],
                arrowprops=dict(arrowstyle="->", color="#4C51BF", lw=2, linestyle='--'))
    ax.text((c_builder["right"][0] + c_query["left"][0])/2, c_builder["right"][1] + 0.8, "provides graph", fontsize=8.5, color='#4C51BF', fontweight='bold', ha='center')

    # 7. NLP --> Query (routes intent)
    ax.annotate("", xy=c_query["right"], xytext=c_nlp["left"],
                arrowprops=dict(arrowstyle="->", color="#7B341E", lw=2, linestyle='--'))
    ax.text((c_query["right"][0] + c_nlp["left"][0])/2, c_query["right"][1] + 0.8, "routes query", fontsize=8.5, color='#7B341E', fontweight='bold', ha='center')

    plt.tight_layout()
    out_path = "c:/Users/lucky/JC-Rella Su-6372/major project/uml_diagrams/class_diagram.jpg"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Class diagram generated successfully at:", out_path)

if __name__ == "__main__":
    generate_class_diagram()

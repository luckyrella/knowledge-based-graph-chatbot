"""
Knowledge Graph Builder
Loads college_data.json and builds a NetworkX DiGraph with
entities (nodes) and relationships (edges).
"""
import json
import networkx as nx


class KnowledgeGraphBuilder:
    def __init__(self, data_path):
        self.data_path = data_path
        self.graph = nx.DiGraph()
        self._raw_data = None

    def load_data(self):
        with open(self.data_path, 'r', encoding='utf-8') as f:
            self._raw_data = json.load(f)
        return self._raw_data

    def _safe_add_node(self, node_id, node_type, data_dict):
        """Add a node safely, storing all JSON data under 'data' key to avoid
        conflicts with NetworkX reserved keyword arguments like 'type'."""
        self.graph.add_node(node_id, node_type=node_type, data=data_dict)

    def build_graph(self):
        data = self.load_data()

        # --- College (root node) ---
        college = data.get("college", {})
        self._safe_add_node("college", "College", college)

        # --- Management ---
        management = data.get("management", {})
        self._safe_add_node("management", "Management", management)
        self.graph.add_edge("college", "management", relationship="has_management")

        # --- Departments ---
        for dept in data.get("departments", []):
            node_id = f"dept_{dept['id']}"
            self._safe_add_node(node_id, "Department", dept)
            self.graph.add_edge("college", node_id, relationship="has_department")

            # HOD sub-node
            hod_node = f"hod_{dept['id']}"
            self._safe_add_node(hod_node, "HOD", {"name": dept.get("hod", "N/A"), "department": dept["name"]})
            self.graph.add_edge(node_id, hod_node, relationship="has_hod")

        # --- Courses ---
        for i, course in enumerate(data.get("courses", [])):
            node_id = f"course_{i}"
            self._safe_add_node(node_id, "Course", course)
            self.graph.add_edge("college", node_id, relationship="offers_course")

        # --- Fees ---
        self._safe_add_node("fees", "Fee", data.get("fees", {}))
        self.graph.add_edge("college", "fees", relationship="has_fee")

        # --- Admissions ---
        self._safe_add_node("admissions", "Admission", data.get("admissions", {}))
        self.graph.add_edge("college", "admissions", relationship="has_admission")

        # --- Facilities ---
        for i, fac in enumerate(data.get("facilities", [])):
            node_id = f"facility_{i}"
            self._safe_add_node(node_id, "Facility", fac)
            self.graph.add_edge("college", node_id, relationship="has_facility")

        # --- Placements ---
        placements = data.get("placements", {})
        self._safe_add_node("placements", "Placement", placements)
        self.graph.add_edge("college", "placements", relationship="has_placement")
        for recruiter in placements.get("top_recruiters", []):
            rec_id = f"recruiter_{recruiter.replace(' ', '_')}"
            self._safe_add_node(rec_id, "Recruiter", {"name": recruiter})
            self.graph.add_edge("placements", rec_id, relationship="has_recruiter")

        # --- Scholarships ---
        for i, schol in enumerate(data.get("scholarships", [])):
            node_id = f"scholarship_{i}"
            self._safe_add_node(node_id, "Scholarship", schol)
            self.graph.add_edge("college", node_id, relationship="has_scholarship")

        # --- Events ---
        for i, event in enumerate(data.get("events", [])):
            node_id = f"event_{i}"
            self._safe_add_node(node_id, "Event", event)
            self.graph.add_edge("college", node_id, relationship="has_event")

        # --- Clubs ---
        for i, club in enumerate(data.get("clubs", [])):
            node_id = f"club_{i}"
            self._safe_add_node(node_id, "Club", {"name": club})
            self.graph.add_edge("college", node_id, relationship="has_club")

        # --- Academic System ---
        self._safe_add_node("academic_system", "AcademicSystem", data.get("academic_system", {}))
        self.graph.add_edge("college", "academic_system", relationship="has_academic_system")

        return self.graph

    def get_graph(self):
        return self.graph

    def get_node_data(self, node_id):
        """Return the 'data' dict stored on a node."""
        if self.graph.has_node(node_id):
            return self.graph.nodes[node_id].get("data", {})
        return {}

    def get_node_type(self, node_id):
        if self.graph.has_node(node_id):
            return self.graph.nodes[node_id].get("node_type", "Unknown")
        return None

    def get_neighbors(self, node_id, edge_type=None):
        if not self.graph.has_node(node_id):
            return []
        result = []
        for neighbor in self.graph.successors(node_id):
            rel = self.graph.edges[node_id, neighbor].get("relationship")
            if edge_type is None or rel == edge_type:
                result.append((neighbor, self.graph.nodes[neighbor]))
        return result

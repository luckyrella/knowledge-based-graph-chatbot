import json
import networkx as nx
import os
import re
from .ontology import validate_node, validate_edge
from .er_schema import export_er_diagram


class KnowledgeGraphBuilder:
    def __init__(self, data_path, faculty_data_path=None):
        self.college_data_path = data_path
        self.faculty_data_path = faculty_data_path
        if not self.faculty_data_path:
            # Default fallback for backward compatibility
            self.faculty_data_path = os.path.join(os.path.dirname(self.college_data_path), 'faculty_data.json')
        self.graph = nx.DiGraph()
        self._college_data = None
        self._faculty_data = None
        # Subject code → node_id mapping for faculty assignment lookups
        self._subject_code_map = {}

    def load_data(self):
        with open(self.college_data_path, 'r', encoding='utf-8') as f:
            self._college_data = json.load(f)
            
        if os.path.exists(self.faculty_data_path):
            with open(self.faculty_data_path, 'r', encoding='utf-8') as f:
                self._faculty_data = json.load(f)
        else:
            self._faculty_data = {"faculty": {}}
            
        return self._college_data

    def _safe_add_node(self, node_id, node_type, data_dict):
        """Add a node safely with validation."""
        is_valid, msg = validate_node(node_type, data_dict)
        if not is_valid:
            print(f"Warning: Node validation failed for {node_id} ({node_type}): {msg}")
            
        self.graph.add_node(node_id, node_type=node_type, data=data_dict)

    def _safe_add_edge(self, source_id, target_id, relationship):
        """Add an edge safely with validation."""
        if not self.graph.has_node(source_id) or not self.graph.has_node(target_id):
            return
            
        source_type = self.graph.nodes[source_id].get("node_type")
        target_type = self.graph.nodes[target_id].get("node_type")
        
        is_valid, msg = validate_edge(relationship, source_type, target_type)
        if not is_valid:
             print(f"Warning: Edge validation failed: {msg}")
             
        self.graph.add_edge(source_id, target_id, relationship=relationship)

    # ── Build methods ─────────────────────────────────────────────────────────

    def _build_college(self, c_data):
        """Build the root College node."""
        college = c_data.get("college", {})
        self._safe_add_node("college", "College", college)

    def _build_management(self, c_data):
        """Build management node and link to college."""
        management = c_data.get("management", {})
        self._safe_add_node("management", "Management", management)
        self._safe_add_edge("college", "management", "has_management")

    def _build_departments(self, c_data):
        """Build department nodes with HODs. Returns dept_id_map."""
        dept_id_map = {}
        for dept in c_data.get("departments", []):
            node_id = f"dept_{dept['id']}"
            dept_id_map[dept['id']] = node_id
            self._safe_add_node(node_id, "Department", dept)
            self._safe_add_edge("college", node_id, "has_department")

            # HOD sub-node
            hod_node = f"hod_{dept['id']}"
            self._safe_add_node(hod_node, "HOD", {"name": dept.get("hod", "N/A"), "department": dept["name"]})
            self._safe_add_edge(node_id, hod_node, "has_hod")
        return dept_id_map

    def _build_campus_infrastructure(self, c_data, dept_id_map):
        """Build Building → Room hierarchy and link departments to buildings."""
        for building in c_data.get("campus_infrastructure", []):
            bld_id = f"building_{building['id']}"
            self._safe_add_node(bld_id, "Building", building)
            self._safe_add_edge("college", bld_id, "has_building")

            # Link departments to this building
            for dept_key in building.get("departments", []):
                dept_node = f"dept_{dept_key}"
                if dept_node in self.graph:
                    self._safe_add_edge(dept_node, bld_id, "housed_in")

            # Build rooms
            for room in building.get("rooms", []):
                room_data = room.copy()
                room_data["building_id"] = building["id"]
                room_id = f"room_{room['id']}"
                self._safe_add_node(room_id, "Room", room_data)
                self._safe_add_edge(bld_id, room_id, "has_room")

                # If room is a lab, also create a Lab node and link
                if room.get("type") == "Lab":
                    lab_id = f"lab_{room['id']}"
                    lab_data = {"name": room["name"], "capacity": room.get("capacity"), "description": f"Located in {building['name']}"}
                    self._safe_add_node(lab_id, "Lab", lab_data)
                    self._safe_add_edge(lab_id, room_id, "lab_in")

                    # Link lab to department(s) of the building
                    for dept_key in building.get("departments", []):
                        dept_node = f"dept_{dept_key}"
                        if dept_node in self.graph:
                            self._safe_add_edge(dept_node, lab_id, "has_lab")

    def _build_curriculum(self, c_data, dept_id_map):
        """Build Program → Semester → Subject hierarchy from curriculum data."""
        curriculum = c_data.get("curriculum", {})
        for dept_key, dept_curriculum in curriculum.items():
            dept_node = f"dept_{dept_key}"
            program_name = dept_curriculum.get("program", "B.Tech")

            # Program node
            prog_id = f"program_{dept_key}"
            self._safe_add_node(prog_id, "Program", {
                "name": f"{program_name} - {dept_key.upper()}",
                "code": f"{program_name}_{dept_key}",
                "department_id": dept_key
            })
            if dept_node in self.graph:
                self._safe_add_edge(dept_node, prog_id, "has_program")

            # Semesters and subjects
            for sem_num, subjects in dept_curriculum.get("semesters", {}).items():
                sem_id = f"sem_{dept_key}_{sem_num}"
                self._safe_add_node(sem_id, "Semester", {
                    "name": f"Semester {sem_num}",
                    "number": int(sem_num)
                })
                self._safe_add_edge(prog_id, sem_id, "has_semester")

                for subj in subjects:
                    subj_id = f"subj_{subj['code']}"
                    subj_data = {
                        "name": subj["name"],
                        "code": subj["code"],
                        "credits": subj.get("credits"),
                        "type": subj.get("type", "theory"),
                        "department_id": dept_key,
                        "semester": int(sem_num)
                    }
                    # Avoid duplicate nodes (same code may exist across depts)
                    if not self.graph.has_node(subj_id):
                        self._safe_add_node(subj_id, "Subject", subj_data)
                    if dept_node in self.graph:
                        self._safe_add_edge(dept_node, subj_id, "offers_subject")
                    self._safe_add_edge(subj_id, sem_id, "offered_in")

                    # Track code → node_id for faculty assignment
                    self._subject_code_map[subj["code"]] = subj_id

                    # If it's a lab subject, try to link to a corresponding lab room
                    if subj.get("type") == "lab":
                        for n in self.graph.nodes():
                            if (self.graph.nodes[n].get("node_type") == "Lab"
                                    and subj["name"].lower().split()[0] in self.graph.nodes[n].get("data", {}).get("name", "").lower()):
                                self._safe_add_edge(subj_id, n, "uses_lab")
                                break

    def _build_faculty(self, f_data, dept_id_map):
        """Build faculty nodes and link to departments. Returns faculty name→id map."""
        fac_key_to_dept = {
            'computer_science_and_engineering': 'cse',
            'cse_aiml': 'cse_aiml',
            'cse_data_science': 'cse_ds',
            'cse_cyber_security': 'cse_cs',
            'electronics_and_communications': 'ece',
            'civil_engineering': 'ce',
            'mechanical_engineering': 'me',
            'mba': 'mba',
            'freshman_engineering': 'fe'
        }

        faculty_name_map = {}  # name → node_id
        faculty_info = f_data.get("faculty", {})
        for fac_key, fac_details in faculty_info.items():
            dept_id = fac_key_to_dept.get(fac_key, fac_key)
            dept_node = f"dept_{dept_id}"
            
            for staff in fac_details.get("staff", []):
                fac_id = f"fac_{id(staff)}"
                staff_data = staff.copy()
                staff_data["department_id"] = dept_id
                self._safe_add_node(fac_id, "Faculty", staff_data)
                faculty_name_map[staff["name"]] = fac_id
                
                if dept_node in self.graph:
                    self._safe_add_edge(fac_id, dept_node, "belongs_to")
                    self._safe_add_edge(dept_node, fac_id, "has_faculty")
                    
                # Extract ResearchArea from qualifications
                qual = staff.get("qualification") or ""
                if "Ph.D" in qual:
                    match = re.search(r'Ph\.D\.?\s*\((.*?)\)', qual)
                    if match:
                        ra_name = match.group(1).strip()
                        ra_id = f"ra_{hash(ra_name)}"
                        if not self.graph.has_node(ra_id):
                            self._safe_add_node(ra_id, "ResearchArea", {"name": ra_name})
                        self._safe_add_edge(fac_id, ra_id, "researches")

        return faculty_name_map

    def _build_faculty_assignments(self, c_data, faculty_name_map):
        """Link faculty to subjects using explicit assignment data."""
        assignments = c_data.get("faculty_assignments", {})
        for dept_key, dept_assignments in assignments.items():
            for assignment in dept_assignments:
                fac_name = assignment.get("faculty", "")
                fac_id = faculty_name_map.get(fac_name)
                if not fac_id:
                    continue
                for subj_code in assignment.get("subjects", []):
                    subj_id = self._subject_code_map.get(subj_code)
                    if subj_id and fac_id:
                        self._safe_add_edge(fac_id, subj_id, "teaches")

    def _build_courses(self, c_data):
        """Build course nodes."""
        for i, course in enumerate(c_data.get("courses", [])):
            node_id = f"course_{i}"
            self._safe_add_node(node_id, "Course", course)
            self._safe_add_edge("college", node_id, "offers_course")

    def _build_fees(self, c_data):
        """Build fee node."""
        self._safe_add_node("fees", "Fee", c_data.get("fees", {}))
        self._safe_add_edge("college", "fees", "has_fee")

    def _build_admissions(self, c_data):
        """Build admission node."""
        self._safe_add_node("admissions", "Admission", c_data.get("admissions", {}))
        self._safe_add_edge("college", "admissions", "has_admission")

    def _build_facilities(self, c_data):
        """Build facility nodes (general campus facilities)."""
        for i, fac in enumerate(c_data.get("facilities", [])):
            node_id = f"facility_{i}"
            self._safe_add_node(node_id, "Facility", fac)
            self._safe_add_edge("college", node_id, "has_facility")

    def _build_placements(self, c_data, dept_id_map):
        """Build placement and recruiter nodes."""
        placements = c_data.get("placements", {})
        self._safe_add_node("placements", "Placement", placements)
        self._safe_add_edge("college", "placements", "has_placement")
        
        for recruiter in placements.get("top_recruiters", []):
            rec_id = f"recruiter_{recruiter.replace(' ', '_')}"
            self._safe_add_node(rec_id, "Recruiter", {"name": recruiter})
            self._safe_add_edge("placements", rec_id, "has_recruiter")

    def _build_scholarships(self, c_data):
        """Build scholarship nodes."""
        for i, schol in enumerate(c_data.get("scholarships", [])):
            node_id = f"scholarship_{i}"
            self._safe_add_node(node_id, "Scholarship", schol)
            self._safe_add_edge("college", node_id, "has_scholarship")

    def _build_events(self, c_data):
        """Build event nodes."""
        for i, event in enumerate(c_data.get("events", [])):
            node_id = f"event_{i}"
            self._safe_add_node(node_id, "Event", event)
            self._safe_add_edge("college", node_id, "has_event")

    def _build_clubs(self, c_data):
        """Build club nodes."""
        for i, club in enumerate(c_data.get("clubs", [])):
            node_id = f"club_{i}"
            self._safe_add_node(node_id, "Club", {"name": club})
            self._safe_add_edge("college", node_id, "has_club")

    def _build_academic_system(self, c_data):
        """Build academic system node."""
        self._safe_add_node("academic_system", "AcademicSystem", c_data.get("academic_system", {}))
        self._safe_add_edge("college", "academic_system", "has_academic_system")

    # ── Main build orchestrator ───────────────────────────────────────────────

    def build_graph(self):
        """Build the complete knowledge graph from data files."""
        self.load_data()
        c_data = self._college_data
        f_data = self._faculty_data

        # 1. Root nodes
        self._build_college(c_data)
        self._build_management(c_data)

        # 2. Departments
        dept_id_map = self._build_departments(c_data)

        # 3. Campus infrastructure (Buildings → Rooms → Labs)
        self._build_campus_infrastructure(c_data, dept_id_map)

        # 4. Curriculum (Programs → Semesters → Subjects)
        self._build_curriculum(c_data, dept_id_map)

        # 5. Faculty
        faculty_name_map = self._build_faculty(f_data, dept_id_map)

        # 6. Faculty ↔ Subject assignments (data-driven, no pseudo-random)
        self._build_faculty_assignments(c_data, faculty_name_map)

        # 7. Courses, Fees, Admissions
        self._build_courses(c_data)
        self._build_fees(c_data)
        self._build_admissions(c_data)

        # 8. Facilities, Placements, Scholarships, Events, Clubs
        self._build_facilities(c_data)
        self._build_placements(c_data, dept_id_map)
        self._build_scholarships(c_data)
        self._build_events(c_data)
        self._build_clubs(c_data)
        self._build_academic_system(c_data)

        return self.graph

    # ── Public API ────────────────────────────────────────────────────────────

    def get_graph(self):
        return self.graph

    def get_node_data(self, node_id):
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
        
    def get_graph_stats(self):
        """Returns node and edge counts by type."""
        stats = {
            "nodes": {},
            "edges": {},
            "total_nodes": self.graph.number_of_nodes(),
            "total_edges": self.graph.number_of_edges()
        }
        
        for n, data in self.graph.nodes(data=True):
            ntype = data.get("node_type", "Unknown")
            stats["nodes"][ntype] = stats["nodes"].get(ntype, 0) + 1
            
        for u, v, data in self.graph.edges(data=True):
            etype = data.get("relationship", "Unknown")
            stats["edges"][etype] = stats["edges"].get(etype, 0) + 1
            
        return stats

    def export_for_visualization(self):
        """Returns nodes and edges as JSON for D3.js visualization."""
        nodes = []
        for n, data in self.graph.nodes(data=True):
            nodes.append({
                "id": str(n),
                "label": data.get("data", {}).get("name", str(n)),
                "group": data.get("node_type", "Unknown"),
                "data": data.get("data", {})
            })
            
        edges = []
        for u, v, data in self.graph.edges(data=True):
            edges.append({
                "source": str(u),
                "target": str(v),
                "label": data.get("relationship", ""),
                "relationship": data.get("relationship", "")
            })
            
        return json.dumps({"nodes": nodes, "links": edges}, indent=2)

    def get_er_diagram(self):
        """Returns the ER diagram string in Mermaid format."""
        return export_er_diagram()

"""
Neo4j Graph Database Service for KG-RAG Campus Assistant
Provides persistent graph storage, Cypher query execution,
and automated synchronization from institutional datasets.
"""
import os
import json
import logging
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger(__name__)

try:
    from neo4j import GraphDatabase, Driver
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False
    GraphDatabase = None
    Driver = None


# Visual styling map for Vis.js graph rendering
NODE_COLOR_MAP = {
    "College": {"background": "#059669", "border": "#047857", "highlight": "#10b981"},      # Emerald
    "Department": {"background": "#8b5cf6", "border": "#7c3aed", "highlight": "#a78bfa"},   # Violet
    "Course": {"background": "#f59e0b", "border": "#d97706", "highlight": "#fbbf24"},       # Amber
    "Faculty": {"background": "#0284c7", "border": "#0369a1", "highlight": "#38bdf8"},      # Sky Blue
    "Subject": {"background": "#10b981", "border": "#059669", "highlight": "#34d399"},      # Green
    "Building": {"background": "#ea580c", "border": "#c2410c", "highlight": "#fb923c"},     # Orange
    "Room": {"background": "#64748b", "border": "#475569", "highlight": "#94a3b8"},         # Slate
    "Lab": {"background": "#06b6d4", "border": "#0891b2", "highlight": "#22d3ee"},          # Cyan
    "Club": {"background": "#ec4899", "border": "#db2777", "highlight": "#f472b6"},         # Pink
    "Event": {"background": "#e11d48", "border": "#be123c", "highlight": "#fb7185"},        # Rose
    "Recruiter": {"background": "#6366f1", "border": "#4f46e5", "highlight": "#818cf8"}     # Indigo
}

NODE_SIZE_MAP = {
    "College": 38,
    "Department": 26,
    "Building": 22,
    "Course": 20,
    "Faculty": 16,
    "Recruiter": 16,
    "Club": 15,
    "Event": 15,
    "Lab": 13,
    "Subject": 11,
    "Room": 10
}



class Neo4jService:
    """Manages connections, Cypher queries, and data ingestion with Neo4j."""

    def __init__(self, uri: Optional[str] = None, user: Optional[str] = None,
                 password: Optional[str] = None, database: str = "neo4j"):
        self.uri = uri or os.environ.get("NEO4J_URI")
        self.user = user or os.environ.get("NEO4J_USERNAME", "neo4j")
        self.password = password or os.environ.get("NEO4J_PASSWORD")
        self.database = database or os.environ.get("NEO4J_DATABASE", "neo4j")
        self.driver: Optional[Driver] = None
        self.is_connected = False

        if NEO4J_AVAILABLE and self.uri and self.password:
            self._connect()
        else:
            if not self.uri:
                logger.info("Neo4j URI not configured. Operating in fallback mode (NetworkX).")
            elif not NEO4J_AVAILABLE:
                logger.warning("neo4j Python package not installed.")

    def _connect(self):
        """Establish connection to Neo4j instance."""
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            self.driver.verify_connectivity()
            self.is_connected = True
            logger.info("Successfully connected to Neo4j Graph Database at %s", self.uri)
        except Exception as e:
            self.is_connected = False
            self.driver = None
            logger.warning("Could not connect to Neo4j: %s. Using local fallback.", e)

    def close(self):
        """Close driver connection."""
        if self.driver:
            self.driver.close()
            self.is_connected = False

    def execute_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Run a Cypher query and return list of record dicts."""
        if not self.is_connected or not self.driver:
            return []
        try:
            with self.driver.session(database=self.database) as session:
                result = session.run(query, parameters or {})
                return [record.data() for record in result]
        except Exception as e:
            logger.error("Neo4j query error: %s | Query: %s", e, query)
            return []

    # ── Schema and Constraints ────────────────────────────────────────────────

    def init_constraints(self):
        """Create uniqueness constraints on primary node IDs."""
        if not self.is_connected:
            return False

        constraints = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:College) REQUIRE c.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (d:Department) REQUIRE d.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (f:Faculty) REQUIRE f.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (s:Subject) REQUIRE s.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Course) REQUIRE c.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (b:Building) REQUIRE b.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (r:Room) REQUIRE r.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (l:Lab) REQUIRE l.id IS UNIQUE",
        ]
        try:
            with self.driver.session(database=self.database) as session:
                for c in constraints:
                    session.run(c)
            return True
        except Exception as e:
            logger.error("Error creating Neo4j constraints: %s", e)
            return False

    # ── Ingestion from JSON ───────────────────────────────────────────────────

    def sync_from_json(self, college_data_path: str, faculty_data_path: Optional[str] = None) -> Dict[str, int]:
        """
        Synchronize the complete college & faculty JSON dataset into Neo4j.
        Returns node and edge count statistics.
        """
        if not self.is_connected:
            return {"status": "error", "message": "Neo4j is not connected", "nodes": 0, "edges": 0}

        self.init_constraints()

        with open(college_data_path, "r", encoding="utf-8") as f:
            c_data = json.load(f)

        f_data = {"faculty": {}}
        if faculty_data_path and os.path.exists(faculty_data_path):
            with open(faculty_data_path, "r", encoding="utf-8") as f:
                f_data = json.load(f)

        stats = {"nodes": 0, "edges": 0}

        with self.driver.session(database=self.database) as session:
            # 1. Root College Node
            c_info = c_data.get("college", {})
            c_id = c_info.get("id", "sphoorthy_engg")
            session.run("""
                MERGE (c:College {id: $id})
                SET c.name = $name,
                    c.code = $code,
                    c.type = $type,
                    c.affiliation = $affiliation,
                    c.approval = $approval,
                    c.accreditation = $accreditation,
                    c.established = $established,
                    c.location = $location
            """, {
                "id": c_id,
                "name": c_info.get("name", "Sphoorthy Engineering College"),
                "code": c_info.get("code", "SPHN"),
                "type": c_info.get("type", "Autonomous"),
                "affiliation": c_info.get("affiliation", "JNTUH"),
                "approval": c_info.get("approval", "AICTE"),
                "accreditation": c_info.get("accreditation", "NAAC A+"),
                "established": c_info.get("established", 2004),
                "location": c_info.get("location", "Hyderabad, Telangana")
            })

            # 2. Departments & Courses
            for d in c_data.get("departments", []):
                dept_id = d.get("id")
                session.run("""
                    MERGE (dept:Department {id: $id})
                    SET dept.name = $name,
                        dept.short = $short,
                        dept.intake = $intake,
                        dept.hod = $hod,
                        dept.established = $est,
                        dept.description = $desc
                    WITH dept
                    MATCH (c:College {id: $college_id})
                    MERGE (c)-[:HAS_DEPARTMENT]->(dept)
                """, {
                    "id": dept_id,
                    "name": d.get("name"),
                    "short": d.get("short"),
                    "intake": d.get("intake"),
                    "hod": d.get("hod"),
                    "est": d.get("established"),
                    "desc": d.get("description", ""),
                    "college_id": c_id
                })

            for c in c_data.get("courses", []):
                session.run("""
                    MERGE (course:Course {id: $id})
                    SET course.name = $name,
                        course.level = $level,
                        course.duration = $duration,
                        course.eligibility = $eligibility
                    WITH course
                    MATCH (c:College {id: $college_id})
                    MERGE (c)-[:OFFERS_COURSE]->(course)
                """, {
                    "id": c.get("id"),
                    "name": c.get("name"),
                    "level": c.get("level"),
                    "duration": c.get("duration"),
                    "eligibility": c.get("eligibility", ""),
                    "college_id": c_id
                })

            # Ensure Freshman Engineering (Humanities & Sciences) Department exists
            session.run("""
                MERGE (dept:Department {id: 'fe'})
                SET dept.name = 'Freshman Engineering (Humanities & Sciences)',
                    dept.short = 'FE',
                    dept.intake = 1200,
                    dept.hod = 'Dr. P. Gayathri Pavani',
                    dept.description = 'Humanities & Sciences department catering to 1st year B.Tech students.'
                WITH dept
                MATCH (c:College {id: $college_id})
                MERGE (c)-[:HAS_DEPARTMENT]->(dept)
            """, {"college_id": c_id})

            # 3. Faculty Members (from faculty_data.json and college_data.json)

            faculty_map = f_data.get("faculty", {})
            for dept_code, f_list in faculty_map.items():
                for f_item in f_list:
                    f_name = f_item.get("name")
                    f_id = f"fac_{dept_code}_{f_name.lower().replace(' ', '_').replace('.', '')}"
                    session.run("""
                        MERGE (fac:Faculty {id: $id})
                        SET fac.name = $name,
                            fac.designation = $designation,
                            fac.qualification = $qualification,
                            fac.experience = $experience,
                            fac.department = $dept
                        WITH fac
                        MATCH (dept:Department)
                        WHERE toLower(dept.id) = toLower($dept) or toLower(dept.short) = toLower($dept)
                        MERGE (fac)-[:BELONGS_TO]->(dept)
                    """, {
                        "id": f_id,
                        "name": f_name,
                        "designation": f_item.get("designation", "Faculty"),
                        "qualification": f_item.get("qualification", "M.Tech"),
                        "experience": f_item.get("experience", ""),
                        "dept": dept_code
                    })

            # 4. Campus Infrastructure: Buildings, Rooms, Labs
            infra = c_data.get("campus_infrastructure", {})
            for b in infra.get("buildings", []):
                b_id = b.get("id")
                session.run("""
                    MERGE (bld:Building {id: $id})
                    SET bld.name = $name,
                        bld.floors = $floors,
                        bld.type = $type,
                        bld.description = $desc
                    WITH bld
                    MATCH (c:College {id: $college_id})
                    MERGE (c)-[:HAS_BUILDING]->(bld)
                """, {
                    "id": b_id,
                    "name": b.get("name"),
                    "floors": b.get("floors"),
                    "type": b.get("type"),
                    "desc": b.get("description", ""),
                    "college_id": c_id
                })

                # Connect departments to buildings
                for dept_assigned in b.get("departments", []):
                    session.run("""
                        MATCH (bld:Building {id: $b_id})
                        MATCH (dept:Department)
                        WHERE toLower(dept.id) = toLower($d) or toLower(dept.short) = toLower($d)
                        MERGE (dept)-[:HOUSED_IN]->(bld)
                    """, {"b_id": b_id, "d": dept_assigned})

                # Rooms
                for r in b.get("rooms", []):
                    r_id = f"room_{b_id}_{r.get('number', r.get('name', '')).replace(' ', '_')}"
                    session.run("""
                        MERGE (rm:Room {id: $id})
                        SET rm.name = $name,
                            rm.number = $number,
                            rm.floor = $floor,
                            rm.type = $type,
                            rm.capacity = $capacity
                        WITH rm
                        MATCH (bld:Building {id: $b_id})
                        MERGE (bld)-[:HAS_ROOM]->(rm)
                    """, {
                        "id": r_id,
                        "name": r.get("name", "Room"),
                        "number": r.get("number", ""),
                        "floor": r.get("floor", 0),
                        "type": r.get("type", "Classroom"),
                        "capacity": r.get("capacity", 60),
                        "b_id": b_id
                    })

            # 5. Recruiters & Placements
            placements = c_data.get("placements", {})
            for recruiter in placements.get("top_recruiters", []):
                r_name = recruiter.get("name") if isinstance(recruiter, dict) else str(recruiter)
                r_id = f"rec_{r_name.lower().replace(' ', '_')}"
                session.run("""
                    MERGE (rec:Recruiter {id: $id})
                    SET rec.name = $name
                    WITH rec
                    MATCH (c:College {id: $college_id})
                    MERGE (rec)-[:HIRES_FROM]->(c)
                """, {"id": r_id, "name": r_name, "college_id": c_id})

            # Count total nodes and relationships
            n_count = session.run("MATCH (n) RETURN count(n) AS c").single()["c"]
            r_count = session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
            stats = {"nodes": n_count, "edges": r_count, "status": "success"}

        return stats

    # ── Live Admin Mutations (Real-time updates) ─────────────────────────────

    def add_entity(self, entity_type: str, name: str, data: Optional[Dict[str, Any]] = None) -> bool:
        """Add or update an entity node directly in Neo4j."""
        if not self.is_connected:
            return False
        try:
            node_id = f"{entity_type.lower()}_{name.lower().replace(' ', '_')}"
            clean_type = "".join(c for c in entity_type if c.isalnum())
            query = f"""
                MERGE (n:{clean_type} {{id: $id}})
                SET n.name = $name, n += $data
                RETURN n
            """
            with self.driver.session(database=self.database) as session:
                session.run(query, {"id": node_id, "name": name, "data": data or {}})
            return True
        except Exception as e:
            logger.error("Failed to add entity to Neo4j: %s", e)
            return False

    def add_relationship(self, source_name: str, target_name: str, rel_type: str) -> bool:
        """Connect two entities by relationship type in Neo4j."""
        if not self.is_connected:
            return False
        try:
            clean_rel = "".join(c for c in rel_type if c.isalnum() or c == "_").upper()
            query = f"""
                MATCH (a), (b)
                WHERE (toLower(a.name) = toLower($src) OR toLower(a.id) = toLower($src))
                  AND (toLower(b.name) = toLower($tgt) OR toLower(b.id) = toLower($tgt))
                MERGE (a)-[r:{clean_rel}]->(b)
                RETURN r
            """
            with self.driver.session(database=self.database) as session:
                result = session.run(query, {"src": source_name, "tgt": target_name})
                return result.single() is not None
        except Exception as e:
            logger.error("Failed to add relationship in Neo4j: %s", e)
            return False

    # ── Web Visualization (Vis.js / Neo4j Bloom Format) ──────────────────────

    def get_graph_visual_data(self, fallback_nx_graph=None, limit: int = 350) -> Dict[str, Any]:
        """
        Export graph data for Vis.js interactive network viewer.
        Queries live Neo4j if connected; falls back to NetworkX graph otherwise.
        """
        nodes = []
        edges = []
        seen_nodes = set()

        if self.is_connected and self.driver:
            try:
                cypher = f"""
                    MATCH (n)-[r]->(m)
                    RETURN n, labels(n)[0] AS n_type, type(r) AS rel_type, m, labels(m)[0] AS m_type
                    LIMIT {int(limit)}
                """
                with self.driver.session(database=self.database) as session:
                    records = session.run(cypher)
                    edge_id = 0
                    for rec in records:
                        n = rec["n"]
                        m = rec["m"]
                        n_type = rec["n_type"] or "Entity"
                        m_type = rec["m_type"] or "Entity"
                        rel = rec["rel_type"]

                        n_id = str(n.get("id", n.get("name", id(n))))
                        m_id = str(m.get("id", m.get("name", id(m))))

                        if n_id not in seen_nodes:
                            seen_nodes.add(n_id)
                            colors = NODE_COLOR_MAP.get(n_type, {"background": "#64748b", "border": "#475569", "highlight": "#94a3b8"})
                            n_name = n.get("name", n_id)
                            nodes.append({
                                "id": n_id,
                                "label": n_name,
                                "group": n_type,
                                "color": colors,
                                "title": f"<b>{n_name}</b> <span style='opacity:0.8;'>({n_type})</span><br><span style='color:#38bdf8;font-size:10px;'>Click node for full details</span>"
                            })

                        if m_id not in seen_nodes:
                            seen_nodes.add(m_id)
                            colors = NODE_COLOR_MAP.get(m_type, {"background": "#64748b", "border": "#475569", "highlight": "#94a3b8"})
                            m_name = m.get("name", m_id)
                            nodes.append({
                                "id": m_id,
                                "label": m_name,
                                "group": m_type,
                                "color": colors,
                                "title": f"<b>{m_name}</b> <span style='opacity:0.8;'>({m_type})</span><br><span style='color:#38bdf8;font-size:10px;'>Click node for full details</span>"
                            })

                        edges.append({
                            "id": f"e_{edge_id}",
                            "from": n_id,
                            "to": m_id,
                            "label": rel,
                            "arrows": "to",
                            "font": {"size": 9, "align": "middle"}
                        })
                        edge_id += 1

                return {
                    "source": "neo4j",
                    "nodes": nodes,
                    "edges": edges,
                    "total_nodes": len(nodes),
                    "total_edges": len(edges)
                }
            except Exception as e:
                logger.error("Error querying Neo4j visual data: %s", e)

        # Fallback to in-memory NetworkX graph if Neo4j is not connected
        if fallback_nx_graph is not None:
            edge_id = 0
            for node_id, data in fallback_nx_graph.nodes(data=True):
                n_type = data.get("node_type", "Entity")
                name = data.get("data", {}).get("name", str(node_id))
                colors = NODE_COLOR_MAP.get(n_type, {"background": "#64748b", "border": "#475569", "highlight": "#94a3b8"})
                size = NODE_SIZE_MAP.get(n_type, 14)

                # Format label: major hubs get full bold labels; leaf nodes get clean concise labels
                is_hub = n_type in ["College", "Department", "Building", "Course"]
                if is_hub:
                    display_label = name
                    font_cfg = {"size": 13, "face": "Inter, sans-serif"}
                elif n_type in ["Faculty", "Recruiter"]:
                    display_label = name if len(name) <= 18 else name[:16] + ".."
                    font_cfg = {"size": 11, "face": "Inter, sans-serif"}
                else:
                    # Subjects, rooms, labs: clean concise labels to prevent overlap
                    display_label = name if len(name) <= 14 else name[:12] + ".."
                    font_cfg = {"size": 9, "face": "Inter, sans-serif"}

                # Build clean, elegant tooltip
                ndata = data.get("data", {})
                extras = []
                if "hod" in ndata and ndata["hod"]:
                    extras.append(f"HOD: {ndata['hod']}")
                elif "designation" in ndata and ndata["designation"]:
                    extras.append(str(ndata["designation"]))
                elif "department" in ndata and ndata["department"]:
                    extras.append(f"Dept: {str(ndata['department']).upper()}")
                elif "code" in ndata and ndata["code"]:
                    extras.append(f"Code: {ndata['code']}")
                elif "intake" in ndata and ndata["intake"]:
                    extras.append(f"Intake: {ndata['intake']}")

                sub_str = f"<br><span style='color:#94a3b8;font-size:11px;'>{' • '.join(extras)}</span>" if extras else ""
                clean_tooltip = f"<b>{name}</b> <span style='opacity:0.8;'>({n_type})</span>{sub_str}<br><span style='color:#38bdf8;font-size:10px;'>Click node for full details</span>"

                nodes.append({
                    "id": str(node_id),
                    "label": display_label,
                    "full_name": name,
                    "group": n_type,
                    "size": size,
                    "color": colors,
                    "font": font_cfg,
                    "title": clean_tooltip
                })

            for u, v, edata in fallback_nx_graph.edges(data=True):
                rel = edata.get("relationship", "RELATED_TO")
                edges.append({
                    "id": f"e_{edge_id}",
                    "from": str(u),
                    "to": str(v),
                    "label": rel,
                    "arrows": "to",
                    "font": {"size": 9, "align": "middle"}
                })
                edge_id += 1

            return {
                "source": "networkx_fallback",
                "nodes": nodes,
                "edges": edges,
                "total_nodes": len(nodes),
                "total_edges": len(edges)
            }


        return {"source": "none", "nodes": [], "edges": [], "total_nodes": 0, "total_edges": 0}

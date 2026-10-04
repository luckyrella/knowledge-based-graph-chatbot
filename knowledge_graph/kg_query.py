"""
Knowledge Graph Query Engine
Traverses the NetworkX DiGraph to answer user questions about the college.
All node data is stored under node['data'] dict.
"""


class KnowledgeGraphQuery:
    def __init__(self, graph):
        self.graph = graph

    def _d(self, node_id):
        """Shorthand: get the 'data' dict for a node."""
        if self.graph.has_node(node_id):
            return self.graph.nodes[node_id].get('data', {})
        return {}

    def _get_nodes_by_type(self, node_type):
        """Return list of (node_id, data_dict) for all nodes of a given type."""
        return [
            (n, attrs.get('data', {}))
            for n, attrs in self.graph.nodes(data=True)
            if attrs.get('node_type') == node_type
        ]

    # ── Department queries ────────────────────────────────────────────────────

    def query_department(self, dept_name):
        dept_name_lower = dept_name.lower()
        for node_id, d in self._get_nodes_by_type('Department'):
            if (dept_name_lower in d.get('name', '').lower()
                    or dept_name_lower in d.get('short', '').lower()
                    or dept_name_lower == d.get('id', '').lower()):
                resp = f"**{d.get('name')} ({d.get('short')})**\n"
                resp += f"HOD: {d.get('hod', 'N/A')} | Intake: {d.get('intake', 'N/A')} seats\n"
                resp += f"{d.get('description', '')}"
                return resp
        return ("I couldn't find information about that department. "
                "Available departments: CSE, CSE (AI & ML), CSE (Data Science), "
                "CSE (Cyber Security), ECE, Civil Engineering, Mechanical Engineering, MBA.")

    # ── Course queries ────────────────────────────────────────────────────────

    def query_course(self, course_name):
        course_lower = course_name.lower()
        for node_id, d in self._get_nodes_by_type('Course'):
            if course_lower in d.get('name', '').lower():
                resp = f"**{d.get('name')}** — {d.get('duration', 'N/A')}, {d.get('level', 'N/A')}\n"
                if 'total_intake' in d:
                    resp += f"Intake: {d['total_intake']} seats\n"
                if 'eligibility' in d:
                    resp += f"Eligibility: {d['eligibility']}"
                return resp
        return "I couldn't find information about that course. We offer B.Tech, M.Tech, and MBA."

    # ── Fee queries ───────────────────────────────────────────────────────────

    def query_fees(self, course_or_dept=None, dept_name=None):
        fd = self._d('fees')
        if not fd:
            return "Fee information is currently unavailable."

        btech = fd.get('btech', {})
        mtech = fd.get('mtech', {})
        mba   = fd.get('mba', {})

        # B.Tech departments → infer B.Tech fee context
        btech_depts = {'cse', 'cse_aiml', 'cse_ds', 'cse_cs', 'ece', 'ce', 'me'}

        if course_or_dept:
            c = course_or_dept.lower()
            if 'btech' in c or 'b.tech' in c or 'b tech' in c:
                return (f"**B.Tech Fees:**\n"
                        f"• Convener: {btech.get('convener_quota', 'N/A')}\n"
                        f"• Management: {btech.get('management_quota', 'N/A')}")
            elif 'mtech' in c or 'm.tech' in c or 'm tech' in c:
                return f"**M.Tech Fee:** {mtech.get('fee', 'N/A')}"
            elif 'mba' in c:
                return f"**MBA Fee:** {mba.get('fee', 'N/A')}"

        # If a B.Tech department was mentioned (but no explicit course), default to B.Tech fees
        if dept_name and dept_name in btech_depts:
            return (f"**B.Tech Fees ({dept_name.upper()}):**\n"
                    f"• Convener: {btech.get('convener_quota', 'N/A')}\n"
                    f"• Management: {btech.get('management_quota', 'N/A')}")

        return (f"**Fee Structure:**\n"
                f"• B.Tech Convener: {btech.get('convener_quota', 'N/A')}\n"
                f"• B.Tech Management: {btech.get('management_quota', 'N/A')}\n"
                f"• M.Tech: {mtech.get('fee', 'N/A')}\n"
                f"• MBA: {mba.get('fee', 'N/A')}")

    # ── Admission queries ─────────────────────────────────────────────────────

    def query_admission(self, course=None):
        ad = self._d('admissions')
        if not ad:
            return "Admission information is currently unavailable."

        if course:
            c = course.lower()
            if 'btech' in c or 'b.tech' in c or 'b tech' in c:
                b = ad.get('btech', {})
                cq = b.get('convener_quota', {})
                mq = b.get('management_quota', {})
                le = b.get('lateral_entry', {})
                return (f"**B.Tech Admission:**\n"
                        f"• Convener ({cq.get('percentage', '70%')}): {cq.get('exam', 'TG EAPCET')} → {cq.get('process', 'State counseling')}\n"
                        f"• Management ({mq.get('percentage', '30%')}): {mq.get('process', 'Direct by college')}\n"
                        f"• Eligibility: {cq.get('eligibility', '10+2 PCM, min 45%')}")
            elif 'mtech' in c or 'm.tech' in c:
                m = ad.get('mtech', {})
                cq = m.get('convener_quota', {})
                mq = m.get('management_quota', {})
                return (f"**M.Tech Admission:** {cq.get('exam', 'TG PGECET / GATE')} | "
                        f"Management: {mq.get('process', 'Based on B.Tech aggregate')}")
            elif 'mba' in c:
                m = ad.get('mba', {})
                cq = m.get('convener_quota', {})
                return (f"**MBA Admission:** {cq.get('exam', 'TG ICET')} | "
                        f"Eligibility: {cq.get('eligibility', 'Graduation min 50%')}")

        # General overview
        return (f"**Admissions:**\n"
                f"• B.Tech: TG EAPCET (Convener 70%) or Direct (Management 30%)\n"
                f"• M.Tech: TG PGECET / GATE\n"
                f"• MBA: TG ICET")

    # ── Placement queries ─────────────────────────────────────────────────────

    def query_placements(self):
        pd = self._d('placements')
        if not pd:
            return "Placement information is currently unavailable."

        resp = f"**Placements (2024-25):**\n"
        resp += f"• Highest: {pd.get('highest_package', 'N/A')} | Avg: {pd.get('average_package', 'N/A')}\n"
        resp += f"• Placed: {pd.get('students_placed_2024_25', 'N/A')} | Offers: {pd.get('job_offers_2024_25', 'N/A')}\n"
        recruiters = pd.get('top_recruiters', [])
        if recruiters:
            resp += f"• Top Recruiters: {', '.join(recruiters[:5])}"
        return resp

    # ── Facility queries ──────────────────────────────────────────────────────

    def query_facilities(self):
        fac_nodes = self._get_nodes_by_type('Facility')
        if not fac_nodes:
            return "Facilities information is currently unavailable."

        resp = "**Campus Facilities:**\n"
        for _, d in fac_nodes:
            resp += f"• {d.get('name', 'Facility')}\n"
        return resp

    # ── Scholarship queries ───────────────────────────────────────────────────

    def query_scholarships(self):
        schol_nodes = self._get_nodes_by_type('Scholarship')
        if not schol_nodes:
            return "Scholarship information is currently unavailable."

        resp = "**Scholarships:**\n"
        for _, d in schol_nodes:
            resp += f"• {d.get('name', '')}: {d.get('description', '')[:80]}\n"
        return resp

    # ── Event queries ─────────────────────────────────────────────────────────

    def query_events(self):
        event_nodes = self._get_nodes_by_type('Event')
        if not event_nodes:
            return "Events information is currently unavailable."

        resp = "**College Events:**\n"
        for _, d in event_nodes:
            resp += f"• {d.get('name', '')} ({d.get('type', '')})\n"
        return resp

    # ── Contact queries ───────────────────────────────────────────────────────

    def query_contact(self):
        cd = self._d('college')
        if not cd:
            return "Contact information is currently unavailable."

        phones = cd.get('phone', [])
        emails = cd.get('email', [])
        resp = "**Contact:**\n"
        if phones:
            resp += f"📞 {' | '.join(phones)}\n"
        if emails:
            resp += f"📧 {emails[0]}\n"
        resp += f"📍 {cd.get('address', 'N/A')}"
        return resp

    # ── College info queries ──────────────────────────────────────────────────

    def query_college_info(self):
        cd = self._d('college')
        if not cd:
            return "College information is currently unavailable."

        resp = f"**{cd.get('name')} ({cd.get('code')})**\n"
        resp += f"Est. {cd.get('established')} | {cd.get('type')}\n"
        resp += f"{cd.get('affiliation')} | {cd.get('accreditation')}\n"
        resp += f"Campus: {cd.get('campus_area')}"
        return resp

    # ── Management queries ────────────────────────────────────────────────────

    def query_management(self):
        md = self._d('management')
        if not md:
            return "Management information is currently unavailable."

        resp = "**Management:**\n"
        roles = {
            'chairman': 'Chairman',
            'principal': 'Principal',
            'director': 'Director',
            'ceo': 'CEO'
        }
        for key, label in roles.items():
            if key in md:
                person = md[key]
                resp += f"• {label}: {person.get('name', 'N/A')}\n"
        return resp

    # ── HOD queries ───────────────────────────────────────────────────────────

    def query_hod(self, dept):
        dept_lower = dept.lower()
        for _, d in self._get_nodes_by_type('Department'):
            if (dept_lower in d.get('name', '').lower()
                    or dept_lower in d.get('short', '').lower()
                    or dept_lower == d.get('id', '').lower()):
                return (f"The Head of Department (HOD) for **{d.get('name')}** is "
                        f"**{d.get('hod', 'N/A')}**.")
        return ("I couldn't find HOD information for that department. "
                "Please specify: CSE, ECE, Civil, Mechanical, AI ML, Data Science, Cyber Security, or MBA.")

    # ── Club queries ──────────────────────────────────────────────────────────

    def query_clubs(self):
        club_nodes = self._get_nodes_by_type('Club')
        if not club_nodes:
            return "Student clubs information is currently unavailable."

        resp = "**🎭 Student Clubs at Sphoorthy:**\n\n"
        for _, d in club_nodes:
            resp += f"• {d.get('name', 'Club')}\n"
        return resp

    # ── NEW: Building / Campus Infrastructure queries ─────────────────────────

    def query_building(self, building_name):
        """Query information about a specific building or block."""
        name_lower = building_name.lower()
        for node_id, d in self._get_nodes_by_type('Building'):
            if (name_lower in d.get('name', '').lower()
                    or name_lower in d.get('id', '').lower()
                    or name_lower in d.get('type', '').lower()):
                resp = f"**🏢 {d.get('name')}**\n"
                resp += f"Type: {d.get('type', 'N/A')} | Floors: {d.get('floors', 'N/A')}\n"
                resp += f"{d.get('description', '')}\n"

                # List rooms in this building
                rooms = [
                    (n, self.graph.nodes[n].get('data', {}))
                    for n in self.graph.successors(node_id)
                    if self.graph.nodes[n].get('node_type') == 'Room'
                ]
                if rooms:
                    resp += "\n**Rooms:**\n"
                    for _, rd in rooms:
                        resp += f"• {rd.get('name', 'Room')} ({rd.get('type', '')}) — Capacity: {rd.get('capacity', 'N/A')}\n"

                return resp

        return ("I couldn't find that building. Available buildings include: "
                "Main Block, Block A (AI & ML), Block B (DS & CS), Block C (ECE & Mech), "
                "Block D (Civil & MBA), Central Library, Administrative Block, Auditorium.")

    def query_campus_infrastructure(self):
        """Overview of all campus buildings and infrastructure."""
        buildings = self._get_nodes_by_type('Building')
        if not buildings:
            return "Campus infrastructure information is currently unavailable."

        resp = "**🏛️ Campus Infrastructure — Sphoorthy Engineering College:**\n\n"
        total_rooms = 0
        for node_id, d in buildings:
            room_count = sum(
                1 for n in self.graph.successors(node_id)
                if self.graph.nodes[n].get('node_type') == 'Room'
            )
            total_rooms += room_count
            resp += f"• **{d.get('name')}** — {d.get('type', '')} | {d.get('floors', '?')} floors | {room_count} rooms\n"

        resp += f"\n📊 Total: {len(buildings)} buildings, {total_rooms} rooms"
        return resp

    # ── NEW: Faculty profile queries ──────────────────────────────────────────

    def query_faculty_profile(self, faculty_name):
        """Detailed faculty profile with subjects taught, department, qualifications."""
        name_lower = faculty_name.lower()
        for node_id, d in self._get_nodes_by_type('Faculty'):
            if name_lower in d.get('name', '').lower():
                resp = f"**👨‍🏫 {d.get('name')}**\n"
                resp += f"Designation: {d.get('designation', 'N/A')}\n"
                resp += f"Qualification: {d.get('qualification', 'N/A')}\n"
                resp += f"Experience: {d.get('experience', 'N/A')}\n"

                # Find department
                for neighbor in self.graph.successors(node_id):
                    if self.graph.nodes[neighbor].get('node_type') == 'Department':
                        dept_data = self.graph.nodes[neighbor].get('data', {})
                        resp += f"Department: {dept_data.get('name', 'N/A')}\n"
                        break

                # Find subjects taught
                subjects = [
                    self.graph.nodes[n].get('data', {}).get('name', 'Unknown')
                    for n in self.graph.successors(node_id)
                    if self.graph.nodes[n].get('node_type') == 'Subject'
                ]
                if subjects:
                    resp += f"\n**Subjects Taught:**\n"
                    for subj in subjects:
                        resp += f"• {subj}\n"

                # Find research areas
                research = [
                    self.graph.nodes[n].get('data', {}).get('name', 'Unknown')
                    for n in self.graph.successors(node_id)
                    if self.graph.nodes[n].get('node_type') == 'ResearchArea'
                ]
                if research:
                    resp += f"\n**Research Areas:** {', '.join(research)}"

                return resp

        return ("I couldn't find that faculty member. "
                "Try using their full name, e.g., 'Dr. KVSN Ramarao' or 'Prof. Kiran B. M.'")

    # ── NEW: Subject queries ──────────────────────────────────────────────────

    def query_subjects_by_department(self, dept_name):
        """List all subjects for a department, grouped by semester."""
        dept_lower = dept_name.lower()
        dept_node = None
        dept_data = None

        for node_id, d in self._get_nodes_by_type('Department'):
            if (dept_lower in d.get('name', '').lower()
                    or dept_lower in d.get('short', '').lower()
                    or dept_lower == d.get('id', '').lower()):
                dept_node = node_id
                dept_data = d
                break

        if not dept_node:
            return "I couldn't find that department. Please specify a valid department name."

        # Collect subjects grouped by semester
        subjects_by_sem = {}
        for n in self.graph.successors(dept_node):
            if self.graph.nodes[n].get('node_type') == 'Subject':
                sd = self.graph.nodes[n].get('data', {})
                sem = sd.get('semester', 0)
                if sem not in subjects_by_sem:
                    subjects_by_sem[sem] = []
                subjects_by_sem[sem].append(sd)

        if not subjects_by_sem:
            return f"No subject data available for {dept_data.get('name')}."

        resp = f"**📚 Subjects — {dept_data.get('name')} ({dept_data.get('short')}):**\n\n"
        for sem in sorted(subjects_by_sem.keys()):
            resp += f"**Semester {sem}:**\n"
            for subj in subjects_by_sem[sem]:
                type_tag = f" [{subj.get('type', 'theory')}]" if subj.get('type') else ""
                resp += f"• {subj.get('code', '')} — {subj.get('name', '')} ({subj.get('credits', '?')} cr){type_tag}\n"
            resp += "\n"

        return resp.strip()

    def query_subjects_by_semester(self, dept_name, semester):
        """Get subjects for a specific department and semester."""
        dept_lower = dept_name.lower()
        dept_node = None
        dept_data = None

        for node_id, d in self._get_nodes_by_type('Department'):
            if (dept_lower in d.get('name', '').lower()
                    or dept_lower in d.get('short', '').lower()
                    or dept_lower == d.get('id', '').lower()):
                dept_node = node_id
                dept_data = d
                break

        if not dept_node:
            return "I couldn't find that department."

        subjects = []
        for n in self.graph.successors(dept_node):
            if self.graph.nodes[n].get('node_type') == 'Subject':
                sd = self.graph.nodes[n].get('data', {})
                if sd.get('semester') == semester:
                    subjects.append(sd)

        if not subjects:
            return f"No subjects found for {dept_data.get('name')} in Semester {semester}."

        resp = f"**📚 {dept_data.get('name')} — Semester {semester}:**\n"
        for subj in subjects:
            type_tag = f" [{subj.get('type', 'theory')}]" if subj.get('type') else ""
            resp += f"• {subj.get('code', '')} — {subj.get('name', '')} ({subj.get('credits', '?')} cr){type_tag}\n"
        return resp

    # ── NEW: ER Schema query ──────────────────────────────────────────────────

    def query_er_schema(self):
        """Returns a text summary of the ER schema."""
        from .er_schema import export_er_summary
        summary = export_er_summary()
        resp = "**📊 Knowledge Graph ER Schema:**\n\n"
        resp += f"**Entity Types:** {summary['total_entities']}\n"
        for et in summary['entity_types']:
            req = ', '.join(et['required_fields']) if et['required_fields'] else 'none'
            resp += f"• {et['name']} (required: {req})\n"
        resp += f"\n**Relationship Types:** {summary['total_relationships']}\n"
        for rt in summary['relationship_types']:
            resp += f"• {rt['source']} —[{rt['name']}]→ {rt['target']}\n"
        return resp

    # ── General search ────────────────────────────────────────────────────────

    def search_general(self, query):
        """Fallback: search across all node data dicts for keyword matches."""
        query_lower = query.lower()
        matches = []

        for node_id, attrs in self.graph.nodes(data=True):
            node_type = attrs.get('node_type', '')
            data = attrs.get('data', {})
            # Search all string values in the data dict
            for val in data.values():
                if isinstance(val, str) and query_lower in val.lower():
                    matches.append((node_type, data))
                    break
                if isinstance(val, list):
                    for item in val:
                        if isinstance(item, str) and query_lower in item.lower():
                            matches.append((node_type, data))
                            break

        if not matches:
            return ("I couldn't find that. Try asking about departments, admissions, fees, placements, facilities, or contact info.")

        resp = "**Found:**\n"
        seen = set()
        for node_type, d in matches[:3]:
            name = d.get('name', node_type)
            if name not in seen:
                seen.add(name)
                resp += f"• {name} ({node_type})\n"
        return resp

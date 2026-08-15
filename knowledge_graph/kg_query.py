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
        b  = ad.get('btech', {})
        mt = ad.get('mtech', {})
        mb = ad.get('mba', {})
        return (f"**Admissions:**\n"
                f"• B.Tech: TG EAPCET (Convener 70%) or Direct (Management 30%)\n"
                f"• M.Tech: TG PGECET / GATE\n"
                f"• MBA: TG ICET")

    def query_placements(self):
        pd = self._d('placements')
        if not pd:
            return "Placement information is currently unavailable."

        training = pd.get('training', [])
        recruiters = pd.get('top_recruiters', [])

        resp = f"**Placements (2024-25):**\n"
        resp += f"• Highest: {pd.get('highest_package', 'N/A')} | Avg: {pd.get('average_package', 'N/A')}\n"
        resp += f"• Placed: {pd.get('students_placed_2024_25', 'N/A')} | Offers: {pd.get('job_offers_2024_25', 'N/A')}\n"
        recruiters = pd.get('top_recruiters', [])
        if recruiters:
            resp += f"• Top Recruiters: {', '.join(recruiters[:5])}"
        return resp

    def query_facilities(self):
        fac_nodes = self._get_nodes_by_type('Facility')
        if not fac_nodes:
            return "Facilities information is currently unavailable."

        resp = "**Campus Facilities:**\n"
        for _, d in fac_nodes:
            resp += f"• {d.get('name', 'Facility')}\n"
        return resp

    def query_scholarships(self):
        schol_nodes = self._get_nodes_by_type('Scholarship')
        if not schol_nodes:
            return "Scholarship information is currently unavailable."

        resp = "**Scholarships:**\n"
        for _, d in schol_nodes:
            resp += f"• {d.get('name', '')}: {d.get('description', '')[:80]}\n"
        return resp

    def query_events(self):
        event_nodes = self._get_nodes_by_type('Event')
        if not event_nodes:
            return "Events information is currently unavailable."

        resp = "**College Events:**\n"
        for _, d in event_nodes:
            resp += f"• {d.get('name', '')} ({d.get('type', '')})\n"
        return resp

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

    def query_college_info(self):
        cd = self._d('college')
        if not cd:
            return "College information is currently unavailable."

        resp = f"**{cd.get('name')} ({cd.get('code')})**\n"
        resp += f"Est. {cd.get('established')} | {cd.get('type')}\n"
        resp += f"{cd.get('affiliation')} | {cd.get('accreditation')}\n"
        resp += f"Campus: {cd.get('campus_area')}"
        return resp

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

    def query_clubs(self):
        club_nodes = self._get_nodes_by_type('Club')
        if not club_nodes:
            return "Student clubs information is currently unavailable."

        resp = "**🎭 Student Clubs at Sphoorthy:**\n\n"
        for _, d in club_nodes:
            resp += f"• {d.get('name', 'Club')}\n"
        return resp

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

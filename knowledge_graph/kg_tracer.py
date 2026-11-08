"""
Knowledge Graph Path Tracer
Extracts and formats live shortest-path traversal chains from the Campus Knowledge Graph
for display as visual knowledge path badges in chat responses.
"""
import networkx as nx

ICON_MAP = {
    "College": "fa-university",
    "Department": "fa-laptop-code",
    "Faculty": "fa-user-tie",
    "HOD": "fa-user-graduate",
    "Subject": "fa-book-open",
    "Course": "fa-graduation-cap",
    "Building": "fa-building",
    "Room": "fa-door-open",
    "Lab": "fa-flask",
    "Recruiter": "fa-briefcase",
    "Club": "fa-users",
    "Facility": "fa-wifi",
    "Scholarship": "fa-award",
    "Event": "fa-calendar-alt",
    "Entity": "fa-circle-nodes"
}

REL_LABELS = {
    "has_department": "Department",
    "has_faculty": "Faculty Member",
    "has_hod": "Headed by HOD",
    "teaches": "Teaches Subject",
    "located_in": "Located in",
    "offers": "Offers Program",
    "offers_course": "Offers Course",
    "has_subject": "Syllabus Subject",
    "has_facility": "Campus Facility",
    "has_club": "Student Club",
    "has_scholarship": "Scholarship",
    "has_building": "Campus Building",
    "has_event": "Campus Event",
    "recruited_by": "Top Recruiter",
    "affiliated_to": "Affiliated with"
}


def find_target_node(graph, intent, entities):
    """Resolve intent + entities to the best matching node in graph."""
    if not graph:
        return None

    # Priority 1: Specific named entity lookups
    if 'faculty_name' in entities:
        t = entities['faculty_name'].lower().strip()
        for n, d in graph.nodes(data=True):
            if d.get('node_type') in ['Faculty', 'HOD']:
                name = d.get('data', {}).get('name', str(n)).lower()
                if t in name or any(part in name for part in t.split() if len(part) > 2):
                    return n

    if 'subject' in entities:
        t = entities['subject'].lower().strip()
        for n, d in graph.nodes(data=True):
            if d.get('node_type') == 'Subject':
                name = d.get('data', {}).get('name', str(n)).lower()
                if t in name or t in str(n).lower():
                    return n

    if 'department' in entities:
        t = entities['department'].lower().strip()
        for n, d in graph.nodes(data=True):
            if d.get('node_type') == 'Department':
                name = d.get('data', {}).get('name', str(n)).lower()
                code = str(d.get('data', {}).get('code', '')).lower()
                if t in name or t in code or t in str(n).lower():
                    return n

    if 'building' in entities:
        t = entities['building'].lower().strip()
        for n, d in graph.nodes(data=True):
            if d.get('node_type') == 'Building':
                name = d.get('data', {}).get('name', str(n)).lower()
                if t in name or t in str(n).lower():
                    return n

    if 'course' in entities:
        t = entities['course'].lower().strip()
        for n, d in graph.nodes(data=True):
            if d.get('node_type') == 'Course':
                name = d.get('data', {}).get('name', str(n)).lower()
                if t in name or t in str(n).lower():
                    return n

    # Priority 2: Intent-based representative nodes
    if intent == 'hod_info':
        dept_match = [n for n, d in graph.nodes(data=True) if d.get('node_type') == 'HOD']
        if dept_match:
            return dept_match[0]

    if intent == 'placement_info':
        recruiter_match = [n for n, d in graph.nodes(data=True) if d.get('node_type') == 'Recruiter']
        if recruiter_match:
            return recruiter_match[0]

    if intent == 'facility_info':
        fac_match = [n for n, d in graph.nodes(data=True) if d.get('node_type') == 'Facility']
        if fac_match:
            return fac_match[0]

    if intent == 'club_info':
        club_match = [n for n, d in graph.nodes(data=True) if d.get('node_type') == 'Club']
        if club_match:
            return club_match[0]

    if intent == 'scholarship_info':
        sch_match = [n for n, d in graph.nodes(data=True) if d.get('node_type') == 'Scholarship']
        if sch_match:
            return sch_match[0]

    if intent == 'building_info':
        bld_match = [n for n, d in graph.nodes(data=True) if d.get('node_type') == 'Building']
        if bld_match:
            return bld_match[0]

    return None


def generate_graph_trace(graph, intent, entities):
    """
    Compute the live shortest graph path from 'college' to target node
    and return structured trace steps with labels, types, and icons.
    """
    if not graph or intent in ['greeting', 'farewell', 'thanks', 'bot_identity']:
        return None

    target = find_target_node(graph, intent, entities)
    if not target or target == 'college':
        return None

    try:
        # Use undirected graph view for robust bi-directional navigation
        Gu = graph.to_undirected()
        if not nx.has_path(Gu, 'college', target):
            return None

        path_nodes = nx.shortest_path(Gu, 'college', target)
        if len(path_nodes) <= 1:
            return None

        # Build step-by-step trace
        trace = []
        for i, nid in enumerate(path_nodes):
            ndata = graph.nodes[nid]
            ntype = ndata.get('node_type', 'Entity')
            nname = ndata.get('data', {}).get('name', str(nid))
            
            # Clean up display name
            if len(nname) > 28:
                nname = nname[:26] + '..'

            node_step = {
                "id": str(nid),
                "name": nname,
                "type": ntype,
                "icon": ICON_MAP.get(ntype, "fa-circle-dot")
            }
            trace.append({"kind": "node", "data": node_step})

            # Add intermediate relationship if not the last node
            if i < len(path_nodes) - 1:
                next_nid = path_nodes[i + 1]
                edge_data = graph.get_edge_data(nid, next_nid) or graph.get_edge_data(next_nid, nid) or {}
                rel_raw = edge_data.get('relationship', 'related_to')
                rel_label = REL_LABELS.get(rel_raw, rel_raw.replace('_', ' ').title())

                trace.append({
                    "kind": "edge",
                    "data": {
                        "rel": rel_raw,
                        "label": rel_label
                    }
                })

        return {
            "source": "campus_kg",
            "hops": len(path_nodes) - 1,
            "target": target,
            "steps": trace
        }
    except Exception as e:
        return None

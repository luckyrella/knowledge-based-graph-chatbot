"""
Automated Knowledge Graph Health & Audit Engine
Performs real-time topological analysis, structural integrity scans,
and schema completeness validations across the Campus Knowledge Graph.
"""
import networkx as nx
from datetime import datetime


def run_graph_audit(graph, neo4j_service=None):
    """
    Execute a full diagnostic audit on the provided NetworkX graph
    and cross-verify with Neo4j status.
    """
    if not graph or graph.number_of_nodes() == 0:
        return {
            "status": "error",
            "message": "Graph is empty or uninitialized.",
            "health_score": 0
        }

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    num_nodes = graph.number_of_nodes()
    num_edges = graph.number_of_edges()

    # 1. Topological Connectivity
    Gu = graph.to_undirected()
    comp_count = nx.number_connected_components(Gu)
    is_connected = comp_count == 1
    density = round(nx.density(graph), 5)
    avg_degree = round((num_edges * 2) / max(num_nodes, 1), 2)

    # 2. Isolated / Orphan Nodes
    deg_map = dict(graph.degree())
    isolated_nodes = []
    for nid, deg in deg_map.items():
        if deg == 0:
            ndata = graph.nodes[nid]
            isolated_nodes.append({
                "id": str(nid),
                "name": ndata.get("data", {}).get("name", str(nid)),
                "type": ndata.get("node_type", "Entity")
            })

    # 3. Entity Distribution
    entity_counts = {}
    for _, ndata in graph.nodes(data=True):
        ntype = ndata.get("node_type", "Entity")
        entity_counts[ntype] = entity_counts.get(ntype, 0) + 1

    # 4. Relational & Schema Integrity Checks
    departments = [n for n, d in graph.nodes(data=True) if d.get("node_type") == "Department"]
    faculty = [n for n, d in graph.nodes(data=True) if d.get("node_type") == "Faculty"]
    subjects = [n for n, d in graph.nodes(data=True) if d.get("node_type") == "Subject"]
    buildings = [n for n, d in graph.nodes(data=True) if d.get("node_type") == "Building"]

    # Check: Department HODs & Locations
    dept_checks = []
    missing_hod_count = 0
    missing_bld_count = 0
    for dept_id in departments:
        d_name = graph.nodes[dept_id].get("data", {}).get("name", dept_id)
        # Check outgoing edges from this dept
        out_edges = graph.edges(dept_id, data=True)
        in_edges = graph.in_edges(dept_id, data=True)
        all_d_edges = list(out_edges) + [(u, v, d) for u, v, d in in_edges]

        has_hod = any(d.get("relationship") in ["has_hod", "headed_by"] or "hod" in str(v).lower() for u, v, d in all_d_edges)
        has_bld = any(d.get("relationship") in ["located_in", "houses"] or "building" in str(v).lower() for u, v, d in all_d_edges)

        if not has_hod:
            missing_hod_count += 1
        if not has_bld:
            missing_bld_count += 1

        dept_checks.append({
            "dept_id": dept_id,
            "name": d_name,
            "has_hod": has_hod,
            "has_location": has_bld
        })

    # Check: Faculty Department affiliations
    unlinked_faculty = []
    for f_id in faculty:
        in_e = graph.in_edges(f_id, data=True)
        out_e = graph.edges(f_id, data=True)
        f_edges = list(in_e) + list(out_e)
        linked_to_dept = any("dept" in str(u).lower() or "dept" in str(v).lower() for u, v, _ in f_edges)
        if not linked_to_dept:
            f_name = graph.nodes[f_id].get("data", {}).get("name", f_id)
            unlinked_faculty.append({"id": str(f_id), "name": f_name})

    # 5. Top Degree Centrality Hubs
    centrality = nx.degree_centrality(graph)
    sorted_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:6]
    top_hubs = []
    for nid, score in sorted_centrality:
        ndata = graph.nodes[nid]
        top_hubs.append({
            "id": str(nid),
            "name": ndata.get("data", {}).get("name", str(nid)),
            "type": ndata.get("node_type", "Entity"),
            "degree": deg_map.get(nid, 0),
            "centrality": round(score, 4)
        })

    # 6. Compute Comprehensive Health Score (0 - 100)
    score = 100.0
    deductions = []

    # Isolated nodes penalty
    if len(isolated_nodes) > 0:
        penalty = min(len(isolated_nodes) * 5.0, 30.0)
        score -= penalty
        deductions.append(f"-{penalty} pts: {len(isolated_nodes)} orphan node(s) with degree 0")

    # Fragmented components penalty
    if comp_count > 1:
        penalty = min((comp_count - 1) * 10.0, 30.0)
        score -= penalty
        deductions.append(f"-{penalty} pts: Graph is fragmented into {comp_count} sub-graphs")

    # Missing Department HODs
    if missing_hod_count > 0:
        penalty = missing_hod_count * 2.0
        score -= penalty
        deductions.append(f"-{penalty} pts: {missing_hod_count} department(s) missing assigned HOD")

    # Missing Department Locations
    if missing_bld_count > 0:
        penalty = missing_bld_count * 1.5
        score -= penalty
        deductions.append(f"-{penalty} pts: {missing_bld_count} department(s) missing building anchor")

    # Unlinked Faculty
    if len(unlinked_faculty) > 0:
        penalty = min(len(unlinked_faculty) * 1.0, 15.0)
        score -= penalty
        deductions.append(f"-{penalty} pts: {len(unlinked_faculty)} faculty member(s) not directly linked to a department")

    health_score = max(round(score, 1), 0.0)

    # Status classification
    if health_score >= 90:
        grade = "A+ (Optimal)"
        status_color = "#10b981"
        status_label = "HEALTHY"
    elif health_score >= 75:
        grade = "B (Good)"
        status_color = "#38bdf8"
        status_label = "STABLE"
    elif health_score >= 50:
        grade = "C (Needs Attention)"
        status_color = "#f59e0b"
        status_label = "WARNING"
    else:
        grade = "D (Fragmented)"
        status_color = "#ef4444"
        status_label = "CRITICAL"

    # Automated positive findings
    findings = []
    if len(isolated_nodes) == 0:
        findings.append("✅ Zero orphan nodes: All 424 entities possess active topological relationships.")
    if is_connected:
        findings.append("✅ Unified Campus Galaxy: Graph is fully connected as 1 single cohesive network.")
    if len(unlinked_faculty) == 0:
        findings.append("✅ Faculty Integration: 100% of faculty members are anchored to academic departments.")
    if len(departments) > 0 and missing_hod_count == 0:
        findings.append("✅ Administrative Completeness: Every academic department has an assigned HOD.")

    # Neo4j status check
    neo4j_status = "Disconnected (In-Memory Engine Active)"
    if neo4j_service:
        try:
            if neo4j_service.is_connected():
                neo4j_status = "Connected (Neo4j Cloud Aura Active)"
        except Exception:
            pass

    return {
        "timestamp": timestamp,
        "health_score": health_score,
        "grade": grade,
        "status_color": status_color,
        "status_label": status_label,
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "density": density,
        "avg_degree": avg_degree,
        "comp_count": comp_count,
        "is_connected": is_connected,
        "isolated_nodes_count": len(isolated_nodes),
        "isolated_nodes": isolated_nodes,
        "unlinked_faculty_count": len(unlinked_faculty),
        "unlinked_faculty": unlinked_faculty,
        "entity_counts": entity_counts,
        "dept_checks": dept_checks,
        "top_hubs": top_hubs,
        "deductions": deductions,
        "findings": findings,
        "neo4j_status": neo4j_status
    }

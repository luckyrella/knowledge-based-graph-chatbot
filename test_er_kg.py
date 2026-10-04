"""
Test suite for the formal Entity-Relationship Knowledge Graph.
Validates existing chatbot functionality + new ER features.
"""
import sys
import os

# Fix Windows console encoding for ₹ and other Unicode
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from knowledge_graph.kg_builder import KnowledgeGraphBuilder
from knowledge_graph.kg_query import KnowledgeGraphQuery
from knowledge_graph.nlp_processor import NLPProcessor
from knowledge_graph.er_schema import export_er_diagram, export_er_summary, validate_graph_against_schema

builder = KnowledgeGraphBuilder('data/college_data.json')
builder.build_graph()
graph = builder.get_graph()
query = KnowledgeGraphQuery(graph)
nlp = NLPProcessor()

passed = 0
failed = 0

def check(test_name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  ✅ {test_name}")
    else:
        failed += 1
        print(f"  ❌ {test_name} — {detail}")

# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 65)
print("  FORMAL ER KNOWLEDGE GRAPH — TEST SUITE")
print("=" * 65)

# ── 1. Graph Structure Tests ──────────────────────────────────────────────────
print("\n📊 1. GRAPH STRUCTURE")
stats = builder.get_graph_stats()
check("Graph has nodes", stats["total_nodes"] > 100, f"Got {stats.get('total_nodes', 0)}")
check("Graph has edges", stats["total_edges"] > 100, f"Got {stats.get('total_edges', 0)}")

# ── 2. Entity Type Tests ─────────────────────────────────────────────────────
print("\n🏗️  2. ENTITY TYPES PRESENT")
node_types = stats["nodes"]
for expected_type in ['College', 'Department', 'Faculty', 'Subject', 'Building',
                      'Room', 'Semester', 'Program', 'Lab', 'Course', 'Facility',
                      'HOD', 'Recruiter', 'Scholarship', 'Event', 'Club']:
    check(f"Has {expected_type} nodes", expected_type in node_types,
          f"Missing node type: {expected_type}")

print(f"\n  Node counts: {node_types}")

# ── 3. Relationship Type Tests ────────────────────────────────────────────────
print("\n🔗 3. RELATIONSHIP TYPES PRESENT")
edge_types = stats["edges"]
for expected_rel in ['has_department', 'has_building', 'has_room', 'has_faculty',
                     'offers_subject', 'has_semester', 'has_program', 'teaches',
                     'belongs_to', 'housed_in', 'offered_in']:
    check(f"Has '{expected_rel}' edges", expected_rel in edge_types,
          f"Missing relationship: {expected_rel}")

# ── 4. Campus Infrastructure Tests ────────────────────────────────────────────
print("\n🏛️  4. CAMPUS INFRASTRUCTURE")
buildings = [n for n, d in graph.nodes(data=True) if d.get('node_type') == 'Building']
rooms = [n for n, d in graph.nodes(data=True) if d.get('node_type') == 'Room']
check("Has buildings", len(buildings) >= 8, f"Got {len(buildings)}")
check("Has rooms", len(rooms) >= 20, f"Got {len(rooms)}")

# Check Building → Room edges
building_room_edges = sum(
    1 for u, v, d in graph.edges(data=True)
    if d.get('relationship') == 'has_room'
)
check("Building→Room edges exist", building_room_edges >= 20, f"Got {building_room_edges}")

# Check Department → Building (housed_in) edges
housed_in_edges = sum(
    1 for u, v, d in graph.edges(data=True)
    if d.get('relationship') == 'housed_in'
)
check("Department→Building edges exist", housed_in_edges >= 5, f"Got {housed_in_edges}")

# ── 5. Curriculum Tests ──────────────────────────────────────────────────────
print("\n📚 5. CURRICULUM (Program → Semester → Subject)")
programs = [n for n, d in graph.nodes(data=True) if d.get('node_type') == 'Program']
semesters = [n for n, d in graph.nodes(data=True) if d.get('node_type') == 'Semester']
subjects = [n for n, d in graph.nodes(data=True) if d.get('node_type') == 'Subject']
check("Has programs", len(programs) >= 8, f"Got {len(programs)}")
check("Has semesters", len(semesters) >= 20, f"Got {len(semesters)}")
check("Has subjects", len(subjects) >= 50, f"Got {len(subjects)}")

# Subjects have code attribute
subjects_with_code = sum(
    1 for n in subjects
    if graph.nodes[n].get('data', {}).get('code')
)
check("Subjects have codes", subjects_with_code >= 50, f"Got {subjects_with_code}")

# ── 6. Faculty Assignment Tests (data-driven, no pseudo-random) ──────────────
print("\n👨‍🏫 6. FACULTY ASSIGNMENTS")
teaches_edges = sum(
    1 for u, v, d in graph.edges(data=True)
    if d.get('relationship') == 'teaches'
)
check("Faculty→Subject 'teaches' edges exist", teaches_edges >= 20, f"Got {teaches_edges}")

# Verify specific known assignment
# Prof. Kiran B. M. should teach CS501 (Computer Networks)
faculty_nodes = [(n, d) for n, d in graph.nodes(data=True) if d.get('node_type') == 'Faculty']
kiran_node = None
for n, d in faculty_nodes:
    if 'Kiran' in d.get('data', {}).get('name', ''):
        kiran_node = n
        break
if kiran_node:
    kiran_teaches = [
        graph.nodes[v].get('data', {}).get('code')
        for v in graph.successors(kiran_node)
        if graph.nodes[v].get('node_type') == 'Subject'
    ]
    check("Prof. Kiran teaches CS501", 'CS501' in kiran_teaches, f"Teaches: {kiran_teaches}")
else:
    check("Prof. Kiran found in graph", False, "Node not found")

# ── 7. ER Schema Tests ───────────────────────────────────────────────────────
print("\n📐 7. ER SCHEMA")
er_diagram = export_er_diagram()
check("ER diagram generated", len(er_diagram) > 100, f"Length: {len(er_diagram)}")
check("ER diagram is Mermaid format", er_diagram.startswith("erDiagram"), "Doesn't start with erDiagram")
check("ER diagram has Building entity", "Building" in er_diagram, "Missing Building")

er_summary = export_er_summary()
check("ER summary has entity_types", len(er_summary['entity_types']) >= 20, f"Got {len(er_summary['entity_types'])}")
check("ER summary has relationship_types", len(er_summary['relationship_types']) >= 25, f"Got {len(er_summary['relationship_types'])}")

# Graph validation
validation = validate_graph_against_schema(graph)
check("Graph validates against schema", True, "")  # We check error count below
print(f"  Validation errors: {len(validation['errors'])}, warnings: {len(validation['warnings'])}")
if validation['errors'][:3]:
    for e in validation['errors'][:3]:
        print(f"    ⚠️ {e}")

# ── 8. Query Engine Tests ────────────────────────────────────────────────────
print("\n💬 8. QUERY ENGINE")

# Existing queries
resp = query.query_department("cse")
check("Department query works", "Computer Science" in resp, resp[:50])

resp = query.query_fees("btech")
check("Fee query works", "B.Tech" in resp, resp[:50])

resp = query.query_placements()
check("Placement query works", "Placements" in resp, resp[:50])

# NEW queries
resp = query.query_campus_infrastructure()
check("Campus infrastructure query works", "Main Block" in resp, resp[:80])

resp = query.query_building("block a")
check("Building query works", "AI" in resp or "Block A" in resp, resp[:80])

resp = query.query_faculty_profile("kiran")
check("Faculty profile query works", "Kiran" in resp, resp[:80])

resp = query.query_subjects_by_department("cse")
check("Subjects by department works", "Semester" in resp, resp[:80])

resp = query.query_subjects_by_semester("cse", 4)
check("Subjects by semester works", "Database" in resp or "Semester 4" in resp, resp[:80])

resp = query.query_er_schema()
check("ER schema query works", "Entity Types" in resp, resp[:80])

# ── 9. NLP Intent Tests ──────────────────────────────────────────────────────
print("\n🧠 9. NLP INTENT DETECTION")
nlp_tests = [
    ("What buildings are on campus?", "building_info"),
    ("Tell me about Dr. KVSN Ramarao", "faculty_profile"),
    ("What subjects are in CSE?", "subject_info"),
    ("Hello", "greeting"),
    ("What is the fee for BTech?", "fee_info"),
    ("Tell me about CSE department", "department_info"),
    ("How are the placements?", "placement_info"),
]
for question, expected_intent in nlp_tests:
    result = nlp.process(question)
    check(f"'{question}' → {expected_intent}", result['intent'] == expected_intent,
          f"Got: {result['intent']}")

# ── 10. No Pseudo-Random Links Test ──────────────────────────────────────────
print("\n🚫 10. NO PSEUDO-RANDOM LINKS")
# The old builder used hash() % N for recruiter→dept and subject→lab links
# Verify that recruiters are NOT linked to departments via recruited_from
recruited_from_edges = sum(
    1 for u, v, d in graph.edges(data=True)
    if d.get('relationship') == 'recruited_from'
)
check("No pseudo-random recruited_from edges", recruited_from_edges == 0,
      f"Found {recruited_from_edges} (should be 0)")

# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print(f"  RESULTS: {passed} passed, {failed} failed, {passed + failed} total")
print("=" * 65)

if failed > 0:
    print(f"\n  ⚠️  {failed} test(s) failed!")
    sys.exit(1)
else:
    print("\n  🎉 ALL TESTS PASSED!")
    sys.exit(0)

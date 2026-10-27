"""
System Performance & Latency Benchmarking Engine
KG-RAG Campus Assistant & Knowledge Graph Engine
"""
import time
import json
import os
import sys
import tracemalloc

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

from app import create_app
from knowledge_graph.kg_builder import KnowledgeGraphBuilder
from knowledge_graph.kg_query import KnowledgeGraphQuery
from knowledge_graph.nlp_processor import NLPProcessor

BENCHMARK_QUERIES = [
    # Department Queries
    ("tell me about cse department", "department_info"),
    ("what are the branches available", "department_info"),
    ("details of ece branch", "department_info"),
    ("info on artificial intelligence", "department_info"),
    ("civil engineering details", "department_info"),
    # Fee Queries
    ("what is the fee structure for btech", "fee_info"),
    ("how much does mba cost", "fee_info"),
    ("tuition fees for cse", "fee_info"),
    ("annual charges for btech", "fee_info"),
    # Admission Queries
    ("admission process through eamcet", "admission_info"),
    ("lateral entry eligibility criteria", "admission_info"),
    ("how can i join sphoorthy college", "admission_info"),
    ("tg eapcet rank needed", "admission_info"),
    # Placement Queries
    ("highest package this year", "placement_info"),
    ("placement statistics and average salary", "placement_info"),
    ("which companies recruit from campus", "placement_info"),
    ("top recruiters in sphoorthy", "placement_info"),
    # Building & Infrastructure
    ("where is block a located", "building_info"),
    ("what buildings are on campus", "building_info"),
    ("where is the cse block", "building_info"),
    ("campus building details", "building_info"),
    # Faculty Profile
    ("tell me about dr kvsn ramarao", "faculty_profile"),
    ("faculty profile of prof kiran", "faculty_profile"),
    ("who teaches machine learning", "faculty_profile"),
    # Subjects & Curriculum
    ("what subjects are in cse 3rd semester", "subject_info"),
    ("curriculum for aiml semester 4", "subject_info"),
    ("subjects taught in mechanical", "subject_info"),
    # Study Materials & Notes
    ("give me study notes for operating systems", "material_info"),
    ("download database systems notes", "material_info"),
    ("where can i find lecture notes", "material_info"),
    ("unit 2 notes for machine learning", "material_info"),
    # Circulars & Notices
    ("what are the latest circulars", "notice_info"),
    ("show recent college notices", "notice_info"),
    ("exam schedule notifications", "notice_info"),
    ("official campus announcements", "notice_info"),
    # Management & HOD
    ("who is the principal", "management_info"),
    ("who is the chairman", "management_info"),
    ("who is the hod of cse", "hod_info"),
    ("ece head of department", "hod_info"),
    # Facilities & Clubs
    ("hostel facilities and library info", "facility_info"),
    ("sports facilities and gym", "facility_info"),
    ("student clubs and activities", "club_info"),
    ("scholarships available", "scholarship_info"),
    # Greetings & Salutations
    ("hello good morning", "greeting"),
    ("thank you for your help", "thanks"),
    ("goodbye see you later", "farewell")
]

def run_benchmarks():
    print("\n" + "=" * 65)
    print("  INITIALIZING KG-RAG PERFORMANCE BENCHMARK ENGINE")
    print("=" * 65)

    app = create_app()
    client = app.test_client()

    data_path = os.path.join(app.root_path, 'data', 'college_data.json')
    kg_builder = KnowledgeGraphBuilder(data_path)
    kg_builder.build_graph()
    graph = kg_builder.get_graph()
    kg_query = KnowledgeGraphQuery(graph)
    nlp = NLPProcessor()

    # 1. Memory Footprint
    tracemalloc.start()
    kg_builder.build_graph()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    ram_mb = peak_mem / (1024 * 1024)
    node_count = graph.number_of_nodes()
    edge_count = graph.number_of_edges()

    print(f"\n[1] Knowledge Graph Topography & Memory Footprint:")
    print(f"    • Total Nodes: {node_count}")
    print(f"    • Total Directed Edges: {edge_count}")
    print(f"    • Graph RAM Allocation: {ram_mb:.2f} MB (Peak)")

    # 2. In-Memory Graph Sync / Hot-Reload Speed
    sync_times = []
    for _ in range(5):
        t0 = time.perf_counter()
        kg_builder.build_graph()
        sync_times.append((time.perf_counter() - t0) * 1000)
    avg_sync_ms = sum(sync_times) / len(sync_times)
    print(f"\n[2] In-Memory Dynamic Synchronization Speed (Reconstruction):")
    print(f"    • Rebuild Latency: {avg_sync_ms:.2f} ms (5-run avg)")

    # 3. NLP Intent Classification Latency & Accuracy
    nlp_times = []
    correct_intents = 0
    total_queries = len(BENCHMARK_QUERIES)

    for query, expected_intent in BENCHMARK_QUERIES:
        t0 = time.perf_counter()
        res = nlp.process(query)
        nlp_times.append((time.perf_counter() - t0) * 1000)
        if res['intent'] == expected_intent:
            correct_intents += 1

    avg_nlp_ms = sum(nlp_times) / len(nlp_times)
    accuracy_pct = (correct_intents / total_queries) * 100
    throughput_qps = 1000 / avg_nlp_ms

    print(f"\n[3] NLP Intent Classification & Fuzzy Matching:")
    print(f"    • Evaluated Queries: {total_queries}")
    print(f"    • Classification Accuracy: {accuracy_pct:.1f}% ({correct_intents}/{total_queries})")
    print(f"    • Avg NLP Latency: {avg_nlp_ms:.2f} ms")
    print(f"    • Intent Throughput: {throughput_qps:.1f} queries/sec")

    # 4. Multi-Hop Graph Traversal Latency
    traversal_tests = [
        ("query_department('cse')", lambda: kg_query.query_department('cse')),
        ("query_faculty_profile('Dr. KVSN Ramarao')", lambda: kg_query.query_faculty_profile('Dr. KVSN Ramarao')),
        ("query_subjects_by_semester('cse', 3)", lambda: kg_query.query_subjects_by_semester('cse', 3)),
        ("query_building('block a')", lambda: kg_query.query_building('block a')),
        ("query_fees('btech', 'cse')", lambda: kg_query.query_fees('btech', 'cse')),
        ("query_placements()", lambda: kg_query.query_placements()),
    ]
    traversal_latencies = []
    print(f"\n[4] Deterministic Graph Traversal Latency (Multi-Hop):")
    for name, fn in traversal_tests:
        times = []
        for _ in range(20):
            t0 = time.perf_counter()
            fn()
            times.append((time.perf_counter() - t0) * 1000)
        avg_t = sum(times) / len(times)
        traversal_latencies.append(avg_t)
        print(f"    • {name:<45} : {avg_t:.3f} ms")
    overall_avg_traversal = sum(traversal_latencies) / len(traversal_latencies)
    print(f"    • Mean Graph Traversal Latency: {overall_avg_traversal:.3f} ms")

    # 5. Full End-to-End HTTP Chatbot Response Latency
    http_latencies = []
    print(f"\n[5] End-to-End HTTP /api/chat Pipeline (Network + NLP + Graph + DB):")
    for query, _ in BENCHMARK_QUERIES[:25]:
        t0 = time.perf_counter()
        res = client.post('/api/chat', json={'message': query})
        http_latencies.append((time.perf_counter() - t0) * 1000)

    avg_http_ms = sum(http_latencies) / len(http_latencies)
    min_http_ms = min(http_latencies)
    max_http_ms = max(http_latencies)
    p95_http_ms = sorted(http_latencies)[int(len(http_latencies) * 0.95)]

    print(f"    • Average End-to-End Latency : {avg_http_ms:.2f} ms")
    print(f"    • Min Response Latency       : {min_http_ms:.2f} ms")
    print(f"    • 95th Percentile (P95)      : {p95_http_ms:.2f} ms")
    print(f"    • Max Response Latency       : {max_http_ms:.2f} ms")
    print(f"    • Sub-150ms Target Met       : {'✅ YES' if p95_http_ms < 150 else '❌ NO'}")

    # Summary Benchmark Dict
    results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "graph_statistics": {
            "node_count": node_count,
            "edge_count": edge_count,
            "process_ram_mb": round(ram_mb, 2)
        },
        "dynamic_sync": {
            "avg_rebuild_ms": round(avg_sync_ms, 2)
        },
        "nlp_performance": {
            "accuracy_percent": round(accuracy_pct, 2),
            "avg_latency_ms": round(avg_nlp_ms, 3),
            "throughput_qps": round(throughput_qps, 1)
        },
        "graph_traversal": {
            "mean_traversal_ms": round(overall_avg_traversal, 3)
        },
        "end_to_end_http": {
            "avg_latency_ms": round(avg_http_ms, 2),
            "p95_latency_ms": round(p95_http_ms, 2),
            "sub_150ms_validated": bool(p95_http_ms < 150)
        }
    }

    with open('benchmark_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 65)
    print("  BENCHMARK COMPLETED & SAVED TO benchmark_results.json")
    print("=" * 65 + "\n")
    return results

if __name__ == '__main__':
    run_benchmarks()

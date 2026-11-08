#!/usr/bin/env python3
"""
Sphoorthy Engineering College — Knowledge Graph to Neo4j Sync Utility
Syncs all college departments, faculty, subjects, buildings, rooms,
and relationships from JSON datasets into your Neo4j Graph Database.

Usage:
    python sync_to_neo4j.py
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from knowledge_graph.neo4j_service import Neo4jService

def main():
    print("=" * 65)
    print("🎓 SPHOORTHY ENGINEERING COLLEGE — NEO4J GRAPH SYNC")
    print("=" * 65)

    uri = os.environ.get("NEO4J_URI")
    user = os.environ.get("NEO4J_USERNAME", "neo4j")
    pwd = os.environ.get("NEO4J_PASSWORD")

    if not uri or not pwd:
        print("\n❌ Error: Missing Neo4j credentials.")
        print("Please set the following in your .env file or environment:")
        print("   NEO4J_URI=neo4j+s://<your-db-id>.databases.neo4j.io")
        print("   NEO4J_USERNAME=neo4j")
        print("   NEO4J_PASSWORD=<your-password>")
        print("\nGet a 100% free cloud instance at: https://neo4j.com/cloud/aura-free/")
        sys.exit(1)

    print(f"\n📡 Connecting to Neo4j at: {uri} ...")
    svc = Neo4jService(uri=uri, user=user, password=pwd)

    if not svc.is_connected:
        print("❌ Could not connect to Neo4j. Please verify your credentials and network connection.")
        sys.exit(1)

    print("✅ Connection verified successfully!")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    c_path = os.path.join(base_dir, "data", "college_data.json")
    f_path = os.path.join(base_dir, "data", "faculty_data.json")

    print(f"📦 Reading dataset from: {c_path}")
    print("⏳ Synchronizing nodes and relationships into Neo4j...")

    stats = svc.sync_from_json(c_path, f_path)

    if stats.get("status") == "success":
        print("\n🎉 SYNC COMPLETED SUCCESSFULLY!")
        print(f"   📊 Total Nodes in Neo4j:         {stats.get('nodes')}")
        print(f"   🔗 Total Relationships in Neo4j: {stats.get('edges')}")
        print("\n🌐 You can now open Neo4j Browser and run:")
        print("   MATCH (n)-[r]->(m) RETURN n,r,m LIMIT 200")
    else:
        print(f"\n⚠️ Sync finished with warning: {stats.get('message')}")

    svc.close()
    print("=" * 65)

if __name__ == "__main__":
    main()

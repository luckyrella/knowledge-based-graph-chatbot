"""
Seed realistic study materials and circular notices into the database.
"""
from app import create_app
from models import db
from models.material import StudyMaterial
from models.notice import Notice
from models.user import User

def seed_data():
    app = create_app()
    with app.app_context():
        admin = User.query.filter_by(role='admin').first()
        admin_id = admin.id if admin else 1

        # Check if materials already exist
        if StudyMaterial.query.count() == 0:
            materials = [
                StudyMaterial(
                    title="Unit 2: Process Management & CPU Scheduling",
                    subject="Operating Systems",
                    department="cse",
                    semester=4,
                    description="Comprehensive lecture notes on FCFS, SJF, Round Robin, and Multi-Level Queue Scheduling.",
                    file_path="/static/uploads/materials/sample_os_unit2.pdf",
                    uploaded_by=admin_id
                ),
                StudyMaterial(
                    title="Unit 3: Relational Algebra & SQL Normalization (1NF to BCNF)",
                    subject="Database Management Systems",
                    department="cse",
                    semester=4,
                    description="Detailed solved examples of database decomposition, dependency preservation, and lossless joins.",
                    file_path="/static/uploads/materials/sample_dbms_unit3.pdf",
                    uploaded_by=admin_id
                ),
                StudyMaterial(
                    title="Unit 1: Supervised Learning & Gradient Descent",
                    subject="Machine Learning",
                    department="cse_aiml",
                    semester=5,
                    description="Mathematical derivation of Cost Functions, MSE, Batch and Stochastic Gradient Descent.",
                    file_path="/static/uploads/materials/sample_ml_unit1.pdf",
                    uploaded_by=admin_id
                ),
                StudyMaterial(
                    title="Unit 4: Transport Layer Protocols (TCP vs UDP Congestion Control)",
                    subject="Computer Networks",
                    department="cse",
                    semester=5,
                    description="Sliding window protocol, 3-way handshake, TCP Tahoe & Reno congestion algorithms.",
                    file_path="/static/uploads/materials/sample_cn_unit4.pdf",
                    uploaded_by=admin_id
                ),
                StudyMaterial(
                    title="Unit 2: Trees, AVL Balancing & Graph Traversals",
                    subject="Data Structures & Algorithms",
                    department="cse",
                    semester=3,
                    description="C++ implementations and time complexity analysis of BFS, DFS, Dijkstra, and AVL rotations.",
                    file_path="/static/uploads/materials/sample_dsa_unit2.pdf",
                    uploaded_by=admin_id
                ),
                StudyMaterial(
                    title="Unit 1: Signals Classification & Fourier Transform Basics",
                    subject="Digital Signal Processing",
                    department="ece",
                    semester=5,
                    description="Discrete-time signals, stability criteria, and Z-transform inverse properties.",
                    file_path="/static/uploads/materials/sample_dsp_unit1.pdf",
                    uploaded_by=admin_id
                ),
            ]
            for m in materials:
                db.session.add(m)
            print(f"Added {len(materials)} study materials.")

        # Check if notices already exist
        if Notice.query.count() == 0:
            notices = [
                Notice(
                    title="B.Tech IV & VI Semester Mid-II Examination Timetable Announced",
                    content="The Mid-II examinations for 2nd and 3rd year B.Tech students will commence from 15th November 2026. Hall tickets can be collected from the respective department examination branches.",
                    department="Campus",
                    author_id=admin_id,
                    is_approved=True,
                    is_ingested_to_kg=True
                ),
                Notice(
                    title="Major Project Review-2 Schedule for CSE & Allied Branches",
                    content="All final year B.Tech CSE, AIML, and DS students must submit their complete implementation code, UML documentation, and presentation PPTs by November 5th. Presentations begin on November 8th.",
                    department="cse",
                    author_id=admin_id,
                    is_approved=True,
                    is_ingested_to_kg=True
                ),
                Notice(
                    title="Campus Placement Drive: TCS Digital & Infosys Specialist Programmer",
                    content="Eligible 7th semester students with CGPA >= 7.0 and no active backlogs are instructed to register on the T&P portal before October 31st for upcoming virtual assessment rounds.",
                    department="Campus",
                    author_id=admin_id,
                    is_approved=True,
                    is_ingested_to_kg=True
                ),
                Notice(
                    title="National Level 24-Hour Hackathon 'SPHN-Hacks 2026'",
                    content="The Department of CSE in collaboration with CSI Student Chapter is organizing a 24-hour national hackathon on December 2nd. Prizes worth Rs. 1,00,000/- up for grabs. Registration opens next week.",
                    department="cse",
                    author_id=admin_id,
                    is_approved=True,
                    is_ingested_to_kg=True
                )
            ]
            for n in notices:
                db.session.add(n)
            print(f"Added {len(notices)} notices.")

        db.session.commit()
        print("Database seeded successfully with initial materials and notices!")

if __name__ == '__main__':
    seed_data()

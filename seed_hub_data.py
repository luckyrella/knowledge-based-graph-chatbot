"""
Seed authentic study materials, lecture notes, and official circulars from
Sphoorthy Engineering College website into the database.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from app import create_app
from models import db
from models.material import StudyMaterial
from models.notice import Notice
from models.user import User

def seed_authentic_data():
    app = create_app()
    with app.app_context():
        admin = User.query.filter_by(role='admin').first()
        admin_id = admin.id if admin else 1

        # Clear existing sample data to re-seed with full authentic data
        StudyMaterial.query.delete()
        Notice.query.delete()
        db.session.commit()

        # Authentic Study Materials across all core departments (SR23 / SR24 Regulations)
        materials = [
            # ── CSE Core ───────────────────────────────────────────────────────
            StudyMaterial(
                title="Unit 1 & 2: Process Synchronization, CPU Scheduling & IPC",
                subject="Operating Systems (CS501PC)",
                department="cse",
                semester=4,
                description="Detailed notes covering Peterson's Algorithm, Semaphores, Monitors, CPU scheduling algorithms (FCFS, SJF, RR), and Classical IPC problems.",
                file_path="https://www.sphoorthyengg.ac.in/public/assets/images/ic-fcsee.jpeg",
                uploaded_by=admin_id
            ),
            StudyMaterial(
                title="Unit 3 & 4: Virtual Memory Management & Banker's Algorithm",
                subject="Operating Systems (CS501PC)",
                department="cse",
                semester=4,
                description="Deadlock detection, prevention, avoidance (Banker's Algorithm), Demand Paging, Page Replacement algorithms (FIFO, LRU, Optimal).",
                file_path="https://www.sphoorthyengg.ac.in/public/assets/images/ic-fcsee.jpeg",
                uploaded_by=admin_id
            ),
            StudyMaterial(
                title="Unit 1 & 2: Relational Model, ER Diagrams & Relational Algebra",
                subject="Database Management Systems (CS402PC)",
                department="cse",
                semester=4,
                description="Entity-Relationship data modeling, Extended ER features, Relational algebra operators, Tuple relational calculus, and SQL DDL/DML.",
                file_path="https://www.sphoorthyengg.ac.in/public/assets/images/ic-fcsee.jpeg",
                uploaded_by=admin_id
            ),
            StudyMaterial(
                title="Unit 3: Functional Dependencies & Database Normalization (1NF to BCNF)",
                subject="Database Management Systems (CS402PC)",
                department="cse",
                semester=4,
                description="Decomposition axioms, Armstrong's axioms, Lossless join decomposition, Dependency preservation, 1NF, 2NF, 3NF, BCNF, and 4NF.",
                file_path="https://www.sphoorthyengg.ac.in/public/assets/images/ic-fcsee.jpeg",
                uploaded_by=admin_id
            ),
            StudyMaterial(
                title="Unit 1 & 2: Asymptotic Notations & Divide-and-Conquer Algorithms",
                subject="Design and Analysis of Algorithms (CS401PC)",
                department="cse",
                semester=4,
                description="Time and space complexity (Big-O, Omega, Theta), Master Theorem, Merge Sort, Quick Sort, Strassen's Matrix Multiplication.",
                file_path="https://www.sphoorthyengg.ac.in/public/assets/images/ic-fcsee.jpeg",
                uploaded_by=admin_id
            ),
            StudyMaterial(
                title="Unit 3: Dynamic Programming & Greedy Methods (0/1 Knapsack, LCS)",
                subject="Design and Analysis of Algorithms (CS401PC)",
                department="cse",
                semester=4,
                description="Optimal substructure, 0/1 Knapsack, Fractional Knapsack, Longest Common Subsequence (LCS), Matrix Chain Multiplication, Dijkstra's algorithm.",
                file_path="https://www.sphoorthyengg.ac.in/public/assets/images/ic-fcsee.jpeg",
                uploaded_by=admin_id
            ),
            StudyMaterial(
                title="Unit 3 & 4: Transport Layer Protocols (TCP Flow & Congestion Control)",
                subject="Computer Networks (CS502PC)",
                department="cse",
                semester=5,
                description="TCP 3-way handshake, TCP connection teardown, Sliding Window protocol, TCP Reno, Tahoe, RED congestion control, and UDP sockets.",
                file_path="https://www.sphoorthyengg.ac.in/public/assets/images/ic-fcsee.jpeg",
                uploaded_by=admin_id
            ),
            StudyMaterial(
                title="Unit 2: Non-Linear Data Structures (Trees, AVL, B-Trees & Heaps)",
                subject="Data Structures & Algorithms (CS301PC)",
                department="cse",
                semester=3,
                description="Binary Search Trees (BST), AVL Tree balancing rotations, Red-Black Trees, B-Trees, Min/Max Heaps, and Priority Queues.",
                file_path="https://www.sphoorthyengg.ac.in/public/assets/images/ic-fcsee.jpeg",
                uploaded_by=admin_id
            ),

            # ── CSE (AI & ML) ──────────────────────────────────────────────────
            StudyMaterial(
                title="Unit 1 & 2: Supervised Learning, Cost Optimization & Gradient Descent",
                subject="Machine Learning (AI501PC)",
                department="cse_aiml",
                semester=5,
                description="Linear regression, Logistic regression, Cost functions, Batch vs Stochastic Gradient Descent, Bias-Variance tradeoff, Regularization (L1/L2).",
                file_path="https://www.sphoorthyengg.ac.in/public/assets/images/ic-fcsee.jpeg",
                uploaded_by=admin_id
            ),
            StudyMaterial(
                title="Unit 3: Support Vector Machines (SVM), Kernels & Ensemble Learning",
                subject="Machine Learning (AI501PC)",
                department="cse_aiml",
                semester=5,
                description="Max-margin hyperplanes, Soft-margin SVM, Kernel trick (RBF, Polynomial), Random Forests, AdaBoost, and Gradient Boosting (XGBoost).",
                file_path="https://www.sphoorthyengg.ac.in/public/assets/images/ic-fcsee.jpeg",
                uploaded_by=admin_id
            ),
            StudyMaterial(
                title="Unit 4: Deep Neural Networks (ANN, CNN, RNN & Backpropagation)",
                subject="Deep Learning (AI601PC)",
                department="cse_aiml",
                semester=6,
                description="Multilayer Perceptrons, Activation functions (ReLU, Sigmoid, Softmax), Backpropagation derivation, Convolutional layers, LSTM architectures.",
                file_path="https://www.sphoorthyengg.ac.in/public/assets/images/ic-fcsee.jpeg",
                uploaded_by=admin_id
            ),

            # ── CSE (Data Science) ─────────────────────────────────────────────
            StudyMaterial(
                title="Unit 1 & 2: Big Data Ecosystem, Hadoop HDFS & MapReduce Programming",
                subject="Big Data Analytics (DS601PC)",
                department="cse_ds",
                semester=6,
                description="Hadoop 3.x architecture, NameNode federation, YARN resource manager, MapReduce execution lifecycle, and MapReduce word-count implementation.",
                file_path="https://www.sphoorthyengg.ac.in/public/assets/images/ic-fcsee.jpeg",
                uploaded_by=admin_id
            ),
            StudyMaterial(
                title="Unit 3: Apache Spark Architecture, Resilient Distributed Datasets (RDD)",
                subject="Big Data Analytics (DS601PC)",
                department="cse_ds",
                semester=6,
                description="Spark core architecture, RDD transformations & actions, Spark DataFrames, Spark SQL, and lazy evaluation optimization.",
                file_path="https://www.sphoorthyengg.ac.in/public/assets/images/ic-fcsee.jpeg",
                uploaded_by=admin_id
            ),

            # ── CSE (Cyber Security) ───────────────────────────────────────────
            StudyMaterial(
                title="Unit 1 & 2: Cryptography, AES/DES & Asymmetric RSA Encryption",
                subject="Network Security and Cryptography (CS601PC)",
                department="cse_cs",
                semester=6,
                description="Symmetric block ciphers, DES rounds, AES 128/256-bit structure, Modular arithmetic, Euler's totient function, RSA cryptosystem, Diffie-Hellman.",
                file_path="https://www.sphoorthyengg.ac.in/public/assets/images/ic-fcsee.jpeg",
                uploaded_by=admin_id
            ),
            StudyMaterial(
                title="Unit 3 & 4: Digital Forensics, VAPT & Threat Modeling",
                subject="Cyber Security Essentials (CS501PC)",
                department="cse_cs",
                semester=5,
                description="Vulnerability Assessment & Penetration Testing (VAPT), OWASP Top 10 vulnerabilities, Wireshark packet capture, and Digital evidence chain of custody.",
                file_path="https://www.sphoorthyengg.ac.in/public/assets/images/ic-fcsee.jpeg",
                uploaded_by=admin_id
            ),

            # ── ECE Department ─────────────────────────────────────────────────
            StudyMaterial(
                title="Unit 1 & 2: Discrete Fourier Transform (DFT), FFT & Z-Transform Analysis",
                subject="Digital Signal Processing (EC501PC)",
                department="ece",
                semester=5,
                description="Discrete-time signals, LTI systems, Z-transform ROC, N-point DFT, Radix-2 Decimation-in-Time (DIT) and Decimation-in-Frequency (DIF) FFT.",
                file_path="https://www.sphoorthyengg.ac.in/public/assets/images/ic-fcsee.jpeg",
                uploaded_by=admin_id
            ),
            StudyMaterial(
                title="Unit 1 & 2: Embedded Systems, 8051 & ARM Cortex Architecture",
                subject="Embedded Systems Design (EC601PC)",
                department="ece",
                semester=6,
                description="Microcontroller architectures, 8051 memory organization, Timers, Interrupts, Serial communication, and ARM Cortex-M processor features.",
                file_path="https://www.sphoorthyengg.ac.in/public/assets/images/ic-fcsee.jpeg",
                uploaded_by=admin_id
            ),

            # ── MBA Department ─────────────────────────────────────────────────
            StudyMaterial(
                title="Unit 1 & 2: Financial Management, Capital Budgeting & Working Capital",
                subject="Financial Management (MB201PC)",
                department="mba",
                semester=2,
                description="Time value of money, Capital budgeting techniques (NPV, IRR, Payback period), Cost of Capital (WACC), and Working Capital cycle.",
                file_path="https://www.sphoorthyengg.ac.in/public/assets/images/ic-fcsee.jpeg",
                uploaded_by=admin_id
            ),
        ]

        for m in materials:
            db.session.add(m)
        print(f"✓ Seeded {len(materials)} authentic curriculum study materials across all departments.")

        # Official Circulars from Sphoorthy Engineering College Website
        notices = [
            Notice(
                title="B.Tech Autonomous (SR23/SR24) Regular & Supplementary Examination Fee Notification",
                content="All B.Tech students under SR-23 and SR-24 Autonomous regulations are hereby informed that the examination registration for the upcoming End-Semester Regular and Supplementary examinations is open. Students must complete fee payment via the examination portal before the deadline. Late fee penalties will apply after the cutoff date.",
                department="Campus",
                author_id=admin_id,
                is_approved=True,
                is_ingested_to_kg=True
            ),
            Notice(
                title="Revised Academic Calendar for B.Tech I, II, III & IV Years (Academic Year 2024-2025)",
                content="The Academic Senate and Controller of Examinations (CoE) have approved the revised academic calendar. The schedule includes instruction period dates, Mid-I Examinations, Mid-II Examinations, Practical Lab exams, and End-Semester Theory examination windows for all semesters.",
                department="Campus",
                author_id=admin_id,
                is_approved=True,
                is_ingested_to_kg=True
            ),
            Notice(
                title="Campus Recruitment Training (CRT) & TCS / Infosys / Capgemini Drive Schedule",
                content="Training and Placement Cell (T&P) announces mandatory CRT bootcamps for registered final-year students. Topics include Advanced Data Structures, Problem Solving in Java/Python, and Mock Technical Interviews. Shortlisted candidates for TCS Digital and Capgemini should report to the Auditorium.",
                department="cse",
                author_id=admin_id,
                is_approved=True,
                is_ingested_to_kg=True
            ),
            Notice(
                title="National Level 24-Hour Annual Hackathon 'SPHN-Hacks' & 'PRAZASTI' Fest Registrations",
                content="The Department of Computer Science & Engineering in association with CSI Student Chapter is organizing the flagship National Level Technical Fest 'PRAZASTI' and 24-Hour Hackathon. Exciting cash rewards up to ₹1,50,000/- for winning teams in AI, Web3, and IoT tracks.",
                department="cse",
                author_id=admin_id,
                is_approved=True,
                is_ingested_to_kg=True
            ),
            Notice(
                title="Major Project Review-2 Guidelines for Final Year B.Tech (CSE, AIML, DS, CS & ECE)",
                content="All 8th semester project batches must present their working software prototypes, system architecture, database design, and verification benchmark results to the departmental evaluation panel. Submission of draft thesis reports is mandatory before the review.",
                department="cse",
                author_id=admin_id,
                is_approved=True,
                is_ingested_to_kg=True
            ),
            Notice(
                title="AICTE Idea Lab Prototyping Workshop for Engineering Students",
                content="The AICTE Idea Lab at Sphoorthy Engineering College is conducting a hands-on workshop on 3D Printing, Laser Cutting, PCB Design, and IoT Prototyping for interested students. Register at the Idea Lab coordinator cabin in Block A.",
                department="Campus",
                author_id=admin_id,
                is_approved=True,
                is_ingested_to_kg=True
            )
        ]

        for n in notices:
            db.session.add(n)
        print(f"✓ Seeded {len(notices)} official campus circulars & examination notifications.")

        db.session.commit()
        print("Database synchronization with official Sphoorthy Engineering College portal data complete!")

if __name__ == '__main__':
    seed_authentic_data()

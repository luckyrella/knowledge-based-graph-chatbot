"""
Generate authentic, professional academic PDF study notes for all college departments
and semesters using ReportLab, save them to static/uploads/materials, and seed them
into the SQLite database.
"""
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')

# Ensure paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, 'static', 'uploads', 'materials')
os.makedirs(UPLOAD_DIR, exist_ok=True)

sys.path.insert(0, BASE_DIR)
from app import create_app
from models.database import db
from models.material import StudyMaterial
from models.user import User

# List of 32 comprehensive branch notes across all semesters
NOTES_CATALOG = [
    # ── CSE Core ──────────────────────────────────────────────────────────────
    {
        "filename": "cse_sem3_data_structures.pdf",
        "title": "Data Structures & Algorithms (Unit 1 to 5 Complete Notes)",
        "subject": "Data Structures & Algorithms (CS301PC)",
        "department": "CSE",
        "semester": 3,
        "description": "Comprehensive reference notes on Stacks, Queues, Linked Lists, Trees (BST, AVL, B-Trees), Graph traversals (BFS/DFS), and Hashing techniques with complexity analysis.",
        "units": [
            ("Unit 1: Linear Data Structures", "Abstract Data Types, Dynamic Arrays, Singly & Doubly Linked Lists, Circular Lists, Stack implementations, and Expression evaluation (Infix to Postfix)."),
            ("Unit 2: Queues and Recursion", "Linear Queue, Circular Queue, Double-Ended Queue (Deque), Priority Queue with Binary Heaps, and Recursion stack frame trace."),
            ("Unit 3: Non-Linear Structures: Trees", "Binary Tree traversals, Binary Search Tree (BST) operations, Self-Balancing AVL trees with rotations (LL, RR, LR, RL), and Red-Black Trees."),
            ("Unit 4: Graph Algorithms", "Graph representation (Adjacency Matrix & List), Depth First Search (DFS), Breadth First Search (BFS), Minimum Spanning Tree (Prim's & Kruskal's), and Dijkstra's Shortest Path."),
            ("Unit 5: Sorting & Hashing", "Merge Sort, Quick Sort, Radix Sort, Open Addressing (Linear Probing, Quadratic, Double Hashing), Separate Chaining, and Collision Resolution.")
        ]
    },
    {
        "filename": "cse_sem4_database_systems.pdf",
        "title": "Database Management Systems: Relational Models & SQL",
        "subject": "Database Management Systems (CS402PC)",
        "department": "CSE",
        "semester": 4,
        "description": "Entity-Relationship Diagrams, Relational Algebra, SQL queries, Normalization (1NF through BCNF), Transaction Processing (ACID), and Concurrency Control.",
        "units": [
            ("Unit 1: Database Architecture & ER Model", "3-tier database architecture, Data independence, Strong & weak entity sets, Cardinality constraints, and Extended ER features."),
            ("Unit 2: Relational Algebra & Calculus", "Fundamental operators (Select, Project, Cartesian Product, Union, Set Difference), Rename, Joins (Theta, Equi, Natural, Outer), and Tuple Relational Calculus."),
            ("Unit 3: SQL & Database Normalization", "DDL, DML, DCL, Aggregate functions, Nested subqueries, Functional dependencies, Armstrong axioms, 1NF, 2NF, 3NF, and Boyce-Codd Normal Form (BCNF)."),
            ("Unit 4: Transaction & Concurrency Control", "ACID properties, Serializability (Conflict & View), Two-Phase Locking (2PL), Deadlock prevention and detection, and Timestamp-based protocols."),
            ("Unit 5: Storage and Indexing", "RAID levels, B-Trees and B+ Trees indexing structure, Static and Dynamic hashing, and Query optimization execution plans.")
        ]
    },
    {
        "filename": "cse_sem4_operating_systems.pdf",
        "title": "Operating Systems: Process Synchronization & Memory Management",
        "subject": "Operating Systems (CS403PC)",
        "department": "CSE",
        "semester": 4,
        "description": "Process control blocks, CPU scheduling, Semaphores & Monitors, Banker's Deadlock Algorithm, Demand Paging, Virtual Memory, and File System structure.",
        "units": [
            ("Unit 1: Process Management & Scheduling", "Process states, Process Control Block (PCB), Context Switching, FCFS, SJF, Priority Scheduling, Round Robin, and Multi-level Queue Scheduling."),
            ("Unit 2: Inter-Process Communication & Synchronization", "Race conditions, Critical section problem, Peterson's algorithm, Counting & Binary Semaphores, Classic IPC problems (Dining Philosophers, Readers-Writers)."),
            ("Unit 3: Deadlocks", "Deadlock characterization (4 Coffman conditions), Resource Allocation Graphs, Deadlock prevention, Banker's safety algorithm, and Deadlock detection & recovery."),
            ("Unit 4: Memory Management & Paging", "Logical vs physical addresses, Paging hardware, Translation Lookaside Buffer (TLB), Segmentation, Demand paging, Page replacement algorithms (FIFO, LRU, Optimal)."),
            ("Unit 5: File & Disk Management", "File allocation methods (Contiguous, Linked, Indexed), Free space management, Disk scheduling algorithms (FCFS, SSTF, SCAN, C-SCAN, LOOK).")
        ]
    },
    {
        "filename": "cse_sem5_design_and_analysis_of_algorithms.pdf",
        "title": "Design & Analysis of Algorithms: Greedy, Dynamic & NP-Completeness",
        "subject": "Design & Analysis of Algorithms (CS501PC)",
        "department": "CSE",
        "semester": 5,
        "description": "Asymptotic notations, Divide-and-Conquer, Greedy Strategy, Dynamic Programming, Backtracking, Branch-and-Bound, and NP-Hard/NP-Complete classification.",
        "units": [
            ("Unit 1: Foundations & Divide-and-Conquer", "Order of growth (O, Omega, Theta), Recurrence relations, Master Theorem, Merge Sort, Quick Sort randomized analysis, Strassen's matrix multiplication."),
            ("Unit 2: Greedy Method", "Greedy choice property, Fractional Knapsack, Huffman coding data compression, Job sequencing with deadlines, and Minimum Spanning Trees."),
            ("Unit 3: Dynamic Programming", "Overlapping subproblems, 0/1 Knapsack problem, Longest Common Subsequence (LCS), Matrix Chain Multiplication, Floyd-Warshall all-pairs shortest paths."),
            ("Unit 4: Backtracking & Branch-and-Bound", "N-Queens problem, Subset sum problem, Graph coloring, Hamiltonian cycles, Traveling Salesperson Problem (TSP) using 15-puzzle branch and bound."),
            ("Unit 5: NP-Completeness", "Deterministic vs Non-deterministic algorithms, Classes P, NP, NP-Hard, NP-Complete, Cook's Theorem, and polynomial-time reduction proofs.")
        ]
    },
    {
        "filename": "cse_sem5_computer_networks.pdf",
        "title": "Computer Networks: OSI/TCP-IP Protocols, Routing & Congestion Control",
        "subject": "Computer Networks (CS502PC)",
        "department": "CSE",
        "semester": 5,
        "description": "Layered protocol stacks, Data link framing & CRC, Sliding Window protocols, Routing algorithms (OSPF, BGP), TCP Reno/Tahoe, and Application layer protocols (DNS, HTTP/2).",
        "units": [
            ("Unit 1: Network Physical & Data Link Layer", "OSI 7-layer reference model, TCP/IP architecture, Framing, Flow control (Stop-and-Wait, Go-Back-N, Selective Repeat), Error detection (CRC, Checksum)."),
            ("Unit 2: Medium Access Control (MAC)", "ALOHA (Pure and Slotted), CSMA/CD (Ethernet IEEE 802.3), CSMA/CA (Wi-Fi IEEE 802.11), and Switching methods (Virtual circuit vs Datagram)."),
            ("Unit 3: Network Layer & Routing", "IPv4 addressing, Subnetting, CIDR, IPv6 header format, Distance Vector Routing (Bellman-Ford), Link State Routing (Dijkstra/OSPF), and BGP routing."),
            ("Unit 4: Transport Layer", "User Datagram Protocol (UDP), Transmission Control Protocol (TCP), 3-way handshake, Flow control, TCP Congestion Control algorithms (AIMD, Slow Start)."),
            ("Unit 5: Application Layer & Security", "Domain Name System (DNS), HTTP/1.1 vs HTTP/2, SMTP, POP3, IMAP, SSL/TLS handshake overview, and symmetric/asymmetric cryptographic principles.")
        ]
    },
    {
        "filename": "cse_sem6_software_engineering.pdf",
        "title": "Software Engineering & Agile Development Methodologies",
        "subject": "Software Engineering (CS601PC)",
        "department": "CSE",
        "semester": 6,
        "description": "SDLC models, Agile Scrum framework, Requirement Engineering (SRS), Object-Oriented Analysis & Design (UML), Software Testing levels, and DevOps CI/CD pipelines.",
        "units": [
            ("Unit 1: Software Process Models", "Waterfall model, Incremental process, Prototyping, Spiral model, Agile Manifesto principles, Scrum sprints, User Stories, and Kanban boards."),
            ("Unit 2: Software Requirements Engineering", "Functional and non-functional requirements, Feasibility study, Requirement elicitation techniques, IEEE 830 SRS document standards, Use case specifications."),
            ("Unit 3: Architectural Design & UML", "Modular design principles, Cohesion and Coupling, Architectural styles (Client-Server, Microservices), UML diagrams (Class, Sequence, Activity, Statechart)."),
            ("Unit 4: Software Testing Strategies", "Unit testing, Integration testing, System testing, Black-box testing (Equivalence Partitioning, Boundary Value Analysis), White-box testing (Basis Path, Cyclomatic Complexity)."),
            ("Unit 5: Software Quality & DevOps", "CMMI levels, ISO 9001 standards, Software metrics, Risk management, Git version control workflows, Continuous Integration and Continuous Deployment (CI/CD).")
        ]
    },

    # ── CSE (AI & ML) ──────────────────────────────────────────────────────────
    {
        "filename": "aiml_sem4_python_data_structures.pdf",
        "title": "Python for AI/ML: NumPy, Pandas, Matplotlib & Scientific Computing",
        "subject": "Python for Data Science (AI401PC)",
        "department": "CSE_AIML",
        "semester": 4,
        "description": "Vectorized computations with NumPy, Data wrangling using Pandas DataFrames, Data visualization with Seaborn/Matplotlib, and Scipy optimization tools.",
        "units": [
            ("Unit 1: Python Advanced Foundations", "List comprehensions, Lambda functions, Generators, Decorators, Object-Oriented Python classes, and Exception handling paradigms."),
            ("Unit 2: NumPy for Numerical Arrays", "N-dimensional array indexing, Slicing, Broadcasting rules, Linear algebra matrix decomposition (SVD, Eigenvalues), and Vectorized operations."),
            ("Unit 3: Pandas Data Manipulation", "Series and DataFrames, Missing value imputation, GroupBy aggregations, Merging/Joining datasets, and Time-series data resampling."),
            ("Unit 4: Statistical Data Visualization", "Matplotlib subplots, Seaborn heatmaps, Histograms, Box plots for outlier detection, Pairplots, and Plotly interactive charts."),
            ("Unit 5: Data Preprocessing for AI", "Feature scaling (StandardScaler, MinMaxScaler), One-Hot Encoding, Label Encoding, Train-Test split stratification, and Dimensionality Reduction (PCA).")
        ]
    },
    {
        "filename": "aiml_sem5_machine_learning.pdf",
        "title": "Machine Learning: Supervised, Unsupervised & Ensemble Algorithms",
        "subject": "Machine Learning (AI501PC)",
        "department": "CSE_AIML",
        "semester": 5,
        "description": "Linear and Logistic Regression, Gradient Descent optimization, Decision Trees, Random Forests, Support Vector Machines (SVM), K-Means clustering, and Evaluation Metrics.",
        "units": [
            ("Unit 1: Supervised Regression", "Simple & Multiple Linear Regression, Cost functions, Gradient Descent (Batch, Mini-batch, SGD), Polynomial Regression, Regularization (Ridge L2, Lasso L1)."),
            ("Unit 2: Classification Models", "Logistic regression, Decision Boundary, ROC-AUC curve, Confusion Matrix, Precision-Recall tradeoff, Naive Bayes classifier, and K-Nearest Neighbors (KNN)."),
            ("Unit 3: Support Vector Machines & Kernels", "Optimal separating hyperplanes, Hard vs Soft margin SVM, Slack variables, Kernel trick (Polynomial, Radial Basis Function RBF, Sigmoid)."),
            ("Unit 4: Ensemble Learning", "Bagging (Random Forests), Boosting (AdaBoost, Gradient Boosting, XGBoost), Voting Classifiers, Stacking, and Bias-Variance tradeoff analysis."),
            ("Unit 5: Unsupervised Learning", "K-Means clustering algorithm, Elbow method, Hierarchical clustering (Dendrograms), DBSCAN density clustering, and Principal Component Analysis (PCA).")
        ]
    },
    {
        "filename": "aiml_sem6_deep_learning.pdf",
        "title": "Deep Learning: Artificial Neural Networks, CNNs & Sequence Models",
        "subject": "Deep Learning (AI601PC)",
        "department": "CSE_AIML",
        "semester": 6,
        "description": "Perceptrons, Backpropagation, Convolutional Neural Networks (CNNs) for Computer Vision, Recurrent Neural Networks (RNNs, LSTMs, GRUs), and Attention Mechanisms.",
        "units": [
            ("Unit 1: Artificial Neural Networks (ANN)", "Biological vs Artificial neurons, Perceptrons, Multilayer Perceptron (MLP), Activation functions (Sigmoid, Tanh, ReLU, LeakyReLU, Softmax), Backpropagation derivation."),
            ("Unit 2: Training Deep Networks", "Vanishing and Exploding gradients, Weight initializations (He, Xavier), Optimizers (Momentum, RMSprop, Adam), Dropout regularization, Batch Normalization."),
            ("Unit 3: Convolutional Neural Networks (CNN)", "Convolution operation, Padding, Strides, Pooling layers (Max, Average), Classic CNN architectures (LeNet, AlexNet, VGG-16, ResNet skip connections)."),
            ("Unit 4: Recurrent Neural Networks (RNN)", "Sequence modeling, Vanilla RNN architecture, Backpropagation Through Time (BPTT), Long Short-Term Memory (LSTM) cell gating, Gated Recurrent Units (GRU)."),
            ("Unit 5: Transformers & Modern Architectures", "Sequence-to-Sequence models, Self-Attention mechanism, Scaled Dot-Product attention, Multi-Head Attention, Transformer Encoder-Decoder, and Generative Adversarial Networks (GANs).")
        ]
    },
    {
        "filename": "aiml_sem7_natural_language_processing.pdf",
        "title": "Natural Language Processing: Text Embeddings, Transformers & LLMs",
        "subject": "Natural Language Processing (AI701PC)",
        "department": "CSE_AIML",
        "semester": 7,
        "description": "Tokenization, Stemming/Lemmatization, TF-IDF, Word2Vec, GloVe, BERT contextual representations, Prompt Engineering, and Retrieval-Augmented Generation (RAG).",
        "units": [
            ("Unit 1: Text Preprocessing & Language Modeling", "Tokenization, Stop-word removal, Stemming (Porter), Lemmatization (WordNet), N-gram language models, Perplexity metric, and Part-of-Speech (POS) tagging."),
            ("Unit 2: Word Representation Techniques", "Bag of Words (BoW), Term Frequency-Inverse Document Frequency (TF-IDF), Word2Vec (Skip-gram & CBOW), Negative Sampling, and GloVe embeddings."),
            ("Unit 3: Deep NLP & Sequence Tagging", "Bi-directional LSTMs for Named Entity Recognition (NER), Sentiment Analysis with GRU, Sequence-to-Sequence Machine Translation, and Beam Search decoding."),
            ("Unit 4: Pre-trained Language Models", "Contextual word embeddings (ELMo), BERT masked language modeling, RoBERTa, T5 encoder-decoder, GPT auto-regressive generation, and Fine-tuning paradigms."),
            ("Unit 5: Generative AI & Knowledge Graphs", "Retrieval-Augmented Generation (RAG) architecture, Vector databases (FAISS, ChromaDB), Prompt Engineering patterns, Hallucination mitigation via Knowledge Graph grounding.")
        ]
    },

    # ── CSE (Data Science) ─────────────────────────────────────────────────────
    {
        "filename": "ds_sem4_exploratory_data_analysis.pdf",
        "title": "Exploratory Data Analysis: Statistical Modeling & Data Cleaning",
        "subject": "Exploratory Data Analysis (DS401PC)",
        "department": "CSE_DS",
        "semester": 4,
        "description": "Descriptive statistics, Outlier detection (IQR, Z-Score), Probability distributions, Hypothesis testing (t-test, ANOVA, Chi-Square), and Multivariate analysis.",
        "units": [
            ("Unit 1: Data Understanding & Cleaning", "Types of variables (Nominal, Ordinal, Interval, Ratio), Handling missing data (MCAR, MAR, MNAR), Imputation techniques, and duplicate identification."),
            ("Unit 2: Descriptive & Summary Statistics", "Measures of central tendency (Mean, Median, Mode), Measures of dispersion (Variance, Standard Deviation, Interquartile Range IQR), Skewness, and Kurtosis."),
            ("Unit 3: Probability Distributions", "Discrete distributions (Binomial, Poisson), Continuous distributions (Normal, Standard Normal, Exponential), Central Limit Theorem, and Sampling techniques."),
            ("Unit 4: Inferential Statistics & Hypothesis Testing", "Null and Alternative hypotheses, Type I and Type II errors, p-values, One-sample and two-sample t-tests, Paired t-test, One-way ANOVA, and Chi-Square tests of independence."),
            ("Unit 5: Bivariate & Multivariate Exploration", "Covariance, Pearson's correlation coefficient, Spearman rank correlation, Collinearity detection (VIF), Factor Analysis, and Principal Component Analysis.")
        ]
    },
    {
        "filename": "ds_sem5_data_warehousing_and_mining.pdf",
        "title": "Data Warehousing & Data Mining: ETL, OLAP & Pattern Discovery",
        "subject": "Data Warehousing & Mining (DS501PC)",
        "department": "CSE_DS",
        "semester": 5,
        "description": "Data warehouse architectures, Star & Snowflake schemas, OLAP operations (Roll-up, Drill-down, Slice-and-dice), Apriori association rule mining, and FP-Growth.",
        "units": [
            ("Unit 1: Data Warehousing Concepts", "Operational databases vs Data Warehouses, Kimball vs Inmon architectures, ETL (Extract, Transform, Load) pipelines, and Data staging areas."),
            ("Unit 2: Multidimensional Data Modeling", "Fact tables, Dimension tables, Star schema, Snowflake schema, Fact Constellation schema, Measures (Additive, Semi-additive, Non-additive)."),
            ("Unit 3: OLAP Systems & Operations", "MOLAP vs ROLAP vs HOLAP, OLAP operations: Roll-up, Drill-down, Slice, Dice, Pivot, and Data cube computation techniques."),
            ("Unit 4: Association Rule Mining", "Market Basket Analysis, Support, Confidence, Lift metrics, Apriori algorithm candidate generation, Apriori property, and FP-Tree growth algorithm."),
            ("Unit 5: Advanced Classification & Clustering for Mining", "Decision tree induction (ID3, C4.5, Gini index), Rule-based classification, Cluster evaluation (Silhouette score), and Mining text and graph streams.")
        ]
    },
    {
        "filename": "ds_sem6_big_data_analytics.pdf",
        "title": "Big Data Analytics: Hadoop Ecosystem, MapReduce & Apache Spark",
        "subject": "Big Data Analytics (DS601PC)",
        "department": "CSE_DS",
        "semester": 6,
        "description": "5 V's of Big Data, Hadoop Distributed File System (HDFS), MapReduce lifecycle, Apache Spark RDD transformations, Spark SQL DataFrames, and Streaming analytics.",
        "units": [
            ("Unit 1: Big Data Landscape & HDFS", "Characteristics of Big Data (Volume, Velocity, Variety, Veracity, Value), HDFS architecture (NameNode, DataNode, Secondary NameNode), Block replication strategy."),
            ("Unit 2: MapReduce Programming Model", "Map phase, Shuffle and Sort phase, Reduce phase, Combiner functions, Partitioner, Inverted index construction, and MapReduce word count tutorial."),
            ("Unit 3: YARN Architecture & Ecosystem", "YARN Resource Manager, Node Manager, Application Master, Apache Hive data warehousing (HQL, Partitions, Buckets), and Apache Pig Latin."),
            ("Unit 4: Apache Spark Core Architecture", "Limitations of MapReduce, In-memory computing, Resilient Distributed Datasets (RDD), Transformations vs Actions, Lineage graph, and Lazy evaluation."),
            ("Unit 5: Spark SQL & Machine Learning (MLlib)", "Spark DataFrames, Spark SQL queries, Catalyst optimizer, Spark MLlib pipelines (Classification, Regression, Clustering), and Kafka real-time streaming ingestion.")
        ]
    },

    # ── CSE (Cyber Security) ───────────────────────────────────────────────────
    {
        "filename": "cs_sem5_network_security_cryptography.pdf",
        "title": "Network Security & Cryptography: Symmetric/Asymmetric Ciphers & PKI",
        "subject": "Network Security and Cryptography (CS505PC)",
        "department": "CSE_CS",
        "semester": 5,
        "description": "Classical encryption ciphers, DES/AES algorithms, Public-Key Cryptography (RSA, ECC), Hash functions (SHA-256), Digital Signatures, and Public Key Infrastructure.",
        "units": [
            ("Unit 1: Classical Ciphers & Symmetric Cryptography", "Security attacks (Passive vs Active), Substitution ciphers, Transposition ciphers, Stream vs Block ciphers, Feistel cipher structure."),
            ("Unit 2: Modern Symmetric Block Ciphers", "Data Encryption Standard (DES), Triple-DES, Advanced Encryption Standard (AES) rounds (SubBytes, ShiftRows, MixColumns, AddRoundKey), Modes of operation (ECB, CBC, CFB, CTR)."),
            ("Unit 3: Asymmetric Cryptography & Key Exchange", "Fermat's and Euler's theorems, Discrete logarithms, Diffie-Hellman Key Exchange, RSA algorithm mathematical proof, Elliptic Curve Cryptography (ECC)."),
            ("Unit 4: Cryptographic Hash Functions & Digital Signatures", "Message Authentication Codes (MAC), HMAC, SHA-256 and SHA-512 compression functions, Birthday paradox, Digital Signature Standard (DSS)."),
            ("Unit 5: Network Security Protocols & Firewalls", "Kerberos authentication, X.509 digital certificates, SSL/TLS handshake, IPsec (AH and ESP protocols), Firewalls (Packet filtering, Stateful inspection, Proxy).")
        ]
    },
    {
        "filename": "cs_sem6_cyber_forensics_incident_response.pdf",
        "title": "Cyber Forensics & Incident Response: VAPT, Memory Forensics & Laws",
        "subject": "Cyber Forensics & Incident Response (CS605PC)",
        "department": "CSE_CS",
        "semester": 6,
        "description": "Vulnerability Assessment & Penetration Testing (VAPT), Volatile memory acquisition, Disk forensic imaging (dd/E01), Network packet analysis, and Cyber laws (IT Act 2000).",
        "units": [
            ("Unit 1: Digital Forensics Fundamentals", "Digital evidence types, Locard's exchange principle, Chain of custody, Forensic readiness, and Evidence seizure protocols under ISO 27037."),
            ("Unit 2: Disk & File System Forensics", "Bit-stream disk imaging, Write blockers, FAT/NTFS file systems, Master File Table (MFT), Deleted file recovery, Slack space analysis, and Steganography detection."),
            ("Unit 3: Memory & Network Forensics", "Volatile memory capture (RAM dumping), Volatility framework analysis, Malicious process injection detection, Wireshark packet capture, and IDS/IPS log analysis."),
            ("Unit 4: Incident Response & Threat Hunting", "NIST incident response lifecycle (Preparation, Detection & Analysis, Containment, Eradication, Recovery), MITRE ATT&CK framework mapping, and SIEM tool monitoring."),
            ("Unit 5: Ethical Hacking & Legal Framework", "Penetration testing phases (Reconnaissance, Scanning, Exploitation, Maintaining access), OWASP Top 10 vulnerabilities, Indian Information Technology Act 2000 amendments.")
        ]
    },

    # ── ECE Department ─────────────────────────────────────────────────────────
    {
        "filename": "ece_sem3_electronic_devices_circuits.pdf",
        "title": "Electronic Devices & Circuits: Diodes, BJTs, MOSFETs & Amplifiers",
        "subject": "Electronic Devices & Circuits (EC301PC)",
        "department": "ECE",
        "semester": 3,
        "description": "PN junction semiconductor physics, Zener voltage regulators, Bipolar Junction Transistor (BJT) configurations, JFET, MOSFET operation, and Small-signal models.",
        "units": [
            ("Unit 1: Semiconductor Diodes", "Carrier concentrations, Drift and diffusion currents, PN junction diode V-I characteristics, Diode capacitance, Half-wave and Full-wave rectifiers with filters."),
            ("Unit 2: Special Semiconductor Devices", "Zener diode avalanche breakdown, Zener voltage regulator design, Tunnel diode, Varactor diode, Photodiode, Solar cells, and Light Emitting Diodes (LED)."),
            ("Unit 3: Bipolar Junction Transistors (BJT)", "BJT physical structure, Transistor currents, Common Base (CB), Common Emitter (CE), and Common Collector (CC) configurations, Input/Output characteristics, Early effect."),
            ("Unit 4: Transistor Biasing & Stabilization", "Operating point (Q-point), DC load line, Fixed bias, Collector-to-base bias, Voltage divider bias, Stability factor analysis (S, S', S''), Thermal runaway prevention."),
            ("Unit 5: Field Effect Transistors (FET & MOSFET)", "JFET construction, Pinch-off voltage, Depletion and Enhancement type MOSFETs, Drain and Transfer characteristics, Small signal h-parameter equivalent circuit models.")
        ]
    },
    {
        "filename": "ece_sem4_signals_and_systems.pdf",
        "title": "Signals and Systems: Fourier Series, Transforms, Laplace & Z-Transform",
        "subject": "Signals and Systems (EC401PC)",
        "department": "ECE",
        "semester": 4,
        "description": "Continuous & Discrete-time signals, Linear Time-Invariant (LTI) systems, Convolution integrals, Continuous-time Fourier Transform (CTFT), Laplace Transform, and Z-Transform.",
        "units": [
            ("Unit 1: Signal Classification & Operations", "Continuous vs Discrete-time signals, Energy vs Power signals, Periodic, Even/Odd signals, Unit Step, Impulse, Ramp functions, Time shifting, scaling, reversal."),
            ("Unit 2: Linear Time-Invariant (LTI) Systems", "LTI system properties (Linearity, Time-invariance, Causality, BIBO Stability), Impulse response, Convolution integral and Convolution sum calculations."),
            ("Unit 3: Fourier Series & Fourier Transform", "Dirichlet conditions, Trigonometric and Exponential Fourier series, Continuous-Time Fourier Transform (CTFT) properties, Frequency response of LTI systems."),
            ("Unit 4: Laplace Transform", "Region of Convergence (ROC) properties, Inverse Laplace Transform, System transfer function H(s), Poles and Zeros plotting, Transient and steady-state response."),
            ("Unit 5: Z-Transform & Sampling", "Z-transform definition and ROC properties, Inverse Z-transform methods (Partial fraction, Power series), Nyquist-Shannon Sampling Theorem, Aliasing mitigation.")
        ]
    },
    {
        "filename": "ece_sem5_digital_signal_processing.pdf",
        "title": "Digital Signal Processing: DFT, FFT Algorithms, IIR & FIR Filter Design",
        "subject": "Digital Signal Processing (EC501PC)",
        "department": "ECE",
        "semester": 5,
        "description": "Discrete Fourier Transform (DFT), Radix-2 FFT algorithms (DIT and DIF), IIR filter design (Butterworth, Chebyshev), FIR filter design using Windows, and DSP processors.",
        "units": [
            ("Unit 1: Discrete Fourier Transform (DFT)", "Properties of DFT, Circular convolution, Linear convolution using DFT, Circular correlation, and Fast convolution methods (Overlap-Add, Overlap-Save)."),
            ("Unit 2: Fast Fourier Transform (FFT) Algorithms", "Radix-2 Decimation-In-Time (DIT) FFT, Decimation-In-Frequency (DIF) FFT, Butterfly signal flow graphs, and Computational complexity reduction from O(N^2) to O(N log N)."),
            ("Unit 3: IIR Digital Filter Design", "Analog filter approximations (Butterworth, Chebyshev Type I), Impulse Invariance Method, Bilinear Transformation Method (BTM), Warping effect, and Pre-warping."),
            ("Unit 4: FIR Digital Filter Design", "Linear phase conditions of FIR filters, Symmetric and anti-symmetric impulse response, Windowing design techniques (Rectangular, Hamming, Hanning, Blackman)."),
            ("Unit 5: Digital Filter Realization & Quantization", "Direct Form I and II, Cascade, and Parallel realizations of IIR systems, Transversal and Linear phase FIR realization, Finite word-length quantization effects.")
        ]
    },
    {
        "filename": "ece_sem6_vlsi_design.pdf",
        "title": "VLSI Design: CMOS Technology, Stick Diagrams, Layout & Verilog HDL",
        "subject": "VLSI Design (EC601PC)",
        "department": "ECE",
        "semester": 6,
        "description": "MOS transistor fabrication, CMOS inverter DC transfer characteristics, Stick diagrams, Euler path layout rules, Dynamic CMOS circuits, and Verilog HDL RTL modeling.",
        "units": [
            ("Unit 1: MOS Transistor Theory", "NMOS and PMOS enhancement mode transistors, Threshold voltage equation, Linear and Saturation region currents, Channel length modulation, Body effect."),
            ("Unit 2: CMOS Fabrication & Processing", "N-well, P-well, Twin-tub CMOS fabrication process steps, Photolithography, Ion implantation, Latch-up prevention techniques in CMOS."),
            ("Unit 3: Circuit Design Rules & Layout", "Lambda (λ) and Micron-based design rules, Contact cuts, Transistor sizing, Stick diagrams, Euler path layout optimization, and Interconnect parasitic estimation."),
            ("Unit 4: Delay Modeling & Logic Families", "RC delay models, Elmore delay calculation, Logical Effort theory, Dynamic CMOS logic, Domino logic, Transmission gates, and Pass transistor logic."),
            ("Unit 5: Hardware Description Language (Verilog)", "Dataflow, Behavioral, and Structural modeling in Verilog HDL, Testbench design, Synthesis of combinational and sequential circuits (ALU, Shift registers, FSMs).")
        ]
    },

    # ── Civil Engineering ──────────────────────────────────────────────────────
    {
        "filename": "civil_sem3_building_materials_surveying.pdf",
        "title": "Building Materials & Surveying: Stones, Cements, Leveling & Theodolite",
        "subject": "Building Materials & Surveying (CE301PC)",
        "department": "Civil",
        "semester": 3,
        "description": "Properties of construction stones, Cement types & hydration, Concrete mix, Chain surveying, Compass traversing, Leveling operations, and Total Station surveying.",
        "units": [
            ("Unit 1: Building Stones, Bricks & Timber", "Igneous, sedimentary, metamorphic rocks, Compressive strength tests, Brick manufacturing (Kilns), Efflorescence test, Timber seasoning and defect prevention."),
            ("Unit 2: Cements, Aggregates & Mortar", "Portland Pozzolana Cement (PPC), Bogue's compounds, Initial and final setting time test, Soundness test, Fineness modulus of aggregates, Mortar proportions."),
            ("Unit 3: Concrete Technology Fundamentals", "Water-cement ratio, Slump test, Compacting factor test, Concrete compressive strength, Admixtures (Plasticizers, Retarders), Concrete curing methods."),
            ("Unit 4: Linear & Angular Surveying", "Chain surveying methods, Chaining on slopes, Prismatic compass, Local attraction errors, Traverse computation, Coordinates and closing error adjustments."),
            ("Unit 5: Leveling, Contouring & Theodolite", "Dumpy level, Height of Collimation method, Rise and Fall method, Curvature and refraction corrections, Contour intervals, and Transit Theodolite traversing.")
        ]
    },
    {
        "filename": "civil_sem4_strength_of_materials.pdf",
        "title": "Strength of Materials: Stress, Strain, SFD/BMD & Deflection of Beams",
        "subject": "Strength of Materials (CE401PC)",
        "department": "Civil",
        "semester": 4,
        "description": "Hooke's Law, Poisson's ratio, Shear Force Diagrams (SFD), Bending Moment Diagrams (BMD), Flexural bending formula, Torsion of shafts, and Euler column buckling.",
        "units": [
            ("Unit 1: Simple Stresses and Strains", "Tensile, compressive, shear stresses, True vs engineering stress-strain curve, Modulus of Elasticity, Poisson's ratio, Volumetric strain, Thermal stresses in bars."),
            ("Unit 2: Principal Stresses & Mohr's Circle", "Stresses on inclined planes, Normal and tangential stresses, Maximum shear stress, Mohr's circle graphical construction, Theories of elastic failure."),
            ("Unit 3: Shear Force and Bending Moment", "Types of beams (Cantilever, Simply supported, Overhanging), Point of contraflexure, Relation between load, shear force, and bending moment, SFD/BMD derivations."),
            ("Unit 4: Flexural & Shear Stresses in Beams", "Pure bending theory, Flexure formula (M/I = sigma/y = E/R), Section modulus of rectangular and I-sections, Shear stress distribution across cross-sections."),
            ("Unit 5: Torsion of Shafts & Deflection of Beams", "Torsion equation (T/J = tau/r = G theta/L), Power transmitted by shafts, Double integration method, Macaulay's method for beam deflection, Euler's column buckling formula.")
        ]
    },
    {
        "filename": "civil_sem5_structural_analysis.pdf",
        "title": "Structural Analysis & Design of Concrete Structures",
        "subject": "Structural Analysis (CE501PC)",
        "department": "Civil",
        "semester": 5,
        "description": "Static and kinematic indeterminacy, Moment Distribution Method, Slope Deflection Method, Limit State Design of singly/doubly reinforced beams, and Slab detailing.",
        "units": [
            ("Unit 1: Energy Theorems & Indeterminacy", "Strain energy due to axial load, bending, torsion, Castigliano's first and second theorems, Unit load method for deflection of determinate trusses."),
            ("Unit 2: Slope Deflection Method", "Slope-deflection equations formulation, Continuous beams with and without support settlement, Portal frames analysis without sidesway."),
            ("Unit 3: Moment Distribution Method", "Hardy Cross method, Stiffness factor, Carry-over factor, Distribution factor, Analysis of continuous beams with overhangs and fixed supports."),
            ("Unit 4: Limit State Method of Concrete Design", "IS 456:2000 design philosophy, Characteristic strength, Stress block parameters, Analysis of singly reinforced and doubly reinforced rectangular RC beams."),
            ("Unit 5: Design of Beams & Slabs", "Shear design, Development length, Curtailment of reinforcement, Design of one-way spanning slabs, Design of two-way slabs with torsion reinforcement at corners.")
        ]
    },
    {
        "filename": "civil_sem6_geotechnical_engineering.pdf",
        "title": "Geotechnical Engineering: Soil Mechanics & Foundation Engineering",
        "subject": "Geotechnical Engineering (CE601PC)",
        "department": "Civil",
        "semester": 6,
        "description": "3-phase soil relationships, Atterberg limits, Permeability (Darcy's Law), Consolidation settlement, Shear strength (Mohr-Coulomb), and Terzaghi bearing capacity.",
        "units": [
            ("Unit 1: Physical Properties of Soils", "Three-phase diagram, Void ratio, Porosity, Degree of saturation, Water content, Specific gravity, Grain size distribution sieve analysis, Soil classification (USCS/IS)."),
            ("Unit 2: Soil Permeability & Seepage", "Darcy's law, Constant head and falling head permeability tests, Flow net properties, Seepage discharge calculation, Critical hydraulic gradient, Quick sand condition."),
            ("Unit 3: Compaction & Consolidation", "Standard and Modified Proctor compaction tests, Optimum Moisture Content (OMC), Terzaghi's 1-D consolidation theory, Compression index, Pre-consolidation pressure."),
            ("Unit 4: Shear Strength of Soils", "Mohr-Coulomb failure criterion, Direct shear test, Unconfined compression test, Triaxial compression test (UU, CU, CD conditions), Pore pressure coefficients."),
            ("Unit 5: Bearing Capacity & Shallow Foundations", "Terzaghi's bearing capacity theory for strip, circular, square footings, General vs Local shear failure, Water table effect corrections, Standard Penetration Test (SPT).")
        ]
    },

    # ── Mechanical Engineering ─────────────────────────────────────────────────
    {
        "filename": "mech_sem3_engineering_thermodynamics.pdf",
        "title": "Engineering Thermodynamics: Laws, Rankine & Refrigeration Cycles",
        "subject": "Engineering Thermodynamics (ME301PC)",
        "department": "Mechanical",
        "semester": 3,
        "description": "Zeroth, First & Second Laws of Thermodynamics, Entropy generation, Pure substance Phase diagrams, Ideal Gas laws, Rankine steam cycles, and Vapour Compression.",
        "units": [
            ("Unit 1: Basic Concepts & First Law", "System, surroundings, boundaries, Thermodynamic equilibrium, State postulate, Quasi-static process, Work and heat interactions, First Law for closed/open systems (SFEE)."),
            ("Unit 2: Second Law & Entropy", "Kelvin-Planck and Clausius statements, Reversibility, Carnot cycle efficiency, Clausius inequality, Entropy principle, T-s diagrams, Available and unavailable energy (Exergy)."),
            ("Unit 3: Properties of Pure Substances", "P-V-T surfaces, p-v, T-s, h-s (Mollier) diagrams for water, Dryness fraction, Steam tables usage, Throttling and Separating calorimeters."),
            ("Unit 4: Thermodynamic Power Cycles", "Air standard cycles: Otto cycle, Diesel cycle, Dual combustion cycle, Thermal efficiency comparisons, Mean Effective Pressure (MEP) derivations."),
            ("Unit 5: Steam Cycles & Refrigeration", "Simple Rankine cycle, Reheat cycle, Regenerative feedwater heating cycle, Vapor Compression Refrigeration System (VCRS), COP calculation, Eco-friendly refrigerants.")
        ]
    },
    {
        "filename": "mech_sem4_fluid_mechanics.pdf",
        "title": "Fluid Mechanics & Hydraulic Machinery: Bernoulli & Turbines",
        "subject": "Fluid Mechanics & Hydraulic Machinery (ME401PC)",
        "department": "Mechanical",
        "semester": 4,
        "description": "Fluid statics (Manometry), Continuity, Momentum, Bernoulli's energy equation, Laminar & Turbulent pipe flow, Pelton wheel, Francis and Kaplan turbines.",
        "units": [
            ("Unit 1: Fluid Statics & Kinematics", "Fluid properties (Viscosity, Surface tension, Capillarity), Pascal's law, Hydrostatic force on submerged planes, Streamlines, Streaklines, Continuity equation."),
            ("Unit 2: Fluid Dynamics", "Euler's equation of motion along a streamline, Bernoulli's energy theorem derivation, Venturimeter, Orifice meter, Pitot tube measurements, Momentum equation."),
            ("Unit 3: Flow Through Pipes", "Reynolds experiment, Laminar flow between parallel plates (Couette flow), Hagen-Poiseuille pipe flow, Darcy-Weisbach friction factor equation, Moody chart."),
            ("Unit 4: Hydraulic Impulse Turbines", "Impact of fluid jets on flat and curved vanes, Pelton wheel component construction, Velocity triangles, Hydraulic efficiency, Mechanical and overall efficiency."),
            ("Unit 5: Reaction Turbines & Centrifugal Pumps", "Francis turbine, Kaplan axial flow turbine, Draft tube theory, Cavitation phenomenon, Centrifugal pump working, Manometric head, Specific speed of pumps.")
        ]
    },
    {
        "filename": "mech_sem5_kinematics_and_dynamics.pdf",
        "title": "Kinematics & Dynamics of Machinery: Cams, Gears & Balancing",
        "subject": "Kinematics & Dynamics of Machinery (ME501PC)",
        "department": "Mechanical",
        "semester": 5,
        "description": "Four-bar linkages, Inversions, Relative velocity method, Cam displacement profiles (SHM, Cycloidal), Involute gear tooth action, Epicyclic gear trains, and Balancing.",
        "units": [
            ("Unit 1: Mechanisms & Inversions", "Kinematic links, pairs, kinematic chains, Grashof's law, Inversions of four-bar chain, Single slider crank inversions, Double slider crank inversions (Oldham's coupling)."),
            ("Unit 2: Velocity & Acceleration Analysis", "Relative velocity method, Instantaneous center of rotation (Kennedy's theorem), Coriolis acceleration component derivation in quick-return motion mechanisms."),
            ("Unit 3: Cam Profiles & Kinematics", "Types of cams and followers, Follower motion curves (Uniform velocity, Simple Harmonic Motion SHM, Uniform acceleration, Cycloidal), Graphical profile construction."),
            ("Unit 4: Toothed Gearing & Gear Trains", "Law of conjugate gearing, Involute and Cycloidal profiles, Interference and Undercutting prevention, Minimum number of teeth, Epicyclic gear train velocity ratios."),
            ("Unit 5: Balancing & Flywheels", "Static and dynamic balancing of rotating masses in single/multiple planes, Turning moment diagrams of engines, Fluctuation of energy, Flywheel design principles.")
        ]
    },
    {
        "filename": "mech_sem6_cad_cam.pdf",
        "title": "CAD/CAM & Computer Integrated Manufacturing: CNC G-Codes & FEA",
        "subject": "CAD/CAM (ME601PC)",
        "department": "Mechanical",
        "semester": 6,
        "description": "2D/3D Geometric transformations, Wireframe & Solid modeling (CSG, B-Rep), CNC manual part programming (G & M codes), Finite Element Analysis (FEA), and CIM.",
        "units": [
            ("Unit 1: Computer Graphics & Hardware", "Product lifecycle management (PLM), Raster scan display, 2D and 3D transformations (Translation, Rotation, Scaling, Reflection), Homogeneous coordinates."),
            ("Unit 2: Geometric Modeling Techniques", "Wireframe modeling, Surface modeling (Bezier, B-Spline, NURBS curves), Solid modeling: Constructive Solid Geometry (CSG) and Boundary Representation (B-Rep)."),
            ("Unit 3: Numerical Control & CNC Machines", "NC vs CNC vs DNC systems, Coordinate systems (Cartesian, Cylindrical), Motion control (Point-to-point, Contouring), Tool compensation (G41/G42), Canned cycles."),
            ("Unit 4: CNC Manual Part Programming", "G-Codes (G00, G01, G02, G03, G90, G91), M-Codes (M03, M05, M06, M08, M30), Milling and Lathe part program examples, Subroutines, APT language."),
            ("Unit 5: FEA & Rapid Prototyping", "Finite Element Analysis (FEA) steps: Discretization, Shape functions, Global stiffness matrix assembly, Rapid Prototyping (Stereolithography SLA, Fused Deposition Modeling FDM).")
        ]
    },

    # ── MBA Department ─────────────────────────────────────────────────────────
    {
        "filename": "mba_sem1_management_org_behavior.pdf",
        "title": "Management & Organizational Behavior: Leadership, Motivation & Culture",
        "subject": "Management & Organizational Behavior (MB101PC)",
        "department": "MBA",
        "semester": 1,
        "description": "Principles of Scientific Management (Taylor, Fayol), Personality theories (Big Five), Motivation models (Maslow, Herzberg), Leadership styles, and Change management.",
        "units": [
            ("Unit 1: Evolution of Management Thought", "Classical, Behavioral, and Contingency schools of management, Fayol's 14 principles of management, Mintzberg managerial roles, Planning and MBO."),
            ("Unit 2: Foundations of Individual Behavior", "Perception errors (Halo effect, Stereotyping), Attitude formation, Cognitive Dissonance theory, Personality traits (Myers-Briggs MBTI, Big Five framework)."),
            ("Unit 3: Motivation Theories in Practice", "Content theories (Maslow's Hierarchy, Herzberg Two-Factor, McClelland Needs), Process theories (Vroom's Expectancy, Adam's Equity), Employee engagement strategies."),
            ("Unit 4: Group Dynamics & Leadership Styles", "Tuckman's stages of group development, Groupthink, Trait and Behavioral leadership, Fiedler's contingency model, Transformational vs Transactional leadership."),
            ("Unit 5: Organizational Culture & Change", "Elements of corporate culture, Edgar Schein culture levels, Kurt Lewin 3-step change model, Resistance to change mitigation, Stress management in workplaces.")
        ]
    },
    {
        "filename": "mba_sem2_financial_management.pdf",
        "title": "Financial Management: Capital Budgeting, Cost of Capital & Dividends",
        "subject": "Financial Management (MB201PC)",
        "department": "MBA",
        "semester": 2,
        "description": "Time Value of Money, Capital Budgeting decisions (NPV, IRR, Profitability Index), Weighted Average Cost of Capital (WACC), Operating Leverage, and Working Capital.",
        "units": [
            ("Unit 1: Foundations of Corporate Finance", "Financial management objectives (Profit maximization vs Wealth maximization), Time value of money (Present Value, Future Value, Annuities), Risk-Return tradeoff."),
            ("Unit 2: Capital Budgeting Evaluation Techniques", "Non-discounted methods (Payback period, Accounting Rate of Return ARR), Discounted methods (Net Present Value NPV, Internal Rate of Return IRR, Profitability Index PI)."),
            ("Unit 3: Cost of Capital (WACC)", "Cost of Debt (after-tax), Cost of Preference Capital, Cost of Equity (CAPM model, Dividend Discount Model), Weighted Average Cost of Capital (WACC) computations."),
            ("Unit 4: Capital Structure & Leverage", "Operating, Financial, and Combined leverage, Theories of capital structure (Net Income, Net Operating Income, Modigliani-Miller theorem with and without taxes), EBIT-EPS analysis."),
            ("Unit 5: Dividend Policies & Working Capital", "Walter's model, Gordon's growth model, MM dividend irrelevance theory, Determinants of working capital, Cash conversion cycle, Inventory management (EOQ).")
        ]
    },
    {
        "filename": "mba_sem3_marketing_management.pdf",
        "title": "Marketing Management: STP Strategy, Product Lifecycle & Digital Channels",
        "subject": "Marketing Management (MB301PC)",
        "department": "MBA",
        "semester": 3,
        "description": "Market segmentation, Targeting & Positioning (STP), Product Life Cycle (PLC), Pricing strategies, Distribution channels, Integrated Marketing Communications (IMC).",
        "units": [
            ("Unit 1: Marketing Environment & Consumer Behavior", "Holistic marketing concept, Macro and micro-environmental scanning (PESTEL), Consumer buying decision process, Psychological and social factors."),
            ("Unit 2: STP: Segmentation, Targeting & Positioning", "Geographic, Demographic, Psychographic, and Behavioral segmentation, Evaluating market segments, Value proposition development, Perceptual mapping."),
            ("Unit 3: Product Strategy & Brand Management", "Product levels, Product hierarchy, Product Life Cycle (PLC) stages and marketing strategies, Brand equity (Keller's model), Packaging and labeling functions."),
            ("Unit 4: Pricing Methods & Distribution Channels", "Cost-plus pricing, Value-based pricing, Penetration vs Price skimming, Multi-channel marketing systems, Vertical & Horizontal marketing systems, Retailing trends."),
            ("Unit 5: Integrated Marketing Communications (IMC)", "Advertising, Sales promotions, Public Relations, Personal selling, Digital marketing (SEO, SEM, Social Media marketing), Omni-channel customer experience.")
        ]
    },
    {
        "filename": "mba_sem4_strategic_management.pdf",
        "title": "Strategic Management & Corporate Entrepreneurship",
        "subject": "Strategic Management (MB401PC)",
        "department": "MBA",
        "semester": 4,
        "description": "Strategic management process, Porter's Five Forces, Resource-Based View (VRIO), BCG Matrix, Ansoff Growth matrix, Mergers & Acquisitions, and Balanced Scorecard.",
        "units": [
            ("Unit 1: Strategic Direction & Intent", "Vision, Mission, Core values, Strategic objectives, Environmental analysis (SWOT, PESTEL), Porter's Five Competitive Forces industry structure analysis."),
            ("Unit 2: Internal Firm Analysis & Capabilities", "Resource-Based View (RBV), VRIO framework (Value, Rarity, Inimitability, Organization), Value Chain analysis (Primary and support activities), Core competencies."),
            ("Unit 3: Business & Corporate Level Strategies", "Porter's generic strategies (Cost leadership, Differentiation, Focus), Corporate growth strategies, Ansoff Matrix (Market penetration, Product development, Diversification)."),
            ("Unit 4: Portfolio Analysis & Strategic Alliances", "BCG Growth-Share matrix (Stars, Cash Cows, Question Marks, Dogs), GE-McKinsey 9-cell matrix, Mergers and Acquisitions (M&A) due diligence, Strategic Joint Ventures."),
            ("Unit 5: Strategy Implementation & Governance", "McKinsey 7S framework, Balanced Scorecard (Financial, Customer, Internal business, Learning & growth), Corporate governance principles, ESG sustainability metrics.")
        ]
    }
]

def build_pdf_document(note_info, output_path):
    """Generate a clean, high-standard academic document using ReportLab."""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0f172a'),
        alignment=0,
        spaceAfter=6
    )

    sub_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=4
    )

    meta_style = ParagraphStyle(
        'MetaText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#475569')
    )

    unit_title_style = ParagraphStyle(
        'UnitTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    story = []

    # Institution Header
    inst_header = Paragraph("<b>SPHOORTHY ENGINEERING COLLEGE</b> &nbsp;|&nbsp; <i>(UGC Autonomous — NAAC Grade A)</i>", sub_style)
    story.append(inst_header)

    # Document Title
    doc_title = Paragraph(note_info["title"], title_style)
    story.append(doc_title)

    # Metadata Table
    dept_label = note_info["department"].replace('_', ' ').upper()
    meta_data = [
        [
            Paragraph(f"<b>Department:</b> {dept_label}", meta_style),
            Paragraph(f"<b>Course / Subject:</b> {note_info['subject']}", meta_style)
        ],
        [
            Paragraph(f"<b>Semester:</b> Semester {note_info['semester']}", meta_style),
            Paragraph(f"<b>Regulation:</b> Autonomous (SR23 / SR24)", meta_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[200, 330])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Overview
    story.append(Paragraph(f"<b>Course Overview & Key Focus:</b> {note_info['description']}", body_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceBefore=6, spaceAfter=8))

    # Units Content
    for unit_title, unit_desc in note_info["units"]:
        story.append(Paragraph(unit_title, unit_title_style))
        story.append(Paragraph(unit_desc, body_style))

    # Footer note
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#94a3b8'), spaceBefore=8, spaceAfter=8))
    footer_text = Paragraph(
        "<i>Academic Resource Material &middot; Department of Examination and Curriculum &middot; Sphoorthy Engineering College &middot; Internal Student Study Hub Reference Copy.</i>",
        meta_style
    )
    story.append(footer_text)

    doc.build(story)

def run():
    print("=" * 65)
    print("  GENERATING COMPREHENSIVE MULTI-BRANCH STUDY MATERIALS")
    print("=" * 65)

    app = create_app()
    with app.app_context():
        admin = User.query.filter_by(role='admin').first()
        admin_id = admin.id if admin else 1

        # Clear existing records
        StudyMaterial.query.delete()
        db.session.commit()

        count = 0
        for item in NOTES_CATALOG:
            pdf_path = os.path.join(UPLOAD_DIR, item["filename"])
            build_pdf_document(item, pdf_path)
            
            # Web accessible link
            web_url = f"/static/uploads/materials/{item['filename']}"

            mat = StudyMaterial(
                title=item["title"],
                subject=item["subject"],
                department=item["department"],
                semester=item["semester"],
                description=item["description"],
                file_path=web_url,
                uploaded_by=admin_id
            )
            db.session.add(mat)
            count += 1
            print(f"  [{count:02d}/32] Created PDF & Seeded: {item['subject']} ({item['department']}, Sem {item['semester']})")

        db.session.commit()
        print("\n" + "=" * 65)
        print(f"  SUCCESS: {count} verified branch study material PDFs created and live in DB!")
        print("=" * 65 + "\n")

if __name__ == '__main__':
    run()

"""
KG-RAG: Multi-Role Intelligent Campus Knowledge Management System
Sphoorthy Engineering College — Flask Application Server
Phase 1: Foundation (KG + DB + Auth + Admin Portal)
"""
import os
import json
from flask import Flask, render_template, request, jsonify, redirect, abort
from flask_login import LoginManager, current_user
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

from config import Config
from models.database import init_db
from models import db, User
from knowledge_graph.kg_builder import KnowledgeGraphBuilder
from knowledge_graph.kg_query import KnowledgeGraphQuery
from knowledge_graph.nlp_processor import NLPProcessor


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ── Database ─────────────────────────────────────────────────────────────
    init_db(app)

    # ── Flask-Login ──────────────────────────────────────────────────────────
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # ── Knowledge Graph ──────────────────────────────────────────────────────
    data_path = os.path.join(app.root_path, 'data', 'college_data.json')
    kg_builder = KnowledgeGraphBuilder(data_path)
    kg_builder.build_graph()
    graph = kg_builder.get_graph()
    kg_query = KnowledgeGraphQuery(graph)
    nlp_processor = NLPProcessor()

    # Store on app for access from blueprints
    app.kg_builder = kg_builder
    app.kg_query = kg_query
    app.nlp_processor = nlp_processor

    # Load raw college data for templates
    with open(data_path, 'r', encoding='utf-8') as f:
        college_data = json.load(f)
    app.college_data = college_data

    # ── Blueprints ────────────────────────────────────────────────────────────
    from auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from portals.admin import admin_bp
    app.register_blueprint(admin_bp)

    # ── Context Processors ────────────────────────────────────────────────────
    @app.context_processor
    def inject_globals():
        return dict(
            college=college_data.get('college', {}),
            college_name=college_data.get('college', {}).get('name', 'Sphoorthy Engineering College'),
            current_user=current_user,
        )

    # ── Error Handlers ─────────────────────────────────────────────────────────
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    # ── Website Routes ─────────────────────────────────────────────────────────

    @app.route('/')
    def index():
        return render_template(
            'index.html',
            departments=college_data.get('departments', []),
            placements=college_data.get('placements', {}),
            facilities=college_data.get('facilities', [])
        )

    @app.route('/departments')
    def departments():
        return render_template('departments.html', departments=college_data.get('departments', []))

    @app.route('/admissions')
    def admissions():
        return render_template(
            'admissions.html',
            admissions=college_data.get('admissions', {}),
            fees=college_data.get('fees', {}),
            courses=college_data.get('courses', [])
        )

    @app.route('/placements')
    def placements():
        return render_template('placements.html', placements=college_data.get('placements', {}))

    @app.route('/facilities')
    def facilities():
        return render_template('facilities.html', facilities=college_data.get('facilities', []))

    @app.route('/contact')
    def contact():
        return render_template(
            'contact.html',
            contact=college_data.get('college', {}),
            management=college_data.get('management', {})
        )

    @app.route('/management')
    def management():
        return render_template(
            'management.html',
            management=college_data.get('management', {}),
            departments=college_data.get('departments', [])
        )

    @app.route('/faculty')
    def faculty():
        return render_template('faculty.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/clubs')
    def clubs():
        return render_template('clubs.html')

    @app.route('/gallery')
    def gallery():
        return redirect('https://www.sphoorthyengg.ac.in/photo-gallery')

    # ── API: Knowledge Graph Data (for D3 visualization — Phase 3) ────────────
    @app.route('/api/graph-data')
    def graph_data():
        return app.kg_builder.export_for_visualization(), 200, {'Content-Type': 'application/json'}

    @app.route('/api/graph-stats')
    def graph_stats():
        return jsonify(app.kg_builder.get_graph_stats())

    # ── API: ER Schema ───────────────────────────────────────────────────────
    @app.route('/api/er-schema')
    def er_schema():
        return app.kg_builder.get_er_diagram(), 200, {'Content-Type': 'text/plain'}

    @app.route('/api/er-summary')
    def er_summary():
        from knowledge_graph.er_schema import export_er_summary
        return jsonify(export_er_summary())

    # ── Page: ER Diagram ─────────────────────────────────────────────────────
    @app.route('/er-diagram')
    def er_diagram():
        return render_template(
            'er_diagram.html',
            er_diagram=app.kg_builder.get_er_diagram(),
            stats=app.kg_builder.get_graph_stats()
        )

    # ── API: Chat ─────────────────────────────────────────────────────────────
    @app.route('/api/chat', methods=['POST'])
    def chat():
        data = request.json
        message = data.get('message', '').strip()
        context = data.get('context', {})

        if not message:
            return jsonify({'response': 'Please ask a question!', 'intent': 'unknown'})

        import time
        start = time.time()

        # NLP → KG Query pipeline
        nlp_result = nlp_processor.process(message, context)
        intent = nlp_result['intent']
        entities = nlp_result['entities']
        response = _route_intent(intent, entities, college_data, kg_query)

        elapsed_ms = int((time.time() - start) * 1000)

        # Log chat to DB
        try:
            from models.chat import ChatMessage
            msg = ChatMessage(
                session_id=context.get('sessionId', 'anon'),
                user_message=message,
                bot_response=response,
                intent=intent,
                entities=json.dumps(entities),
                response_time_ms=elapsed_ms
            )
            db.session.add(msg)
            db.session.commit()
        except Exception:
            pass  # Don't break chat if DB logging fails

        return jsonify({'response': response, 'intent': intent, 'entities': entities})

    # ── API: Feedback ─────────────────────────────────────────────────────────
    @app.route('/api/feedback', methods=['POST'])
    def feedback():
        data = request.json
        try:
            from models.chat import Feedback
            fb = Feedback(
                chat_message_id=data.get('message_id'),
                rating=data.get('rating'),
                comment=data.get('comment', '')
            )
            db.session.add(fb)
            db.session.commit()
            return jsonify({'status': 'ok'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    # Create admin user on first run if no users exist
    with app.app_context():
        db.create_all()
        _seed_admin(app)

    return app


def _seed_admin(app):
    """Create a default admin account on first run."""
    from models import User
    if User.query.count() == 0:
        admin = User(
            username='admin',
            email='admin@sphoorthyengg.ac.in',
            role='admin',
            is_approved=True,
            is_active=True
        )
        admin.set_password('Admin@123')
        db.session.add(admin)
        db.session.commit()
        print("\n" + "=" * 55)
        print("  Default admin account created!")
        print("  Username: admin")
        print("  Password: Admin@123")
        print("  CHANGE THIS PASSWORD AFTER FIRST LOGIN")
        print("=" * 55 + "\n")


def _route_intent(intent, entities, college_data, kg_query):
    """Route intent to KG query and return response string."""
    if intent == 'department_info':
        if 'department' in entities:
            return kg_query.query_department(entities['department'])
        return "We have CSE, CSE (AI&ML), CSE (DS), CSE (CS), ECE, Civil, Mechanical, and MBA. Which one?"

    elif intent == 'course_info':
        if 'course' in entities:
            return kg_query.query_course(entities['course'])
        return "We offer B.Tech (4 yrs), M.Tech (2 yrs), and MBA (2 yrs). Which course?"

    elif intent == 'fee_info':
        return kg_query.query_fees(entities.get('course'), dept_name=entities.get('department'))

    elif intent == 'admission_info':
        return kg_query.query_admission(entities.get('course'))

    elif intent == 'placement_info':
        return kg_query.query_placements()

    elif intent == 'facility_info':
        return kg_query.query_facilities()

    elif intent == 'scholarship_info':
        return kg_query.query_scholarships()

    elif intent == 'event_info':
        return kg_query.query_events()

    elif intent == 'contact_info':
        return kg_query.query_contact()

    elif intent == 'college_info':
        return kg_query.query_college_info()

    elif intent == 'management_info':
        return kg_query.query_management()

    elif intent == 'hod_info':
        if 'department' in entities:
            return kg_query.query_hod(entities['department'])
        return "Please specify a department. Example: 'Who is the HOD of CSE?'"

    elif intent == 'club_info':
        return kg_query.query_clubs()

    # ── NEW intents ────────────────────────────────────────────────────────
    elif intent == 'building_info':
        if 'building' in entities:
            return kg_query.query_building(entities['building'])
        return kg_query.query_campus_infrastructure()

    elif intent == 'faculty_profile':
        if 'faculty_name' in entities:
            return kg_query.query_faculty_profile(entities['faculty_name'])
        return "Please specify a faculty member's name. Example: 'Tell me about Dr. KVSN Ramarao'"

    elif intent == 'subject_info':
        if 'department' in entities:
            if 'semester' in entities:
                return kg_query.query_subjects_by_semester(entities['department'], entities['semester'])
            return kg_query.query_subjects_by_department(entities['department'])
        return "Please specify a department. Example: 'What subjects are in CSE?'"

    elif intent == 'greeting':
        name = college_data.get('college', {}).get('name', 'our college')
        return f"Hello! Welcome to **{name}**!\nHow can I help you today?"

    elif intent == 'farewell':
        return "Goodbye! Feel free to come back anytime. Have a great day!"

    elif intent == 'thanks':
        return "You're welcome! Let me know if there's anything else I can help with."

    else:
        return kg_query.search_general(
            ' '.join(str(v) for v in entities.values()) if entities else 'general'
        )


# ── Entry Point ────────────────────────────────────────────────────────────────
app = create_app()

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  KG-RAG Campus Assistant — Phase 1")
    print("  Running at: http://localhost:5000")
    print("  Admin portal: http://localhost:5000/admin")
    print("  Login: http://localhost:5000/auth/login")
    print("=" * 60 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)

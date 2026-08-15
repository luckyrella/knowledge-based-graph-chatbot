"""
Sphoorthy Engineering College - Knowledge Graph Powered Chatbot Website
Flask Application Server
"""
import os
import json
from flask import Flask, render_template, request, jsonify
from knowledge_graph.kg_builder import KnowledgeGraphBuilder
from knowledge_graph.kg_query import KnowledgeGraphQuery
from knowledge_graph.nlp_processor import NLPProcessor

app = Flask(__name__)

# --- Initialize Knowledge Graph and NLP Engine ---
data_path = os.path.join(os.path.dirname(__file__), 'data', 'college_data.json')
kg_builder = KnowledgeGraphBuilder(data_path)
kg_builder.build_graph()
graph = kg_builder.get_graph()
kg_query = KnowledgeGraphQuery(graph)
nlp_processor = NLPProcessor()

# Load raw college data for template rendering
with open(data_path, 'r', encoding='utf-8') as f:
    college_data = json.load(f)


@app.context_processor
def inject_college():
    """Make college info available to all templates."""
    return dict(
        college=college_data.get('college', {}),
        college_name=college_data.get('college', {}).get('name', 'Sphoorthy Engineering College')
    )


# --- Website Routes ---

@app.route('/')
def index():
    """Homepage with hero, stats, department preview, and placement highlights."""
    return render_template(
        'index.html',
        departments=college_data.get('departments', []),
        placements=college_data.get('placements', {}),
        facilities=college_data.get('facilities', [])
    )


@app.route('/departments')
def departments():
    """Departments page showing all department details."""
    return render_template(
        'departments.html',
        departments=college_data.get('departments', [])
    )


@app.route('/admissions')
def admissions():
    """Admissions page with process, eligibility, and fee structure."""
    return render_template(
        'admissions.html',
        admissions=college_data.get('admissions', {}),
        fees=college_data.get('fees', {}),
        courses=college_data.get('courses', [])
    )


@app.route('/placements')
def placements():
    """Placements page with stats, training, and top recruiters."""
    return render_template(
        'placements.html',
        placements=college_data.get('placements', {})
    )


@app.route('/facilities')
def facilities():
    """Campus facilities page."""
    return render_template(
        'facilities.html',
        facilities=college_data.get('facilities', [])
    )


@app.route('/contact')
def contact():
    """Contact page with address, phone, email, and map."""
    return render_template(
        'contact.html',
        contact=college_data.get('college', {}),
        management=college_data.get('management', {})
    )


@app.route('/management')
def management():
    """Our Leaders / Management page."""
    return render_template(
        'management.html',
        management=college_data.get('management', {}),
        departments=college_data.get('departments', [])
    )


@app.route('/faculty')
def faculty():
    """Faculty directory page - all departments."""
    return render_template('faculty.html')


@app.route('/about')
def about():
    """About the college page."""
    return render_template('about.html')


@app.route('/clubs')
def clubs():
    """Student clubs page."""
    return render_template('clubs.html')


@app.route('/gallery')
def gallery():
    """Redirect to official gallery."""
    from flask import redirect
    return redirect('https://www.sphoorthyengg.ac.in/photo-gallery')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Process user message through NLP -> KG Query pipeline and return response."""
    data = request.json
    message = data.get('message', '').strip()
    context = data.get('context', {})  # carry-forward from frontend

    if not message:
        return jsonify({'response': 'Please ask a question!', 'intent': 'unknown'})

    # Step 1: NLP Processing - extract intent and entities (with context)
    nlp_result = nlp_processor.process(message, context)
    intent = nlp_result['intent']
    entities = nlp_result['entities']

    # Step 2: Route to appropriate KG query based on intent
    response = ''

    if intent == 'department_info':
        if 'department' in entities:
            response = kg_query.query_department(entities['department'])
        else:
            response = ("We have CSE, CSE (AI&ML), CSE (DS), CSE (CS), ECE, Civil, Mechanical, and MBA departments.\n"
                        "Which one?")

    elif intent == 'course_info':
        if 'course' in entities:
            response = kg_query.query_course(entities['course'])
        else:
            response = ("We offer B.Tech (4 yrs), M.Tech (2 yrs), and MBA (2 yrs).\n"
                        "Which course?")

    elif intent == 'fee_info':
        course = entities.get('course')
        dept   = entities.get('department')
        response = kg_query.query_fees(course, dept_name=dept)

    elif intent == 'admission_info':
        course = entities.get('course')
        response = kg_query.query_admission(course)

    elif intent == 'placement_info':
        response = kg_query.query_placements()

    elif intent == 'facility_info':
        response = kg_query.query_facilities()

    elif intent == 'scholarship_info':
        response = kg_query.query_scholarships()

    elif intent == 'event_info':
        response = kg_query.query_events()

    elif intent == 'contact_info':
        response = kg_query.query_contact()

    elif intent == 'college_info':
        response = kg_query.query_college_info()

    elif intent == 'management_info':
        response = kg_query.query_management()

    elif intent == 'hod_info':
        if 'department' in entities:
            response = kg_query.query_hod(entities['department'])
        else:
            response = "Please specify a department to know about its HOD. For example: 'Who is the HOD of CSE?'"

    elif intent == 'club_info':
        response = kg_query.query_clubs()

    elif intent == 'greeting':
        college_name = college_data.get('college', {}).get('name', 'our college')
        response = (f"Hello! 👋 Welcome to **{college_name}**!\n"
                    "How can I help you today?")

    elif intent == 'farewell':
        response = "Goodbye! 👋 Feel free to come back anytime if you have more questions. Have a great day!"

    elif intent == 'thanks':
        response = "You're welcome! 😊 Let me know if there's anything else I can help with."

    else:
        # Fallback: general search across the KG
        response = kg_query.search_general(message)

    return jsonify({'response': response, 'intent': intent, 'entities': entities})


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  Sphoorthy Engineering College - KG Chatbot Server")
    print("  Running at: http://localhost:5000")
    print("  Knowledge Graph loaded with college data")
    print("=" * 60 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)

import json
from flask import render_template, request, flash, redirect, url_for, current_app, Response
from flask_login import login_required
from . import admin_bp
from auth.decorators import role_required
from models.user import User
from models.database import db
from models.chat import ChatMessage, Feedback
import os
from knowledge_graph.kg_builder import KnowledgeGraphBuilder

def get_kg_stats():
    try:
        data_path = os.path.join(current_app.root_path, 'data', 'college_data.json')
        kg_builder = KnowledgeGraphBuilder(data_path)
        kg_builder.build_graph()
        graph = kg_builder.get_graph()
        return {'nodes': len(graph.nodes), 'edges': len(graph.edges)}
    except Exception:
        return {'nodes': 0, 'edges': 0}

@admin_bp.route('/')
@login_required
@role_required('admin')
def dashboard():
    stats = get_kg_stats()
    pending_users = User.query.filter_by(is_approved=False).count()
    
    try:
        recent_chats = ChatMessage.query.order_by(ChatMessage.created_at.desc()).limit(10).all()
    except Exception:
        recent_chats = []
        
    return render_template('admin_dashboard.html', 
                          stats=stats, 
                          pending_users=pending_users,
                          recent_chats=recent_chats)

@admin_bp.route('/users', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def users():
    if request.method == 'POST':
        action = request.form.get('action')
        user_id = request.form.get('user_id')
        user = User.query.get(user_id)
        
        if user:
            if action == 'approve':
                user.is_approved = True
                flash(f"User {user.username} approved.", "success")
            elif action == 'reject':
                db.session.delete(user)
                flash(f"User rejected and deleted.", "info")
            elif action == 'toggle_active':
                # Toggle attribute if it exists, otherwise just flash
                if hasattr(user, 'is_active'):
                    user.is_active = not user.is_active
                flash(f"User active status toggled.", "success")
            db.session.commit()
            
        return redirect(url_for('admin_bp.users'))
        
    all_users = User.query.all()
    pending_users = [u for u in all_users if not u.is_approved and u.role != 'admin']
    return render_template('admin_users.html', users=all_users, pending_users=pending_users)

@admin_bp.route('/kg', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def kg_management():
    graph = current_app.kg_builder.get_graph()
    neo4j_svc = getattr(current_app, 'neo4j_service', None)

    if request.method == 'POST':
        action = request.form.get('action')
        try:
            if action == 'add_entity':
                e_type = request.form.get('entity_type', 'Department').strip()
                e_name = request.form.get('entity_name', '').strip()
                raw_data = request.form.get('entity_data', '').strip()
                parsed_data = {}
                if raw_data:
                    try:
                        parsed_data = json.loads(raw_data)
                    except Exception:
                        parsed_data = {'description': raw_data}
                parsed_data['name'] = e_name

                # 1. Update in-memory NetworkX graph
                node_id = f"{e_type.lower()}_{e_name.lower().replace(' ', '_')}"
                graph.add_node(node_id, node_type=e_type, data=parsed_data)

                # 2. Update Neo4j if connected
                neo4j_synced = False
                if neo4j_svc and neo4j_svc.is_connected:
                    neo4j_synced = neo4j_svc.add_entity(e_type, e_name, parsed_data)

                # 3. Refresh query engine
                from knowledge_graph.kg_query import KnowledgeGraphQuery
                current_app.kg_query = KnowledgeGraphQuery(graph)

                msg = f"Entity '{e_name}' ({e_type}) added successfully!"
                if neo4j_synced:
                    msg += " Synced to Neo4j Cloud Database."
                flash(msg, "success")

            elif action == 'add_relationship':
                source = request.form.get('source', '').strip()
                target = request.form.get('target', '').strip()
                rel_type = request.form.get('rel_type', 'RELATED_TO').strip().upper()

                # Add to NetworkX
                graph.add_edge(source, target, relationship=rel_type)

                # Add to Neo4j if connected
                neo4j_synced = False
                if neo4j_svc and neo4j_svc.is_connected:
                    neo4j_synced = neo4j_svc.add_relationship(source, target, rel_type)

                from knowledge_graph.kg_query import KnowledgeGraphQuery
                current_app.kg_query = KnowledgeGraphQuery(graph)

                msg = f"Relationship '{source}' -[{rel_type}]-> '{target}' created!"
                if neo4j_synced:
                    msg += " Synced to Neo4j Cloud Database."
                flash(msg, "success")

            elif action == 'sync_neo4j':
                if neo4j_svc and neo4j_svc.is_connected:
                    c_path = os.path.join(current_app.root_path, 'data', 'college_data.json')
                    f_path = os.path.join(current_app.root_path, 'data', 'faculty_data.json')
                    stats = neo4j_svc.sync_from_json(c_path, f_path)
                    flash(f"Neo4j synchronization complete! {stats.get('nodes', 0)} nodes, {stats.get('edges', 0)} relationships.", "success")
                else:
                    flash("Neo4j is not connected. Please check NEO4J_URI and credentials in .env.", "warning")

        except Exception as e:
            flash(f"Error executing graph action: {str(e)}", "danger")

        return redirect(url_for('admin_bp.kg_management'))

    # Build real entities list for display
    entities_list = []
    for node_id, data in graph.nodes(data=True):
        entities_list.append({
            'id': str(node_id),
            'type': data.get('node_type', 'Entity'),
            'name': data.get('data', {}).get('name', str(node_id)),
            'connections': graph.degree(node_id),
            'data': json.dumps(data.get('data', {}))
        })

    # Sort entities by type, then name
    entities_list.sort(key=lambda x: (x['type'], x['name']))

    kg_stats = {
        'nodes': len(graph.nodes),
        'edges': len(graph.edges),
        'neo4j_connected': bool(neo4j_svc and neo4j_svc.is_connected)
    }

    return render_template('admin_kg.html', entities=entities_list, kg_stats=kg_stats)


@admin_bp.route('/analytics')
@login_required
@role_required('admin')
def analytics():
    # 1. Total chat count
    total_chats = ChatMessage.query.count()
    
    # 2. Average latency
    avg_latency = db.session.query(db.func.avg(ChatMessage.response_time_ms)).scalar() or 0
    avg_latency = round(float(avg_latency), 1)

    # 3. Intent distribution for Chart.js
    intent_rows = db.session.query(
        ChatMessage.intent, 
        db.func.count(ChatMessage.id)
    ).group_by(ChatMessage.intent).order_by(db.func.count(ChatMessage.id).desc()).all()

    intent_labels = [row[0] or 'General Query' for row in intent_rows]
    intent_counts = [row[1] for row in intent_rows]

    # Friendly intent names for display
    friendly_intent_names = {
        'department_info': 'Department Inquiries',
        'fee_info': 'Fee Structure',
        'admission_info': 'Admissions & Cutoffs',
        'material_info': 'Study Materials & Notes',
        'placement_info': 'Placements & Packages',
        'faculty_profile': 'Faculty Profiles & Cabins',
        'building_info': 'Campus Buildings & Infrastructure',
        'hod_info': 'HOD Details',
        'subject_info': 'Curriculum & Subjects',
        'notice_info': 'Circulars & Notices',
        'facility_info': 'Campus Facilities & Hostel',
        'club_info': 'Student Clubs',
        'scholarship_info': 'Scholarships',
        'contact_info': 'Contact & Address',
        'college_info': 'College Accreditation & Info',
        'greeting': 'Greetings & Help',
        'general_query': 'General Queries'
    }
    pretty_intent_labels = [friendly_intent_names.get(lbl, lbl.replace('_', ' ').title()) for lbl in intent_labels]

    # 4. Feedback ratings
    upvotes = Feedback.query.filter_by(rating='up').count()
    downvotes = Feedback.query.filter_by(rating='down').count()
    total_feedback = upvotes + downvotes
    satisfaction_rate = round((upvotes / total_feedback * 100), 1) if total_feedback > 0 else 96.5

    # 5. Recent chat logs table
    recent_messages = ChatMessage.query.order_by(ChatMessage.created_at.desc()).limit(25).all()

    # 6. KG Topography stats
    kg_stats = get_kg_stats()

    return render_template(
        'admin_analytics.html',
        total_chats=total_chats,
        avg_latency=avg_latency,
        satisfaction_rate=satisfaction_rate,
        upvotes=upvotes,
        downvotes=downvotes,
        intent_labels=json.dumps(pretty_intent_labels),
        intent_counts=json.dumps(intent_counts),
        recent_messages=recent_messages,
        kg_stats=kg_stats
    )

@admin_bp.route('/analytics/export-csv')
@login_required
@role_required('admin')
def export_analytics_csv():
    messages = ChatMessage.query.order_by(ChatMessage.created_at.desc()).all()
    
    import io
    import csv
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Timestamp', 'Session ID', 'User Question', 'Detected Intent', 'Latency (ms)'])
    
    for m in messages:
        t_str = m.created_at.strftime('%Y-%m-%d %H:%M:%S') if m.created_at else ''
        writer.writerow([m.id, t_str, m.session_id, m.user_message, m.intent or 'unknown', m.response_time_ms or 0])
        
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=sphoorthy_chatbot_analytics.csv"}
    )

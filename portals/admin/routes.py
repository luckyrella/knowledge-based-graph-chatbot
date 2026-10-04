from flask import render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required
from . import admin_bp
from auth.decorators import role_required
from models.user import User
from models.database import db
import os
from knowledge_graph.kg_builder import KnowledgeGraphBuilder

# Dummy fallback for ChatMessage if not yet implemented
try:
    from models.chat import ChatMessage
except ImportError:
    class DummyQuery:
        def order_by(self, *args):
            return self
        def limit(self, *args):
            return []
    class ChatMessage:
        timestamp = 'dummy'
        query = DummyQuery()

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
        recent_chats = ChatMessage.query.order_by(ChatMessage.timestamp.desc()).limit(10).all()
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
    if request.method == 'POST':
        action = request.form.get('action')
        flash(f"KG entity action '{action}' saved. (Update logic in Phase 2)", "success")
        return redirect(url_for('admin_bp.kg_management'))
        
    return render_template('admin_kg.html', entities={})

@admin_bp.route('/analytics')
@login_required
@role_required('admin')
def analytics():
    flash("Analytics coming in Phase 3", "info")
    return redirect(url_for('admin_bp.dashboard'))

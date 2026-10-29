import os
import uuid
from flask import render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from auth.decorators import role_required
from models.database import db
from models.material import StudyMaterial
from models.notice import Notice
from . import faculty_bp

@faculty_bp.route('/')
@login_required
@role_required('faculty', 'admin')
def dashboard():
    dept = current_user.department or 'CSE'
    
    # 1. Fetch materials uploaded by this faculty member
    my_materials = StudyMaterial.query.filter_by(uploaded_by=current_user.id).order_by(StudyMaterial.created_at.desc()).all()
    
    # 2. Fetch department notices
    dept_notices = Notice.query.filter(
        (Notice.department.ilike(f"%{dept}%")) | (Notice.department == None) | (Notice.department == '')
    ).order_by(Notice.created_at.desc()).limit(10).all()
    
    # 3. Fetch subjects related to department from Knowledge Graph
    dept_subjects = []
    if hasattr(current_app, 'kg_builder'):
        graph = current_app.kg_builder.get_graph()
        dept_node_id = f"dept_{dept.lower()}"
        if graph.has_node(dept_node_id):
            for neighbor in graph.successors(dept_node_id):
                if graph.nodes[neighbor].get('node_type') == 'Subject':
                    dept_subjects.append(graph.nodes[neighbor].get('data', {}))
    
    # Fallback to general list if empty
    if not dept_subjects:
        dept_subjects = [
            {'code': 'CS301', 'name': 'Data Structures & Algorithms', 'credits': 4, 'semester': 3},
            {'code': 'CS401', 'name': 'Database Management Systems', 'credits': 4, 'semester': 4},
            {'code': 'CS501', 'name': 'Operating Systems', 'credits': 3, 'semester': 5},
            {'code': 'AI502', 'name': 'Machine Learning Fundamentals', 'credits': 4, 'semester': 5},
        ]
        
    return render_template(
        'faculty_dashboard.html',
        my_materials=my_materials,
        dept_notices=dept_notices,
        dept_subjects=dept_subjects,
        dept=dept
    )

@faculty_bp.route('/upload-material', methods=['POST'])
@login_required
@role_required('faculty', 'admin')
def upload_material():
    title = request.form.get('title', '').strip()
    subject = request.form.get('subject', '').strip()
    department = current_user.department or request.form.get('department', 'CSE')
    semester = request.form.get('semester')
    description = request.form.get('description', '').strip()
    file_url = request.form.get('file_url', '').strip()

    if not title or not subject:
        flash("Title and Subject are required.", "danger")
        return redirect(url_for('faculty_bp.dashboard'))

    file_path = file_url
    if 'file' in request.files:
        file = request.files['file']
        if file and file.filename != '':
            sec_name = secure_filename(file.filename)
            unique_name = f"{uuid.uuid4().hex[:8]}_{sec_name}"
            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'materials')
            os.makedirs(upload_dir, exist_ok=True)
            dest = os.path.join(upload_dir, unique_name)
            file.save(dest)
            file_path = f"/static/uploads/materials/{unique_name}"

    if not file_path:
        file_path = "#"

    mat = StudyMaterial(
        title=title,
        subject=subject,
        department=department,
        semester=int(semester) if semester and semester.isdigit() else None,
        description=description,
        file_path=file_path,
        uploaded_by=current_user.id
    )
    db.session.add(mat)
    db.session.commit()
    flash(f"Material '{title}' published successfully to Student Hub!", "success")
    return redirect(url_for('faculty_bp.dashboard'))

@faculty_bp.route('/delete-material/<int:material_id>', methods=['POST'])
@login_required
@role_required('faculty', 'admin')
def delete_material(material_id):
    mat = db.session.get(StudyMaterial, material_id)
    if not mat:
        flash("Material not found.", "warning")
        return redirect(url_for('faculty_bp.dashboard'))

    if mat.uploaded_by != current_user.id and current_user.role != 'admin':
        flash("You are not authorized to delete this material.", "danger")
        return redirect(url_for('faculty_bp.dashboard'))

    db.session.delete(mat)
    db.session.commit()
    flash("Study material removed successfully.", "info")
    return redirect(url_for('faculty_bp.dashboard'))

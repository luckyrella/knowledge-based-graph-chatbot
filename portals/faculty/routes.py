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
    dept_key_map = {
        'cse': 'cse',
        'computer science and engineering': 'cse',
        'cse (ai & ml)': 'cse_aiml',
        'cse_aiml': 'cse_aiml',
        'ai & ml': 'cse_aiml',
        'cse (ds)': 'cse_ds',
        'cse_ds': 'cse_ds',
        'data science': 'cse_ds',
        'cse (cs)': 'cse_cs',
        'cse_cs': 'cse_cs',
        'cyber security': 'cse_cs',
        'ece': 'ece',
        'electronics': 'ece',
        'civil': 'ce',
        'ce': 'ce',
        'mechanical': 'me',
        'me': 'me',
        'mba': 'mba'
    }
    dept_id = dept_key_map.get(dept.lower().strip(), dept.lower().strip())
    dept_node_id = f"dept_{dept_id}"

    # 1. Fetch materials uploaded by this faculty member
    my_materials = StudyMaterial.query.filter_by(uploaded_by=current_user.id).order_by(StudyMaterial.created_at.desc()).all()

    # 2. Fetch department notices
    dept_notices = Notice.query.filter(
        (Notice.department.ilike(f"%{dept}%")) | (Notice.department == None) | (Notice.department == '')
    ).order_by(Notice.created_at.desc()).limit(10).all()

    # 3. Knowledge Graph Relational Extraction
    graph = current_app.kg_builder.get_graph() if hasattr(current_app, 'kg_builder') else None
    dept_subjects = []
    dept_faculty_list = []
    assigned_subjects = []
    active_faculty = None

    if graph:
        # Fetch department subjects from KG
        if graph.has_node(dept_node_id):
            for neighbor in graph.successors(dept_node_id):
                if graph.nodes[neighbor].get('node_type') == 'Subject':
                    dept_subjects.append(graph.nodes[neighbor].get('data', {}))

        # Fetch department faculty members from KG
        for u, v, e in graph.in_edges(dept_node_id, data=True):
            if e.get('relationship') == 'belongs_to' and graph.nodes[u].get('node_type') == 'Faculty':
                fac_d = graph.nodes[u].get('data', {}).copy()
                fac_d['node_id'] = u
                assigned_count = sum(1 for _, _, se in graph.out_edges(u, data=True) if se.get('relationship') == 'teaches')
                fac_d['assigned_count'] = assigned_count
                dept_faculty_list.append(fac_d)

        # Sort faculty: those with assignments first, then alphabetical
        dept_faculty_list.sort(key=lambda x: (-x.get('assigned_count', 0), x.get('name', '')))

        # Determine active faculty
        req_fac = request.args.get('faculty_name', '').strip()
        matched_node_id = None

        # A. Query param match
        if req_fac:
            for fac in dept_faculty_list:
                if req_fac.lower() in fac.get('name', '').lower() or fac.get('node_id') == req_fac:
                    active_faculty = fac
                    matched_node_id = fac['node_id']
                    break

        # B. Current user username match
        if not active_faculty:
            uname = current_user.username.lower().replace('_', ' ')
            for fac in dept_faculty_list:
                fname = fac.get('name', '').lower()
                if uname in fname or fname in uname:
                    active_faculty = fac
                    matched_node_id = fac['node_id']
                    break

        # C. Default fallback: first faculty with assignments or first in list
        if not active_faculty and dept_faculty_list:
            active_faculty = dept_faculty_list[0]
            matched_node_id = active_faculty['node_id']

        # Extract assigned subjects, labs, and research areas for active faculty
        if matched_node_id:
            # Research areas
            research_areas = []
            for _, rnode, re_edge in graph.out_edges(matched_node_id, data=True):
                if re_edge.get('relationship') == 'researches':
                    r_name = graph.nodes[rnode]['data'].get('name')
                    if r_name:
                        research_areas.append(r_name)
            active_faculty['research_areas'] = research_areas

            # Assigned subjects via 'teaches' edges
            for _, snode, te_edge in graph.out_edges(matched_node_id, data=True):
                if te_edge.get('relationship') == 'teaches':
                    s_data = graph.nodes[snode]['data'].copy()
                    labs = []
                    for _, lnode, le_edge in graph.out_edges(snode, data=True):
                        if le_edge.get('relationship') == 'uses_lab':
                            lab_name = graph.nodes[lnode]['data'].get('name')
                            if lab_name:
                                labs.append(lab_name)
                    s_data['labs'] = labs
                    assigned_subjects.append(s_data)

            # Sort by semester
            assigned_subjects.sort(key=lambda x: x.get('semester') or 99)

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
        dept_faculty_list=dept_faculty_list,
        active_faculty=active_faculty,
        assigned_subjects=assigned_subjects,
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

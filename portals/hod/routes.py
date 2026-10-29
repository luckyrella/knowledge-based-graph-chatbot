import os
from flask import render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from auth.decorators import role_required
from models.database import db
from models.notice import Notice
from models.material import StudyMaterial
from . import hod_bp

@hod_bp.route('/')
@login_required
@role_required('hod', 'admin')
def dashboard():
    dept = current_user.department or 'CSE'
    
    # 1. Fetch Department Info from app.college_data
    college_data = getattr(current_app, 'college_data', {})
    dept_info = {}
    for d in college_data.get('departments', []):
        if d.get('short', '').lower() == dept.lower() or d.get('id', '').lower() == dept.lower() or dept.lower() in d.get('name', '').lower():
            dept_info = d
            break

    # 2. Fetch Department Faculty Roster
    faculty_list = []
    # Check faculty_data or college_data
    faculty_data = getattr(current_app.kg_builder, '_faculty_data', {}).get('faculty', {}) if hasattr(current_app, 'kg_builder') else {}
    dept_key_map = {
        'cse': 'computer_science_and_engineering',
        'aiml': 'cse_aiml',
        'cse_aiml': 'cse_aiml',
        'ds': 'cse_data_science',
        'cse_ds': 'cse_data_science',
        'cs': 'cse_cyber_security',
        'cse_cs': 'cse_cyber_security',
        'ece': 'electronics_and_communications',
        'civil': 'civil_engineering',
        'ce': 'civil_engineering',
        'mech': 'mechanical_engineering',
        'me': 'mechanical_engineering',
        'mba': 'mba'
    }
    fac_key = dept_key_map.get(dept.lower(), dept.lower())
    if fac_key in faculty_data:
        faculty_list = faculty_data[fac_key].get('staff', [])
    
    # 3. Department Notices
    dept_notices = Notice.query.filter(
        (Notice.department.ilike(f"%{dept}%")) | (Notice.department == None)
    ).order_by(Notice.created_at.desc()).all()
    
    # 4. Department Study Materials
    dept_materials = StudyMaterial.query.filter(
        StudyMaterial.department.ilike(f"%{dept}%")
    ).order_by(StudyMaterial.created_at.desc()).all()

    return render_template(
        'hod_dashboard.html',
        dept=dept,
        dept_info=dept_info,
        faculty_list=faculty_list,
        dept_notices=dept_notices,
        dept_materials=dept_materials
    )

@hod_bp.route('/publish-notice', methods=['POST'])
@login_required
@role_required('hod', 'admin')
def publish_notice():
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    dept = current_user.department or request.form.get('department', 'CSE')

    if not title or not content:
        flash("Title and Content are required to publish a notice.", "danger")
        return redirect(url_for('hod_bp.dashboard'))

    notice = Notice(
        title=title,
        content=content,
        department=dept,
        author_id=current_user.id,
        is_approved=True,
        is_ingested_to_kg=True
    )
    db.session.add(notice)
    db.session.commit()
    flash(f"Official Department Notice '{title}' broadcasted to Student Hub & Chatbot!", "success")
    return redirect(url_for('hod_bp.dashboard'))

@hod_bp.route('/delete-notice/<int:notice_id>', methods=['POST'])
@login_required
@role_required('hod', 'admin')
def delete_notice(notice_id):
    notice = db.session.get(Notice, notice_id)
    if not notice:
        flash("Notice not found.", "warning")
        return redirect(url_for('hod_bp.dashboard'))

    db.session.delete(notice)
    db.session.commit()
    flash("Notice removed successfully.", "info")
    return redirect(url_for('hod_bp.dashboard'))

@hod_bp.route('/delete-material/<int:material_id>', methods=['POST'])
@login_required
@role_required('hod', 'admin')
def delete_material(material_id):
    mat = db.session.get(StudyMaterial, material_id)
    if not mat:
        flash("Material not found.", "warning")
        return redirect(url_for('hod_bp.dashboard'))

    db.session.delete(mat)
    db.session.commit()
    flash(f"Material '{mat.title}' removed from Department Hub.", "info")
    return redirect(url_for('hod_bp.dashboard'))

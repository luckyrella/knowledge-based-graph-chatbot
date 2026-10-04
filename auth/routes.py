from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import auth_bp
from models.user import User
from models.database import db

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username_or_email = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()
        
        if user and user.check_password(password):
            if user.role != 'admin' and not user.is_approved:
                flash("Your account is pending admin approval.", "warning")
                return redirect(url_for('auth_bp.login'))
            
            login_user(user)
            flash("Logged in successfully.", "success")
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash("Invalid username or password.", "danger")
            
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role')
        department = request.form.get('department')
        
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('auth_bp.register'))
            
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username or email already exists.", "danger")
            return redirect(url_for('auth_bp.register'))
            
        new_user = User(
            username=username,
            email=email,
            role=role,
            department=department,
            is_approved=False
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful. Your account will be activated after admin approval.", "success")
        return redirect(url_for('auth_bp.login'))
        
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

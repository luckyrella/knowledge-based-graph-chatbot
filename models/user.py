from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from models.database import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(32), default='student', nullable=False) # 'admin', 'faculty', 'hod', 'placement_officer', 'student'
    department = db.Column(db.String(128), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role_name):
        return self.role == role_name

    def __repr__(self):
        return f'<User {self.username}>'

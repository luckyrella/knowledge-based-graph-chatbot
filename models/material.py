from models.database import db

class StudyMaterial(db.Model):
    __tablename__ = 'study_materials'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text, nullable=True)
    subject = db.Column(db.String(128), nullable=False)
    department = db.Column(db.String(128), nullable=False)
    semester = db.Column(db.Integer, nullable=True)
    file_path = db.Column(db.String(512), nullable=True)  # Path or link
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f'<StudyMaterial {self.title}>'

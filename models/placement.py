from models.database import db

class PlacementRecord(db.Model):
    __tablename__ = 'placement_records'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(128), nullable=False)
    package_lpa = db.Column(db.Float, nullable=False)
    department = db.Column(db.String(128), nullable=True)
    year = db.Column(db.Integer, nullable=False)
    students_placed = db.Column(db.Integer, nullable=False)
    drive_date = db.Column(db.DateTime, nullable=True)
    eligibility = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f'<PlacementRecord {self.company_name} {self.year}>'

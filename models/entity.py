from models.database import db

class KGEntity(db.Model):
    __tablename__ = 'kg_entities'

    id = db.Column(db.Integer, primary_key=True)
    entity_type = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    data = db.Column(db.Text, nullable=True) # JSON text
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __repr__(self):
        return f'<KGEntity {self.name} ({self.entity_type})>'

class KGRelationship(db.Model):
    __tablename__ = 'kg_relationships'

    id = db.Column(db.Integer, primary_key=True)
    source_entity_id = db.Column(db.Integer, db.ForeignKey('kg_entities.id'), nullable=False)
    target_entity_id = db.Column(db.Integer, db.ForeignKey('kg_entities.id'), nullable=False)
    relationship_type = db.Column(db.String(64), nullable=False)
    weight = db.Column(db.Float, default=1.0)
    metadata_ = db.Column('metadata', db.Text, nullable=True) # JSON text
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f'<KGRelationship {self.source_entity_id} -[{self.relationship_type}]-> {self.target_entity_id}>'

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Bind the SQLAlchemy instance to the app. Tables are created later in create_app()."""
    db.init_app(app)

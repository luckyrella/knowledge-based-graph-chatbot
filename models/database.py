import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Bind the SQLAlchemy instance to the app. Tables are created later in create_app()."""
    # Ensure instance directory exists for SQLite
    os.makedirs(app.instance_path, exist_ok=True)
    db.init_app(app)

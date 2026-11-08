import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
os.makedirs(INSTANCE_DIR, exist_ok=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    _db_url = os.environ.get('DATABASE_URL')
    if _db_url:
        if _db_url.startswith('postgres://'):
            _db_url = _db_url.replace('postgres://', 'postgresql+psycopg://', 1)
        elif _db_url.startswith('postgresql://') and not _db_url.startswith('postgresql+'):
            _db_url = _db_url.replace('postgresql://', 'postgresql+psycopg://', 1)

    SQLALCHEMY_DATABASE_URI = (
        _db_url or
        'sqlite:///' + os.path.join(INSTANCE_DIR, 'campus_kg.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

    # ── Neo4j Cloud / Local Graph Database Configuration ──────────────────────
    NEO4J_URI = os.environ.get('NEO4J_URI') # e.g. neo4j+s://xxxx.databases.neo4j.io
    NEO4J_USERNAME = os.environ.get('NEO4J_USERNAME', 'neo4j')
    NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD')
    NEO4J_DATABASE = os.environ.get('NEO4J_DATABASE', 'neo4j')

    # ── Rate Limiting (Production Security) ──────────────────────────────────
    RATELIMIT_DEFAULT = os.environ.get('RATELIMIT_DEFAULT', '300 per hour; 60 per minute')
    RATELIMIT_STORAGE_URI = os.environ.get('REDIS_URL', 'memory://')


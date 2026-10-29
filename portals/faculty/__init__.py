from flask import Blueprint

faculty_bp = Blueprint('faculty_bp', __name__, url_prefix='/faculty-portal', template_folder='templates')

from . import routes

from flask import Blueprint

hod_bp = Blueprint('hod_bp', __name__, url_prefix='/hod', template_folder='templates')

from . import routes

from flask import Blueprint

companies_api_blueprint = Blueprint('companies_api',
                             __name__,
                             template_folder='templates')

@companies_api_blueprint.route('/', methods=['GET'])
def index():
    return "COMPANIES API"

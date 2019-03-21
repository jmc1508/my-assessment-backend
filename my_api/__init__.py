from app import app
from flask_cors import CORS

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
from my_api.blueprints.users.views import users_api_blueprint
from my_api.blueprints.sessions.views import sessions_api_blueprint
from my_api.blueprints.companies.views import companies_api_blueprint

app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(companies_api_blueprint, url_prefix='/api/v1/companies')
app.register_blueprint(sessions_api_blueprint,url_prefix='/api/v1/')

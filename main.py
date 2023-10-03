from flask import Flask
from schemas.models import db
from routes.player_routes import player_routes
from routes.lineup_routes import lineup_routes

app = Flask(__name__)
app.app_context().push()


# Configure the PostgreSQL database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:database@localhost:5432/hockey'

# Initialize SQLAlchemy extension
db.init_app(app)

# Register blueprints for player and lineup routes
app.register_blueprint(player_routes, url_prefix='/api/players')
app.register_blueprint(lineup_routes, url_prefix='/api/lineups')

if __name__ == '__main__':
    app.run(debug=True)
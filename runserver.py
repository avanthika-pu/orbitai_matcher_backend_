# runserver.py
from app import create_app, db
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from flask_cors import CORS


load_dotenv()

app = create_app()

CORS(app)
# Initialize Flask-Migrate
migrate = Migrate(app, db)

if __name__ == '__main__':
    # Flask runs in debug mode if FLASK_ENV is not explicitly set to production
    app.run(host='0.0.0.0', port=5000)
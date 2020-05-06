# /run.py
import os
from dotenv import load_dotenv
from src.app import create_app, create_db

if __name__ == '__main__':
    # Load the environment variables
    load_dotenv(override=True)
    env_name = os.getenv('FLASK_ENV')
    db_url = os.getenv('DATABASE_URL')

    # Create database if doesn't exist
    create_db(db_url)
    # Create the application
    app = create_app(env_name)

    # Run the application
    app.run(debug=True)

# /run.py
import os
from src.app import create_app
from dotenv import load_dotenv 

if __name__ == '__main__':
  load_dotenv(override=True)
  env_name = os.getenv('FLASK_ENV')
  print(env_name)
  app = create_app(env_name)
  # run app
  app.run(debug=True)
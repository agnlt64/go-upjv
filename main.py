from app import create_app
from config import DEV, PROD
import os

app = create_app(config_name=PROD if os.getenv('FLASK_ENV') == 'prod' else DEV)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

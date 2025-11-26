# WSGI file, only used for production
from app import create_app
from config import PROD

app = create_app(config_name=PROD)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

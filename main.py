from app import create_app
from config import DEV

app = create_app(config_name=DEV)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

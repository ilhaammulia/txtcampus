from src.app import create_app
import os

app = create_app()

if __name__ == '__main__':
    app.run(port=int(os.environ.get('APP_PORT', 5000)), debug=bool(os.environ.get('APP_DEBUG')))

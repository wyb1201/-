from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    if not os.path.exists('app/static/uploads'):
        os.makedirs('app/static/uploads')
    app.run(debug=True)
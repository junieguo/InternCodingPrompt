from flask import Flask
from api.routes import tasks_bp

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(tasks_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

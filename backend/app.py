from flask import Flask
from routes.articles import articles_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Register articles blueprint
app.register_blueprint(articles_bp, url_prefix="/api/articles")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

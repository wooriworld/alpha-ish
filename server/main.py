import logging

from flask import Flask
from flask_cors import CORS

from routers.search import search_bp

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

CORS(
    app,
    origins=[
        "http://localhost:9000",
        "http://localhost:5173",
        "http://localhost:8080",
    ],
)

app.register_blueprint(search_bp, url_prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)

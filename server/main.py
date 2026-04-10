import logging
import threading

from dotenv import load_dotenv
from flask import Flask

load_dotenv()
from flask_cors import CORS

from routers.chart import chart_bp
from routers.search import search_bp
from services import dart_service

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
app.register_blueprint(chart_bp, url_prefix="/api")

# 서버 시작 시 백그라운드에서 DART 종목 리스트 미리 로드
threading.Thread(target=dart_service._get_corp_list, daemon=True).start()


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)

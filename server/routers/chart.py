from flask import Blueprint, jsonify, request

from services import chart_service

chart_bp = Blueprint("chart", __name__)


@chart_bp.get("/chart")
def get_chart():
    symbol = request.args.get("symbol", "").strip()
    interval = request.args.get("interval", "1d")
    range_ = request.args.get("range", "1y")

    if not symbol:
        return jsonify({"error": "symbol을 입력하세요."}), 400

    candles = chart_service.get_candles(symbol, interval=interval, range_=range_)
    return jsonify(candles)

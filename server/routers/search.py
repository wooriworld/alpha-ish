from flask import Blueprint, jsonify, request

from services import yahoo_service

search_bp = Blueprint("search", __name__)


@search_bp.get("/search")
def search_symbols():
    q = request.args.get("q", "").strip()
    market = request.args.get("market", "ALL").upper()
    limit = min(int(request.args.get("limit", 10)), 30)

    if not q:
        return jsonify({"error": "검색어를 입력하세요."}), 400

    if market not in ("ALL", "KRX", "US"):
        return jsonify({"error": "market은 ALL, KRX, US 중 하나여야 합니다."}), 400

    results = yahoo_service.search_symbols(q, market=market, limit=limit)
    return jsonify(results)

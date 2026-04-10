from flask import Blueprint, jsonify, request

from services import dart_service, yahoo_service

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

    if market == "KRX":
        results = dart_service.search_symbols(q, limit=limit)
    elif market == "US":
        results = yahoo_service.search_symbols(q, market="US", limit=limit)
    else:
        krx = dart_service.search_symbols(q, limit=limit)
        us = yahoo_service.search_symbols(q, market="US", limit=limit)
        results = (krx + us)[:limit]

    return jsonify(results)

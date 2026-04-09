import logging
from typing import List

import requests

logger = logging.getLogger(__name__)

YAHOO_SEARCH_URL = "https://query1.finance.yahoo.com/v1/finance/search"

# 거래소 코드 → MarketType 매핑
KRX_EXCHANGES = {"KSC", "KOE", "KPQ"}  # KOSPI, KOSDAQ, KONEX
US_EXCHANGES = {"NMS", "NYQ", "NGM", "PCX", "ASE", "BTS", "NCM"}


def _detect_market(exchange: str) -> str | None:
    if exchange in KRX_EXCHANGES:
        return "KRX"
    if exchange in US_EXCHANGES:
        return "US"
    return None


def search_symbols(query: str, market: str = "ALL", limit: int = 15) -> List[dict]:
    try:
        resp = requests.get(
            YAHOO_SEARCH_URL,
            params={"q": query, "quotesCount": limit * 2, "newsCount": 0},
            timeout=5,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        resp.raise_for_status()
        data = resp.json()

        results = []
        for quote in data.get("quotes", []):
            exchange = quote.get("exchange", "")
            detected = _detect_market(exchange)
            if detected is None:
                continue
            if market != "ALL" and detected != market:
                continue

            results.append(
                {
                    "symbol": quote.get("symbol", ""),
                    "display_symbol": quote.get("symbol", "").split(".")[0],
                    "description": quote.get("longname") or quote.get("shortname", ""),
                    "market": detected,
                    "type": quote.get("quoteType", "EQUITY"),
                }
            )
            if len(results) >= limit:
                break

        return results
    except Exception as e:
        logger.error(f"Yahoo Finance 검색 실패: {e}")
        return []

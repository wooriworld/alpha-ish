import logging
import re
from typing import List

import requests

logger = logging.getLogger(__name__)

YAHOO_SEARCH_URL = "https://query1.finance.yahoo.com/v1/finance/search"

KRX_EXCHANGES = {"KSC", "KOE", "KPQ"}
US_EXCHANGES = {"NMS", "NYQ", "NGM", "PCX", "ASE", "BTS", "NCM"}

EXCHANGE_NAME_MAP = {
    "KSC": "KOSPI",
    "KOE": "KOSDAQ",
    "KPQ": "KONEX",
    "NMS": "NASDAQ",
    "NYQ": "NYSE",
    "NGM": "NASDAQ GM",
    "PCX": "NYSE Arca",
    "ASE": "NYSE American",
    "BTS": "OTC Markets",
    "NCM": "NASDAQ CM",
}

_KO_RE = re.compile(r"[\uac00-\ud7a3]")


def _detect_market(exchange: str) -> str | None:
    if exchange in KRX_EXCHANGES:
        return "KRX"
    if exchange in US_EXCHANGES:
        return "US"
    return None


def _split_names(shortname: str, longname: str) -> tuple[str, str]:
    """(name_kr, name_en) 반환. 한글 포함 여부로 분리."""
    if _KO_RE.search(shortname):
        return shortname, longname or shortname
    if _KO_RE.search(longname):
        return longname, shortname or longname
    return "", longname or shortname


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

            shortname = quote.get("shortname", "")
            longname = quote.get("longname", "")
            name_kr, name_en = _split_names(shortname, longname)

            results.append(
                {
                    "symbol": quote.get("symbol", ""),
                    "display_symbol": quote.get("symbol", "").split(".")[0],
                    "description": name_en,
                    "name_kr": name_kr,
                    "market": detected,
                    "exchange_name": EXCHANGE_NAME_MAP.get(exchange, exchange),
                    "logo_url": quote.get("logoUrl", ""),
                    "type": quote.get("quoteType", "EQUITY"),
                }
            )
            if len(results) >= limit:
                break

        return results
    except Exception as e:
        logger.error(f"Yahoo Finance 검색 실패: {e}")
        return []

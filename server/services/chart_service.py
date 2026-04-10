import logging

import requests

logger = logging.getLogger(__name__)

YAHOO_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"

INTERVAL_MAP = {
    "1d": "1d",
    "1wk": "1wk",
    "1mo": "1mo",
}

RANGE_MAP = {
    "1d": "1d",
    "1mo": "1mo",
    "3mo": "3mo",
    "6mo": "6mo",
    "1y": "1y",
    "2y": "2y",
    "5y": "5y",
}


def get_candles(symbol: str, interval: str = "1d", range_: str = "1y") -> list[dict]:
    interval = INTERVAL_MAP.get(interval, "1d")
    range_ = RANGE_MAP.get(range_, "1y")

    try:
        resp = requests.get(
            YAHOO_CHART_URL.format(symbol=symbol),
            params={"interval": interval, "range": range_},
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        resp.raise_for_status()
        data = resp.json()

        result = data.get("chart", {}).get("result", [])
        if not result:
            return []

        chart = result[0]
        timestamps = chart.get("timestamp", [])
        indicators = chart.get("indicators", {})
        quotes = indicators.get("quote", [{}])[0]

        opens = quotes.get("open", [])
        highs = quotes.get("high", [])
        lows = quotes.get("low", [])
        closes = quotes.get("close", [])
        volumes = quotes.get("volume", [])

        candles = []
        for i, ts in enumerate(timestamps):
            o = opens[i] if i < len(opens) else None
            h = highs[i] if i < len(highs) else None
            l = lows[i] if i < len(lows) else None
            c = closes[i] if i < len(closes) else None

            if None in (o, h, l, c):
                continue

            candles.append({
                "time": ts,
                "open": round(o, 4),
                "high": round(h, 4),
                "low": round(l, 4),
                "close": round(c, 4),
                "volume": volumes[i] if i < len(volumes) else 0,
            })

        return candles

    except Exception as e:
        logger.error(f"차트 데이터 조회 실패 ({symbol}): {e}")
        return []

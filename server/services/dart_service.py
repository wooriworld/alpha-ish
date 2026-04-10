import concurrent.futures
import io
import logging
import os
import threading
import time
import zipfile
import xml.etree.ElementTree as ET
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DART_BASE_URL = "https://opendart.fss.or.kr/api"

CORP_CLS_MAP = {
    "Y": "KOSPI",
    "K": "KOSDAQ",
    "N": "KONEX",
}
SUFFIX_MAP = {
    "Y": ".KS",
    "K": ".KQ",
    "N": ".KQ",
}

# 전체 종목 리스트 캐시 (24시간)
_corp_list: list[dict] = []
_corp_list_lock = threading.Lock()
_corp_list_time: float = 0
CORP_LIST_TTL = 86400

# corp_code → corp_cls 영구 캐시 (서버 실행 중 유지)
_corp_cls_cache: dict[str, str] = {}
_corp_cls_lock = threading.Lock()


def _load_corp_list(api_key: str) -> list[dict]:
    """DART corpCode.xml ZIP 다운로드 후 상장 종목만 파싱."""
    resp = requests.get(
        f"{DART_BASE_URL}/corpCode.xml",
        params={"crtfc_key": api_key},
        timeout=30,
    )
    resp.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
        xml_name = next(n for n in z.namelist() if n.endswith(".xml"))
        with z.open(xml_name) as f:
            tree = ET.parse(f)

    corps = []
    for item in tree.getroot().findall("list"):
        stock_code = (item.findtext("stock_code") or "").strip()
        if not stock_code:
            continue
        corps.append({
            "corp_code": (item.findtext("corp_code") or "").strip(),
            "corp_name": (item.findtext("corp_name") or "").strip(),
            "stock_code": stock_code,
        })

    logger.info(f"DART 기업 목록 로드 완료: {len(corps)}개")
    return corps


def _get_corp_list() -> list[dict]:
    global _corp_list, _corp_list_time

    with _corp_list_lock:
        now = time.time()
        if _corp_list and (now - _corp_list_time) < CORP_LIST_TTL:
            return _corp_list

        api_key = os.getenv("DART_API_KEY", "")
        if not api_key:
            logger.error("DART_API_KEY가 설정되지 않았습니다.")
            return _corp_list

        try:
            _corp_list = _load_corp_list(api_key)
            _corp_list_time = now
        except Exception as e:
            logger.error(f"DART 기업 목록 로드 실패: {e}")

        return _corp_list


def _fetch_corp_cls(corp_code: str, api_key: str) -> Optional[str]:
    """단일 기업의 corp_cls 조회."""
    try:
        resp = requests.get(
            f"{DART_BASE_URL}/company.json",
            params={"crtfc_key": api_key, "corp_code": corp_code},
            timeout=3,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") == "000":
            return data.get("corp_cls")
    except Exception:
        pass
    return None


def _resolve_corp_cls(corps: list[dict], api_key: str) -> dict[str, str]:
    """corp_cls 캐시 미스 항목만 병렬 조회 후 캐시에 저장."""
    with _corp_cls_lock:
        missing = [c for c in corps if c["corp_code"] not in _corp_cls_cache]

    if not missing:
        with _corp_cls_lock:
            return {c["corp_code"]: _corp_cls_cache.get(c["corp_code"], "") for c in corps}

    fetched: dict[str, str] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(missing), 10)) as executor:
        future_map = {
            executor.submit(_fetch_corp_cls, c["corp_code"], api_key): c["corp_code"]
            for c in missing
        }
        for future in concurrent.futures.as_completed(future_map, timeout=5):
            corp_code = future_map[future]
            cls = future.result()
            if cls:
                fetched[corp_code] = cls

    with _corp_cls_lock:
        _corp_cls_cache.update(fetched)
        return {c["corp_code"]: _corp_cls_cache.get(c["corp_code"], "") for c in corps}


def search_symbols(query: str, limit: int = 15) -> list[dict]:
    corp_list = _get_corp_list()
    if not corp_list:
        return []

    matched = [c for c in corp_list if query in c["corp_name"]]
    # 1순위: 완전 일치, 2순위: query로 시작, 3순위: 포함 / 동순위 내에서는 이름 길이 짧은 순
    matched.sort(key=lambda c: (
        0 if c["corp_name"] == query else (1 if c["corp_name"].startswith(query) else 2),
        len(c["corp_name"])
    ))
    matched = matched[:limit]

    if not matched:
        return []

    api_key = os.getenv("DART_API_KEY", "")
    cls_map = _resolve_corp_cls(matched, api_key)

    results = []
    for corp in matched:
        corp_cls = cls_map.get(corp["corp_code"], "")
        exchange_name = CORP_CLS_MAP.get(corp_cls, "KRX")
        suffix = SUFFIX_MAP.get(corp_cls, ".KS")

        results.append({
            "symbol": f"{corp['stock_code']}{suffix}",
            "display_symbol": corp["stock_code"],
            "description": corp["corp_name"],
            "name_kr": corp["corp_name"],
            "market": "KRX",
            "exchange_name": exchange_name,
            "logo_url": "",
            "type": "EQUITY",
        })

    return results

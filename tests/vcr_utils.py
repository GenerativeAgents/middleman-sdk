# VCRテストでは、例えばSTGに向けてテストした場合と本番に向けてテストした場合など
# 環境差異によって生じるリクエスト内容の差異があるとエラーになってしまう
# かといってリクエストボディを丸ごとignoreするとテストにならないので
# 環境差異を吸収するための関数をここに定義し、
# それぞれのテストで環境差異が発生する部分をマスクしてカセットを登録できるようにする

import copy
import json
from collections.abc import Callable
from typing import Any
from urllib.parse import urlparse, urlunparse


def _filter_value_in_request_body(request: Any, key: str, replace_value: str) -> Any:
    """
    共通ロジック：
    リクエストボディが JSON である場合、一致する key があれば置き換える
    """
    try:
        body = json.loads(request.body.decode())
    except Exception:
        return request
    if key in body:
        body[key] = replace_value
        request.body = json.dumps(body).encode()
    return request


def _generate_filter_request_body_function(key: str, replace_value: str) -> Callable:
    """
    VCRテストで環境依存な値をマスクするための関数（リクエストボディ用）
    """
    return lambda request: _filter_value_in_request_body(request, key, replace_value)


def _mask_request_uri(request: Any) -> Any:
    """
    本番環境以外のURLが露出することを避けるなどカセットに秘匿情報が出ないための処置を行う
    """
    req = copy.deepcopy(request)
    p = urlparse(req.uri)
    redacted = urlunparse(
        (p.scheme, "middleman-ai.com", p.path, p.params, p.query, p.fragment)
    )
    req.uri = redacted
    return req


def scrub_request(request: Any) -> Any:
    """
    環境差異によってエラーが発生しないよう、環境依存のパラメータの値をカセットに記録する差異に統一する
    """
    # リクエストのURI からホスト名を標準化してmiddleman-ai.comに置換する
    # 本番環境以外のURLが露出することを避けるための処置です
    req = _mask_request_uri(request)

    p = urlparse(req.uri)
    request_path = p.path
    if "md-to-pdf" in request_path:
        req = _filter_value_in_request_body(req, "pdf_template_id", "TEMPLATE_ID")
    if "md-to-docx" in request_path:
        req = _filter_value_in_request_body(req, "docx_template_id", "TEMPLATE_ID")
    if "json-to-pptx" in request_path:
        req = _filter_value_in_request_body(req, "pptx_template_id", "TEMPLATE_ID")
    if "xlsx-to-pdf" in request_path:
        req = _filter_value_in_request_body(req, "xlsx_template_id", "TEMPLATE_ID")
    return req


def scrub_response(response: Any) -> Any:
    """レスポンスの機密情報や環境依存情報を削除・置換する

    特定のヘッダー（x-middleware-rewrite, x-request-id など）を削除し、
    レスポンス中のURLを標準化します。
    """
    # レスポンス本体のディープコピーを作成
    resp = copy.deepcopy(response)

    # 環境依存の情報が含まれるヘッダーを削除または置換
    headers_to_filter = [
        "x-middleware-rewrite",
        "x-request-id",
        "date",
        "server",
        "set-cookie",
    ]

    for header in headers_to_filter:
        if header in resp["headers"]:
            resp["headers"][header] = ["FILTERED"]

    # リダイレクト先URLがあればそれも標準化
    if "location" in resp["headers"]:
        location = resp["headers"]["location"][0]
        p = urlparse(location)
        if p.netloc and "middleman-ai.com" in p.netloc:
            standardized = urlunparse(
                (p.scheme, "middleman-ai.com", p.path, p.params, p.query, p.fragment)
            )
            resp["headers"]["location"] = [standardized]

    # レスポンス本文内のURLパターンも置換できますが、ここでは実装していません

    return resp

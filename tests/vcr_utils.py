# VCRテストでは、例えばSTGに向けてテストした場合と本番に向けてテストした場合など
# 環境差異によって生じるリクエスト内容の差異があるとエラーになってしまう
# かといってリクエストボディを丸ごとignoreするとテストにならないので
# 環境差異を吸収するための関数をここに定義し、
# それぞれのテストで環境差異が発生する部分をマスクしてカセットを登録できるようにする


import json
from collections.abc import Callable
from typing import Any


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


def generate_filter_request_body_function(key: str, replace_value: str) -> Callable:
    """
    VCRテストで環境依存な値をマスクするための関数（リクエストボディ用）
    """
    return lambda request: _filter_value_in_request_body(request, key, replace_value)

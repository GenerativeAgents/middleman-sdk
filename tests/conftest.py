"""テスト実行のための設定モジュール。"""

import copy
import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict
from urllib.parse import urlparse, urlunparse

import pytest
from dotenv import load_dotenv
from vcr.cassette import Cassette  # type: ignore
from vcr.stubs import VCRHTTPResponse  # type: ignore

if TYPE_CHECKING:
    from pytest_mock import MockerFixture  # noqa: F401


def pytest_configure(config: pytest.Config) -> None:
    """テスト実行前の設定を行います。"""
    # vcrマークを登録
    config.addinivalue_line("markers", "vcr: mark test to use VCR.py cassettes")

    # ロギングの設定
    log_level = os.getenv("LOG_LEVEL", "INFO")
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        force=True,
    )

    # urllib3のデバッグログを無効化
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    env_file = Path(__file__).parent.parent / ".env.test"

    if env_file.exists():
        load_dotenv(env_file)

    # Skip API key check for CLI tests which use mocks
    if "test_cli.py" not in str(config.invocation_params.dir):
        if not os.getenv("MIDDLEMAN_API_KEY"):
            pytest.skip("MIDDLEMAN_API_KEY is not set")


# オリジナルの play_response メソッドを保存
_original_play_response = Cassette.play_response


def patched_play_response(self: Cassette, request: Any) -> Any:
    """VCRHTTPResponseにversion_stringを追加するパッチ関数。"""
    # オリジナル処理で VCRHTTPResponse オブジェクトを生成
    resp = _original_play_response(self, request)

    # VCRHTTPResponseの場合のみversion_stringを追加
    if isinstance(resp, VCRHTTPResponse):
        resp.version_string = "HTTP/1.1"
    return resp


# Cassette.play_response をパッチする
Cassette.play_response = patched_play_response


# VCRHTTPResponseにversion_stringプロパティを追加
def _get_version_string(self: VCRHTTPResponse) -> str:
    return "HTTP/1.1"


def _set_version_string(self: VCRHTTPResponse, value: str) -> None:
    pass


VCRHTTPResponse.version_string = property(_get_version_string, _set_version_string)


def scrub_uri_request(request: Any) -> Any:
    """リクエストのURI からホスト名を標準化してmiddleman-ai.comに置換する"""
    req = copy.deepcopy(request)  # ミュータブルに触らず安全に
    p = urlparse(req.uri)
    redacted = urlunparse(
        (p.scheme, "middleman-ai.com", p.path, p.params, p.query, p.fragment)
    )
    req.uri = redacted
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


@pytest.fixture(scope="module")
def vcr_config() -> Dict[str, Any]:
    """VCRの設定を行います。

    Returns:
        Dict[str, Any]: VCRの設定辞書
    """
    return {
        "filter_headers": [
            ("authorization", "DUMMY"),
        ],
        "record_mode": "once",
        "match_on": ["method", "path", "query", "body"],
        "ignore_localhost": True,
        "before_record_request": scrub_uri_request,
        "before_record_response": scrub_response,
    }

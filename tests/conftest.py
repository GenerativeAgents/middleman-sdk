"""テスト実行のための設定モジュール。"""

import logging
import os
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict

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

    # urllib3のデバッグログを無効化
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    env_file = Path(__file__).parent.parent / ".env.test"

    if env_file.exists():
        load_dotenv(env_file)

    # Register markers
    config.addinivalue_line(
        "markers",
        "requires_api_key: mark test that requires MIDDLEMAN_API_KEY"
    )


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """テストコレクションの修正を行います。"""
    for item in items:
        # Skip non-CLI tests when API key is missing
        if (
            "test_cli.py" not in str(item.path)
            and not os.getenv("MIDDLEMAN_API_KEY")
        ):
            item.add_marker(pytest.mark.skip(reason="MIDDLEMAN_API_KEY is not set"))
            item.add_marker(pytest.mark.requires_api_key)


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


@pytest.fixture(scope="module")
def vcr_config() -> Dict[str, Any]:
    """VCRの設定を行います。

    Returns:
        Dict[str, Any]: VCRの設定辞書
    """
    return {
        "filter_headers": [
            ('authorization', 'DUMMY'),
            ('user-agent', None),
            ('accept-encoding', None)
        ],
        "record_mode": "once",
        "match_on": ["method", "scheme", "host", "port", "path"],
        "ignore_localhost": True,
        "ignore_hosts": ["api.middleman.ai"],  # APIホストも無視するように追加
        "decode_compressed_response": True,
        "before_record_request": lambda r: r,
        "before_record_response": lambda r: r,
        "serializer": "yaml",
        "filter_headers": [
            ('authorization', 'DUMMY'),
            ('user-agent', None),
            ('accept-encoding', None),
            ('content-type', None)
        ],
        "record_mode": "once",
        "filter_post_data_parameters": [
            ('file', None),
            ('pptx_template_id', None),
            ('presentation', None)
        ],
        "filter_query_parameters": [
            ('api_key', None)
        ]
    }

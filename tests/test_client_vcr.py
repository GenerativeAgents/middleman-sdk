"""LangChainツール群のVCRテストモジュール。"""

import os
from typing import TYPE_CHECKING

import pytest

from middleman_ai.client import ToolsClient

if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest

@pytest.fixture
def client() -> ToolsClient:
    """テスト用のToolsClientインスタンスを生成します。

    Returns:
        ToolsClient: テスト用のクライアントインスタンス
    """
    return ToolsClient(api_key=os.getenv("MIDDLEMAN_API_KEY") or "")

@pytest.mark.vcr()
def test_md_to_pdf_vcr(client: ToolsClient) -> None:
    """ToolsClient.md_to_pdfの実際のAPIを使用したテスト。

    Note:
        このテストは実際のAPIを呼び出し、レスポンスをキャッシュします。
        初回実行時のみAPIを呼び出し、以降はキャッシュを使用します。
    """
    test_markdown = """# Test Heading

    This is a test markdown document.

    ## Section 1
    - Item 1
    - Item 2
    """
    pdf_url = client.md_to_pdf(markdown_text=test_markdown)
    assert pdf_url.startswith("https://")
    assert "md-to-pdf" in pdf_url
    assert "blob.core.windows.net" in pdf_url

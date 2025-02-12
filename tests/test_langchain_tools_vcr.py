"""LangChainツール群のVCRテストモジュール。"""

import json
import os
from typing import TYPE_CHECKING

import pytest

from middleman_ai.client import ToolsClient
from middleman_ai.langchain_tools.md_to_pdf import MdToPdfTool
from middleman_ai.langchain_tools.md_to_docx import MdToDocxTool
from middleman_ai.langchain_tools.md_to_pptx import MdToPptxTool
from middleman_ai.langchain_tools.pdf_to_page_images import PdfToPageImagesTool
from middleman_ai.langchain_tools.json_to_pptx import (
    JsonToPptxAnalyzeTool,
    JsonToPptxExecuteTool,
)

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
def test_md_to_pdf_tool_vcr(client: ToolsClient) -> None:
    """MdToPdfToolの実際のAPIを使用したテスト。

    Note:
        このテストは実際のAPIを呼び出し、レスポンスをキャッシュします。
        初回実行時のみAPIを呼び出し、以降はキャッシュを使用します。

    Args:
        client: テスト用のクライアントインスタンス
    """
    test_markdown = """# Test Heading

    This is a test markdown document.

    ## Section 1
    - Item 1
    - Item 2
    """

    tool = MdToPdfTool(client=client)
    result = tool._run(test_markdown)

    assert isinstance(result, str)
    assert result.startswith("https://")
    assert "md-to-pdf" in result
    assert "blob.core.windows.net" in result


@pytest.mark.vcr()
def test_md_to_docx_tool_vcr(client: ToolsClient) -> None:
    """MdToDocxToolの実際のAPIを使用したテスト。

    Note:
        このテストは実際のAPIを呼び出し、レスポンスをキャッシュします。
        初回実行時のみAPIを呼び出し、以降はキャッシュを使用します。

    Args:
        client: テスト用のクライアントインスタンス
    """
    test_markdown = """# Test Heading

    This is a test markdown document.

    ## Section 1
    - Item 1
    - Item 2
    """

    tool = MdToDocxTool(client=client)
    result = tool._run(test_markdown)

    assert isinstance(result, str)
    assert result.startswith("https://")
    assert "md-to-docx" in result
    assert "blob.core.windows.net" in result


@pytest.mark.vcr()
def test_md_to_pptx_tool_vcr(client: ToolsClient) -> None:
    """MdToPptxToolの実際のAPIを使用したテスト。

    Note:
        このテストは実際のAPIを呼び出し、レスポンスをキャッシュします。
        初回実行時のみAPIを呼び出し、以降はキャッシュを使用します。

    Args:
        client: テスト用のクライアントインスタンス
    """
    test_markdown = """# Test Heading

    This is a test markdown document.

    ## Section 1
    - Item 1
    - Item 2
    """

    tool = MdToPptxTool(client=client)
    result = tool._run(test_markdown)

    assert isinstance(result, str)
    assert result.startswith("https://")
    assert "md-to-pptx" in result
    assert "blob.core.windows.net" in result


@pytest.mark.vcr()
def test_pdf_to_page_images_tool_vcr(client: ToolsClient) -> None:
    """PdfToPageImagesToolの実際のAPIを使用したテスト。

    Note:
        このテストは実際のAPIを呼び出し、レスポンスをキャッシュします。
        初回実行時のみAPIを呼び出し、以降はキャッシュを使用します。

    Args:
        client: テスト用のクライアントインスタンス
    """
    pdf_path = "tests/data/test.pdf"
    
    tool = PdfToPageImagesTool(client=client)
    result = tool._run(pdf_path)

    assert isinstance(result, str)
    assert "pdf-to-page-images" in result
    assert "blob.core.windows.net" in result


@pytest.mark.vcr()
def test_json_to_pptx_analyze_tool_vcr(client: ToolsClient) -> None:
    """JsonToPptxAnalyzeToolの実際のAPIを使用したテスト。

    Note:
        このテストは実際のAPIを呼び出し、レスポンスをキャッシュします。
        初回実行時のみAPIを呼び出し、以降はキャッシュを使用します。

    Args:
        client: テスト用のクライアントインスタンス
    """
    tool = JsonToPptxAnalyzeTool(client=client)
    result = tool._run("0bb238bd-d03a-4f1a-be6f-fe2e0c6e91f7")

    assert isinstance(result, str)
    assert "Slide" in result


@pytest.mark.vcr()
def test_json_to_pptx_execute_tool_vcr(client: ToolsClient) -> None:
    """JsonToPptxExecuteToolの実際のAPIを使用したテスト。

    Note:
        このテストは実際のAPIを呼び出し、レスポンスをキャッシュします。
        初回実行時のみAPIを呼び出し、以降はキャッシュを使用します。

    Args:
        client: テスト用のクライアントインスタンス
    """
    presentation_data = {
        "slides": [
            {"type": "title", "placeholders": [
                {"name": "title", "content": "Test Title"},
                {"name": "subtitle", "content": "Test Subtitle"}
            ]}
        ]
    }
    
    tool = JsonToPptxExecuteTool(client=client)
    result = tool._run(
        slide_json_str=json.dumps(presentation_data),
        template_id="0bb238bd-d03a-4f1a-be6f-fe2e0c6e91f7"
    )

    assert isinstance(result, str)
    assert result.startswith("https://")
    assert "json-to-pptx" in result
    assert "blob.core.windows.net" in result

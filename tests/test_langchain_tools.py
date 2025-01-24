"""LangChainツール群のテストモジュール。"""

import json
from typing import TYPE_CHECKING

import pytest

from middleman_ai.client import ToolsClient
from middleman_ai.langchain_tools.json_to_pptx import (
    JsonToPptxAnalyzeTool,
    JsonToPptxExecuteTool,
)
from middleman_ai.langchain_tools.md_to_docx import MdToDocxTool
from middleman_ai.langchain_tools.md_to_pdf import MdToPdfTool
from middleman_ai.langchain_tools.md_to_pptx import MdToPptxTool
from middleman_ai.langchain_tools.pdf_to_page_images import PdfToPageImagesTool

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


@pytest.fixture
def client() -> ToolsClient:
    """テスト用のToolsClientインスタンスを生成します。"""
    return ToolsClient(api_key="test_api_key")


def test_md_to_pdf_tool(client: ToolsClient, mocker: "MockerFixture") -> None:
    """MdToPdfToolのテスト。"""
    mock_md_to_pdf = mocker.patch.object(
        client,
        "md_to_pdf",
        return_value="https://example.com/test.pdf",
    )

    tool = MdToPdfTool(client=client)
    result = tool._run("# Test")

    assert result == "https://example.com/test.pdf"
    mock_md_to_pdf.assert_called_once_with("# Test")


def test_md_to_docx_tool(client: ToolsClient, mocker: "MockerFixture") -> None:
    """MdToDocxToolのテスト。"""
    mock_md_to_docx = mocker.patch.object(
        client,
        "md_to_docx",
        return_value="https://example.com/test.docx",
    )

    tool = MdToDocxTool(client=client)
    result = tool._run("# Test")

    assert result == "https://example.com/test.docx"
    mock_md_to_docx.assert_called_once_with("# Test")


def test_md_to_pptx_tool(client: ToolsClient, mocker: "MockerFixture") -> None:
    """MdToPptxToolのテスト。"""
    mock_md_to_pptx = mocker.patch.object(
        client,
        "md_to_pptx",
        return_value="https://example.com/test.pptx",
    )

    tool = MdToPptxTool(client=client)
    result = tool._run("# Test")

    assert result == "https://example.com/test.pptx"
    mock_md_to_pptx.assert_called_once_with("# Test")


def test_pdf_to_page_images_tool(client: ToolsClient, mocker: "MockerFixture") -> None:
    """PdfToPageImagesToolのテスト。"""
    expected_result = [
        {"page_no": 1, "image_url": "https://example.com/page1.png"},
        {"page_no": 2, "image_url": "https://example.com/page2.png"},
    ]
    mock_pdf_to_page_images = mocker.patch.object(
        client,
        "pdf_to_page_images",
        return_value=expected_result,
    )

    tool = PdfToPageImagesTool(client=client)
    result = tool._run("/path/to/test.pdf")

    assert isinstance(result, str)
    assert "https://example.com/page1.png" in result
    assert "https://example.com/page2.png" in result
    mock_pdf_to_page_images.assert_called_once_with("/path/to/test.pdf")


def test_json_to_pptx_analyze_tool(
    client: ToolsClient, mocker: "MockerFixture"
) -> None:
    """JsonToPptxAnalyzeToolのテスト。"""
    template_structure = {
        "slides": [
            {"title": "Title Slide", "placeholders": ["title", "subtitle"]},
            {"title": "Content Slide", "placeholders": ["title", "content"]},
        ]
    }
    mock_analyze = mocker.patch.object(
        client,
        "json_to_pptx_analyze_v2",
        return_value=template_structure,
    )

    tool = JsonToPptxAnalyzeTool(client=client)
    result = tool._run("template-123")

    assert isinstance(result, str)
    assert "Title Slide" in result
    assert "Content Slide" in result
    mock_analyze.assert_called_once_with("template-123")


def test_json_to_pptx_execute_tool(
    client: ToolsClient, mocker: "MockerFixture"
) -> None:
    """JsonToPptxExecuteToolのテスト。"""
    template_id = "template-123"
    presentation_data = {
        "slides": [
            {"title": "My Title", "subtitle": "My Subtitle"},
            {"title": "Content", "content": "Some content"},
        ]
    }
    mock_execute = mocker.patch.object(
        client,
        "json_to_pptx_execute_v2",
        return_value="https://example.com/result.pptx",
    )

    tool = JsonToPptxExecuteTool(client=client)
    result = tool._run(f"{template_id},{json.dumps(presentation_data)}")

    assert result == "https://example.com/result.pptx"
    mock_execute.assert_called_once_with(template_id, presentation_data)

"""MCPサーバーのテストモジュール。"""

from typing import TYPE_CHECKING

from mcp.server.fastmcp import FastMCP

from middleman_ai.client import Presentation, Slide
from middleman_ai.mcp.server import (
    docx_to_page_images,
    json_to_pptx_analyze,
    json_to_pptx_execute,
    mcp,
    md_to_docx,
    md_to_pdf,
    pdf_to_page_images,
    pptx_to_page_images,
    run_server,
    xlsx_to_page_images,
)

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


def test_mcp_instance() -> None:
    """MCPサーバーインスタンスのテスト。"""
    assert isinstance(mcp, FastMCP)
    assert mcp.name == "Middleman Tools"


def test_md_to_pdf_tool(mocker: "MockerFixture") -> None:
    """md_to_pdfツールのテスト。"""
    mock_client = mocker.patch("middleman_ai.mcp.server.client")
    mock_client.md_to_pdf.return_value = "https://example.com/test.pdf"

    result = md_to_pdf("# Test")

    assert result == "https://example.com/test.pdf"
    mock_client.md_to_pdf.assert_called_once_with("# Test", pdf_template_id=None)


def test_md_to_docx_tool(mocker: "MockerFixture") -> None:
    """md_to_docxツールのテスト。"""
    mock_client = mocker.patch("middleman_ai.mcp.server.client")
    mock_client.md_to_docx.return_value = "https://example.com/test.docx"

    result = md_to_docx("# Test")

    assert result == "https://example.com/test.docx"
    mock_client.md_to_docx.assert_called_once_with("# Test")


def test_pptx_to_page_images_tool(mocker: "MockerFixture") -> None:
    """pptx_to_page_imagesツールのテスト。"""
    expected_result = [
        {"page_no": 1, "image_url": "https://example.com/slide1.png"},
        {"page_no": 2, "image_url": "https://example.com/slide2.png"},
    ]
    mock_client = mocker.patch("middleman_ai.mcp.server.client")
    mock_client.pptx_to_page_images.return_value = expected_result

    result = pptx_to_page_images("/path/to/test.pptx")

    assert result == expected_result
    mock_client.pptx_to_page_images.assert_called_once_with("/path/to/test.pptx")


def test_docx_to_page_images_tool(mocker: "MockerFixture") -> None:
    """docx_to_page_imagesツールのテスト。"""
    expected_result = [
        {"page_no": 1, "image_url": "https://example.com/page1.png"},
        {"page_no": 2, "image_url": "https://example.com/page2.png"},
    ]
    mock_client = mocker.patch("middleman_ai.mcp.server.client")
    mock_client.docx_to_page_images.return_value = expected_result

    result = docx_to_page_images("/path/to/test.docx")

    assert result == expected_result
    mock_client.docx_to_page_images.assert_called_once_with("/path/to/test.docx")


def test_xlsx_to_page_images_tool(mocker: "MockerFixture") -> None:
    """xlsx_to_page_imagesツールのテスト。"""
    expected_result = [
        {"sheet_name": "Sheet1", "image_url": "https://example.com/sheet1.png"},
        {"sheet_name": "Sheet2", "image_url": "https://example.com/sheet2.png"},
    ]
    mock_client = mocker.patch("middleman_ai.mcp.server.client")
    mock_client.xlsx_to_page_images.return_value = expected_result

    result = xlsx_to_page_images("/path/to/test.xlsx")

    assert result == expected_result
    mock_client.xlsx_to_page_images.assert_called_once_with("/path/to/test.xlsx")


def test_pdf_to_page_images_tool(mocker: "MockerFixture") -> None:
    """pdf_to_page_imagesツールのテスト。"""
    expected_result = [
        {"page_no": 1, "image_url": "https://example.com/page1.png"},
        {"page_no": 2, "image_url": "https://example.com/page2.png"},
    ]
    mock_client = mocker.patch("middleman_ai.mcp.server.client")
    mock_client.pdf_to_page_images.return_value = expected_result

    result = pdf_to_page_images("/path/to/test.pdf")

    assert result == expected_result
    mock_client.pdf_to_page_images.assert_called_once_with("/path/to/test.pdf")


def test_json_to_pptx_analyze_tool(mocker: "MockerFixture") -> None:
    """json_to_pptx_analyzeツールのテスト。"""
    expected_result = {"slides": 5, "estimated_time": 10}
    mock_client_analyze = mocker.patch(
        "middleman_ai.mcp.server.client.json_to_pptx_analyze_v2"
    )
    mock_client_analyze.return_value = expected_result
    json_data = {"pptx_template_id": "some_template_id"}

    result = json_to_pptx_analyze(json_data["pptx_template_id"])

    assert result == expected_result
    mock_client_analyze.assert_called_once_with(json_data["pptx_template_id"])


def test_json_to_pptx_execute_tool(mocker: "MockerFixture") -> None:
    """json_to_pptx_executeツールのテスト。"""
    expected_result = "https://example.com/generated.pptx"
    mock_execute = mocker.patch(
        "middleman_ai.mcp.server.client.json_to_pptx_execute_v2"
    )
    mock_execute.return_value = expected_result
    json_data = {"slides": [{"type": "title_slide", "title": "Test"}]}
    template_id = "template1"

    result = json_to_pptx_execute(template_id, json_data["slides"])

    assert result == expected_result
    # expected_arg の定義を複数行に分割
    expected_arg = Presentation(slides=[Slide(type="title_slide", placeholders=[])])
    mock_execute.assert_called_once_with(template_id, expected_arg)


def test_run_server(mocker: "MockerFixture") -> None:
    """run_serverのテスト。"""
    mock_mcp = mocker.patch("middleman_ai.mcp.server.mcp")

    run_server()

    mock_mcp.run.assert_called_once_with(transport="stdio")

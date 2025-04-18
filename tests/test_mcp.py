"""MCPサーバーのテストモジュール。"""

from typing import TYPE_CHECKING

from mcp.server.fastmcp import FastMCP

from middleman_ai.mcp.server import mcp, md_to_docx, md_to_pdf, md_to_pptx, pdf_to_page_images, pptx_to_page_images, docx_to_page_images, json_to_pptx_analyze, json_to_pptx_execute, run_server

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
    mock_client.md_to_pdf.assert_called_once_with("# Test")


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


def test_run_server(mocker: "MockerFixture") -> None:
    """run_serverのテスト。"""
    mock_mcp = mocker.patch("middleman_ai.mcp.server.mcp")

    run_server()

    mock_mcp.run.assert_called_once_with(transport="stdio")

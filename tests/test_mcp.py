"""MCPサーバーのテストモジュール。"""

from typing import TYPE_CHECKING

from mcp.server.fastmcp import FastMCP

from middleman_ai.mcp.server import mcp, md_to_docx, md_to_pdf, run_server

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


def test_run_server(mocker: "MockerFixture") -> None:
    """run_serverのテスト。"""
    mock_mcp = mocker.patch("middleman_ai.mcp.server.mcp")

    run_server()

    mock_mcp.run.assert_called_once_with(transport="stdio")
    mock_mcp.run.assert_called_once_with(transport="stdio")

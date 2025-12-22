"""MCPサーバーのテストモジュール。"""

from typing import TYPE_CHECKING

import pytest
from mcp.server.fastmcp import FastMCP

from middleman_ai.client import Presentation, Slide
from middleman_ai.mcp.server import (
    docx_to_page_images,
    json_to_pptx_analyze,
    json_to_pptx_execute,
    mcp,
    md_file_to_docx,
    md_file_to_pdf,
    md_to_docx,
    md_to_pdf,
    mermaid_file_to_image,
    mermaid_to_image,
    pdf_to_page_images,
    pptx_to_page_images,
    run_server,
    xlsx_to_page_images,
    xlsx_to_pdf_analyze,
    xlsx_to_pdf_execute,
)

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


def test_mcp_instance() -> None:
    """MCPサーバーインスタンスのテスト。"""
    assert isinstance(mcp, FastMCP)
    assert mcp.name == "Middleman Tools"


@pytest.mark.parametrize(
    "template_id",
    [
        None,
        "123e4567-e89b-12d3-a456-426614174000",
    ],
)
def test_md_to_pdf_tool_mcp(mocker: "MockerFixture", template_id: str | None) -> None:
    """md_to_pdfツールのテスト。"""
    mock_client = mocker.patch("middleman_ai.mcp.server.client")
    mock_client.md_to_pdf.return_value = "https://example.com/test.pdf"

    result = md_to_pdf("# Test", pdf_template_id=template_id)

    assert result == "https://example.com/test.pdf"
    mock_client.md_to_pdf.assert_called_once_with("# Test", pdf_template_id=template_id)


@pytest.mark.parametrize(
    "template_id",
    [
        None,
        "123e4567-e89b-12d3-a456-426614174000",
    ],
)
def test_md_file_to_pdf_tool_mcp(
    mocker: "MockerFixture",
    template_id: str | None,
) -> None:
    """md_file_to_pdfツールのテスト。"""
    mock_client = mocker.patch("middleman_ai.mcp.server.client")
    mock_path = mocker.patch("middleman_ai.mcp.server.Path")
    mock_os_access = mocker.patch("middleman_ai.mcp.server.os.access")
    # mock_open を変数に束縛せず、Pathオブジェクトのopenメソッドのモックを設定
    mock_file_handle = mocker.MagicMock()
    mock_file_handle.read.return_value = "# Test MD"
    mock_path.return_value.open.return_value.__enter__.return_value = mock_file_handle

    mock_path.return_value.exists.return_value = True
    mock_path.return_value.is_file.return_value = True
    mock_client.md_to_pdf.return_value = "https://example.com/test_file.pdf"

    file_path = "/fake/path/to/test.md"
    result = md_file_to_pdf(file_path, pdf_template_id=template_id)

    assert result == "https://example.com/test_file.pdf"
    mock_path.assert_called_once_with(file_path)
    mock_path.return_value.open.assert_called_once_with("r")
    mock_client.md_to_pdf.assert_called_once_with(
        "# Test MD",
        pdf_template_id=template_id,
    )
    mock_os_access.assert_called_once_with(mock_path.return_value, mocker.ANY)


@pytest.mark.parametrize(
    "template_id",
    [
        None,
        "123e4567-e89b-12d3-a456-426614174000",
    ],
)
def test_md_to_docx_tool_mcp(mocker: "MockerFixture", template_id: str | None) -> None:
    """md_to_docxツールのテスト。"""
    mock_client = mocker.patch("middleman_ai.mcp.server.client")
    mock_client.md_to_docx.return_value = "https://example.com/test.docx"

    result = md_to_docx("# Test", docx_template_id=template_id)

    assert result == "https://example.com/test.docx"
    mock_client.md_to_docx.assert_called_once_with(
        "# Test",
        docx_template_id=template_id,
    )


@pytest.mark.parametrize(
    "template_id",
    [
        None,
        "123e4567-e89b-12d3-a456-426614174000",
    ],
)
def test_md_file_to_docx_tool_mcp(
    mocker: "MockerFixture",
    template_id: str | None,
) -> None:
    """md_file_to_docxツールのテスト。"""
    mock_client = mocker.patch("middleman_ai.mcp.server.client")
    mock_path = mocker.patch("middleman_ai.mcp.server.Path")
    mock_os_access = mocker.patch("middleman_ai.mcp.server.os.access")
    # mock_open を変数に束縛せず、Pathオブジェクトのopenメソッドのモックを設定
    mock_file_handle = mocker.MagicMock()
    mock_file_handle.read.return_value = "# Test MD"
    mock_path.return_value.open.return_value.__enter__.return_value = mock_file_handle

    mock_path.return_value.exists.return_value = True
    mock_path.return_value.is_file.return_value = True
    mock_client.md_to_docx.return_value = "https://example.com/test_file.docx"

    file_path = "/fake/path/to/test.md"
    result = md_file_to_docx(file_path, docx_template_id=template_id)

    assert result == "https://example.com/test_file.docx"
    mock_path.assert_called_once_with(file_path)
    mock_path.return_value.open.assert_called_once_with("r")
    mock_client.md_to_docx.assert_called_once_with(
        "# Test MD",
        docx_template_id=template_id,
    )
    mock_os_access.assert_called_once_with(mock_path.return_value, mocker.ANY)


def test_pptx_to_page_images_tool_mcp(mocker: "MockerFixture") -> None:
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


def test_docx_to_page_images_tool_mcp(mocker: "MockerFixture") -> None:
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


def test_xlsx_to_page_images_tool_mcp(mocker: "MockerFixture") -> None:
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


def test_pdf_to_page_images_tool_mcp(mocker: "MockerFixture") -> None:
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


def test_json_to_pptx_analyze_tool_mcp(mocker: "MockerFixture") -> None:
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


def test_json_to_pptx_execute_tool_mcp(mocker: "MockerFixture") -> None:
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


def test_mermaid_to_image_tool_mcp(mocker: "MockerFixture") -> None:
    """mermaid_to_imageツールのテスト。"""
    mock_client = mocker.patch("middleman_ai.mcp.server.client")
    mock_client.mermaid_to_image.return_value = "https://example.com/mermaid.png"

    result = mermaid_to_image("graph TD; A-->B")

    assert result == "https://example.com/mermaid.png"
    mock_client.mermaid_to_image.assert_called_once_with(
        "graph TD; A-->B", options=None
    )


def test_mermaid_file_to_image_tool_mcp(mocker: "MockerFixture") -> None:
    """mermaid_file_to_imageツールのテスト。"""
    from pathlib import Path

    mock_client = mocker.patch("middleman_ai.mcp.server.client")
    mock_client.mermaid_to_image.return_value = "https://example.com/mermaid_file.png"

    # 実際のテストファイルを使用
    test_file = Path(__file__).parent / "data" / "test.mmd"
    result = mermaid_file_to_image(str(test_file))

    assert result == "https://example.com/mermaid_file.png"
    # 実際のファイル内容がクライアントに渡されることを確認
    call_args = mock_client.mermaid_to_image.call_args
    assert "graph TD" in call_args[0][0]  # Mermaidファイルの内容
    assert call_args[1]["options"] is None


def test_xlsx_to_pdf_analyze_tool_mcp(mocker: "MockerFixture") -> None:
    """xlsx_to_pdf_analyzeツールのテスト。"""
    from unittest.mock import MagicMock

    mock_client = mocker.patch("middleman_ai.mcp.server.client")
    mock_result = MagicMock()
    mock_result.sheet_name = "Sheet1"
    mock_placeholder = MagicMock()
    mock_placeholder.model_dump.return_value = {
        "key": "name",
        "description": "名前",
        "cell": "A1",
        "sheet_name": "Sheet1",
        "number_format": None,
    }
    mock_result.placeholders = [mock_placeholder]
    mock_result.placeholders_json_schema = '{"type": "object"}'
    mock_client.xlsx_to_pdf_analyze.return_value = mock_result

    result = xlsx_to_pdf_analyze("00000000-0000-0000-0000-000000000001")

    assert result["sheet_name"] == "Sheet1"
    assert len(result["placeholders"]) == 1
    assert result["placeholders"][0]["key"] == "name"
    mock_client.xlsx_to_pdf_analyze.assert_called_once_with(
        "00000000-0000-0000-0000-000000000001", sheet_name=None
    )


def test_xlsx_to_pdf_execute_tool_mcp(mocker: "MockerFixture") -> None:
    """xlsx_to_pdf_executeツールのテスト。"""
    from unittest.mock import MagicMock

    mock_client = mocker.patch("middleman_ai.mcp.server.client")
    mock_result = MagicMock()
    mock_result.pdf_url = "https://example.com/output.pdf"
    mock_result.warnings = []
    mock_client.xlsx_to_pdf_execute.return_value = mock_result

    result = xlsx_to_pdf_execute(
        "00000000-0000-0000-0000-000000000001",
        {"name": "テスト"},
    )

    assert result["pdf_url"] == "https://example.com/output.pdf"
    assert result["warnings"] == []
    mock_client.xlsx_to_pdf_execute.assert_called_once_with(
        "00000000-0000-0000-0000-000000000001",
        {"name": "テスト"},
        sheet_name=None,
    )


def test_run_server_mcp(mocker: "MockerFixture") -> None:
    """run_serverのテスト。"""
    mock_mcp = mocker.patch("middleman_ai.mcp.server.mcp")

    run_server()

    mock_mcp.run.assert_called_once_with(transport="stdio")

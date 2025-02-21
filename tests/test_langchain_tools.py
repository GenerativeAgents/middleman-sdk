"""LangChainツール群のテストモジュール。"""

from typing import TYPE_CHECKING

import pytest

from middleman_ai.client import Presentation, ToolsClient
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


def test_json_to_pptx_analyze_tool_without_default_template_id(
    client: ToolsClient, mocker: "MockerFixture"
) -> None:
    """JsonToPptxAnalyzeToolのテスト。"""
    template_structure = [
        {
            "type": "Title Slide",
            "description": "Description1",
            "placeholders": [
                {
                    "name": "title",
                    "description": "スライドのタイトル",
                },
                {
                    "name": "subtitle",
                    "description": "スライドのサブタイトル",
                },
            ],
        },
        {
            "type": "Content Slide",
            "description": "Description2",
            "placeholders": [
                {
                    "name": "title",
                    "description": "スライドのタイトル",
                },
                {
                    "name": "content",
                    "description": "スライドの内容",
                },
            ],
        },
    ]
    mock_analyze = mocker.patch.object(
        client,
        "json_to_pptx_analyze_v2",
        return_value=template_structure,
    )

    tool = JsonToPptxAnalyzeTool(client=client)

    # テンプレートIDが指定されていない場合はエラー
    with pytest.raises(ValueError, match="テンプレートIDが指定されていません"):
        tool._run(None)

    # テンプレートIDが指定された場合は成功
    result = tool._run("template-123")
    assert isinstance(result, str)
    assert "Title Slide" in result
    assert "Content Slide" in result
    assert "Description1" in result
    assert "Description2" in result
    assert "title" in result
    assert "subtitle" in result
    assert "content" in result
    assert "スライドのタイトル" in result
    assert "スライドのサブタイトル" in result
    assert "スライドの内容" in result
    mock_analyze.assert_called_once_with("template-123")


def test_json_to_pptx_analyze_tool_with_default_template_id(
    client: ToolsClient, mocker: "MockerFixture"
) -> None:
    """JsonToPptxAnalyzeToolのテスト。"""
    template_structure = [
        {
            "type": "Title Slide",
            "description": "Description1",
            "placeholders": [
                {
                    "name": "title",
                    "description": "スライドのタイトル",
                },
                {
                    "name": "subtitle",
                    "description": "スライドのサブタイトル",
                },
            ],
        },
        {
            "type": "Content Slide",
            "description": "Description2",
            "placeholders": [
                {
                    "name": "title",
                    "description": "スライドのタイトル",
                },
                {
                    "name": "content",
                    "description": "スライドの内容",
                },
            ],
        },
    ]
    mock_analyze = mocker.patch.object(
        client,
        "json_to_pptx_analyze_v2",
        return_value=template_structure,
    )

    tool = JsonToPptxAnalyzeTool(client=client, default_template_id="template-123")
    result = tool._run()

    assert isinstance(result, str)
    assert "Title Slide" in result
    assert "Content Slide" in result
    assert "Description1" in result
    assert "Description2" in result
    assert "title" in result
    assert "subtitle" in result
    assert "content" in result
    assert "スライドのタイトル" in result
    assert "スライドのサブタイトル" in result
    assert "スライドの内容" in result
    mock_analyze.assert_called_once_with("template-123")


def test_json_to_pptx_analyze_tool_with_both_template_id_and_default_template_id(
    client: ToolsClient, mocker: "MockerFixture"
) -> None:
    """JsonToPptxAnalyzeToolのテスト。"""
    template_structure = [
        {
            "type": "Title Slide",
            "description": "Description1",
            "placeholders": [
                {
                    "name": "title",
                    "description": "スライドのタイトル",
                },
                {
                    "name": "subtitle",
                    "description": "スライドのサブタイトル",
                },
            ],
        },
        {
            "type": "Content Slide",
            "description": "Description2",
            "placeholders": [
                {
                    "name": "title",
                    "description": "スライドのタイトル",
                },
                {
                    "name": "content",
                    "description": "スライドの内容",
                },
            ],
        },
    ]
    mock_analyze = mocker.patch.object(
        client,
        "json_to_pptx_analyze_v2",
        return_value=template_structure,
    )

    tool = JsonToPptxAnalyzeTool(client=client, default_template_id="template-123")
    result = tool._run(template_id="template-456")

    assert isinstance(result, str)
    assert "Title Slide" in result
    assert "Content Slide" in result
    assert "Description1" in result
    assert "Description2" in result
    assert "title" in result
    assert "subtitle" in result
    assert "content" in result
    assert "スライドのタイトル" in result
    assert "スライドのサブタイトル" in result
    assert "スライドの内容" in result
    mock_analyze.assert_called_once_with("template-456")


def test_json_to_pptx_execute_tool_without_default_template_id(
    client: ToolsClient, mocker: "MockerFixture"
) -> None:
    """JsonToPptxExecuteToolのテスト。"""
    template_id = "template-123"
    presentation_data = {
        "slides": [
            {
                "type": "Title Slide",
                "placeholders": [
                    {"name": "title", "content": "My Title"},
                    {"name": "subtitle", "content": "My Subtitle"},
                ],
            },
            {
                "type": "Content Slide",
                "placeholders": [
                    {"name": "title", "content": "My Title"},
                    {"name": "content", "content": "Some content"},
                ],
            },
        ],
    }
    mock_execute = mocker.patch.object(
        client,
        "json_to_pptx_execute_v2",
        return_value="https://example.com/result.pptx",
    )

    tool = JsonToPptxExecuteTool(client=client)

    # テンプレートIDが指定されていない場合はエラー
    with pytest.raises(ValueError, match="テンプレートIDが指定されていません"):
        tool._run(
            presentation=Presentation.model_validate(
                presentation_data,
            ).model_dump_json(),
        )

    # テンプレートIDが指定された場合は成功
    result = tool._run(
        presentation=Presentation.model_validate(
            presentation_data,
        ).model_dump_json(),
        template_id=template_id,
    )
    assert result == "https://example.com/result.pptx"
    mock_execute.assert_called_once_with(
        template_id,
        Presentation.model_validate(
            presentation_data,
        ),
    )


def test_json_to_pptx_execute_tool_with_default_template_id(
    client: ToolsClient, mocker: "MockerFixture"
) -> None:
    """JsonToPptxExecuteToolのテスト。"""
    template_id = "template-123"
    presentation_data = {
        "slides": [
            {
                "type": "Title Slide",
                "placeholders": [
                    {"name": "title", "content": "My Title"},
                    {"name": "subtitle", "content": "My Subtitle"},
                ],
            },
            {
                "type": "Content Slide",
                "placeholders": [
                    {"name": "title", "content": "My Title"},
                    {"name": "content", "content": "Some content"},
                ],
            },
        ],
    }
    mock_execute = mocker.patch.object(
        client,
        "json_to_pptx_execute_v2",
        return_value="https://example.com/result.pptx",
    )

    tool = JsonToPptxExecuteTool(client=client, default_template_id=template_id)
    result = tool._run(
        presentation=Presentation.model_validate(
            presentation_data,
        ).model_dump_json(),
    )

    assert result == "https://example.com/result.pptx"
    mock_execute.assert_called_once_with(
        template_id,
        Presentation.model_validate(
            presentation_data,
        ),
    )


def test_json_to_pptx_execute_tool_with_both_template_id_and_default_template_id(
    client: ToolsClient, mocker: "MockerFixture"
) -> None:
    """JsonToPptxExecuteToolのテスト。"""
    presentation_data = {
        "slides": [
            {
                "type": "Title Slide",
                "placeholders": [
                    {"name": "title", "content": "My Title"},
                    {"name": "subtitle", "content": "My Subtitle"},
                ],
            },
            {
                "type": "Content Slide",
                "placeholders": [
                    {"name": "title", "content": "My Title"},
                    {"name": "content", "content": "Some content"},
                ],
            },
        ],
    }
    mock_execute = mocker.patch.object(
        client,
        "json_to_pptx_execute_v2",
        return_value="https://example.com/result.pptx",
    )

    tool = JsonToPptxExecuteTool(client=client, default_template_id="template-123")
    result = tool._run(
        presentation=Presentation.model_validate(
            presentation_data,
        ).model_dump_json(),
        template_id="template-456",
    )

    assert result == "https://example.com/result.pptx"
    mock_execute.assert_called_once_with(
        "template-456",
        Presentation.model_validate(
            presentation_data,
        ),
    )


def test_json_to_pptx_analyze_tool_template_id_error(
    client: ToolsClient, mocker: "MockerFixture"
) -> None:
    """JsonToPptxAnalyzeToolのテンプレートIDエラーのテスト。"""
    mock_analyze = mocker.patch.object(
        client,
        "json_to_pptx_analyze_v2",
        return_value=[],
    )

    # テンプレートIDが指定されていない場合
    tool = JsonToPptxAnalyzeTool(client=client)
    with pytest.raises(ValueError, match="テンプレートIDが指定されていません"):
        tool._run(None)

    mock_analyze.assert_not_called()


def test_json_to_pptx_execute_tool_template_id_error(
    client: ToolsClient, mocker: "MockerFixture"
) -> None:
    """JsonToPptxExecuteToolのテンプレートIDエラーのテスト。"""
    mock_execute = mocker.patch.object(
        client,
        "json_to_pptx_execute_v2",
        return_value="https://example.com/result.pptx",
    )

    # テンプレートIDが指定されていない場合
    tool = JsonToPptxExecuteTool(client=client)
    test_json = '{"slides": []}'
    with pytest.raises(ValueError, match="テンプレートIDが指定されていません"):
        tool._run(test_json)

    mock_execute.assert_not_called()


def test_json_to_pptx_execute_tool_json_error(
    client: ToolsClient, mocker: "MockerFixture"
) -> None:
    """JsonToPptxExecuteToolのJSON形式エラーのテスト。"""
    mock_execute = mocker.patch.object(
        client,
        "json_to_pptx_execute_v2",
        return_value="https://example.com/result.pptx",
    )

    tool = JsonToPptxExecuteTool(client=client)
    with pytest.raises(ValueError, match="不正なJSON形式です"):
        tool._run("invalid json", template_id="template-123")

    mock_execute.assert_not_called()

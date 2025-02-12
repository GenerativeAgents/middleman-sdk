"""LangChainツール群のテンプレートID関連のテストモジュール。"""

import os

import pytest

from middleman_ai.client import ToolsClient
from middleman_ai.langchain_tools.json_to_pptx import (
    JsonToPptxAnalyzeTool,
    JsonToPptxExecuteTool,
)


@pytest.fixture
def client() -> ToolsClient:
    """テスト用のToolsClientインスタンスを生成します。

    Returns:
        ToolsClient: テスト用のクライアントインスタンス
    """
    return ToolsClient(api_key=os.getenv("MIDDLEMAN_API_KEY") or "")


def test_json_to_pptx_analyze_tool_template_id(client: ToolsClient) -> None:
    """JsonToPptxAnalyzeToolのテンプレートID関連のテスト。"""
    tool = JsonToPptxAnalyzeTool(client=client)
    
    # テンプレートIDが指定されていない場合
    with pytest.raises(ValueError, match="テンプレートIDが指定されていません"):
        tool._run(None)
    
    # default_template_idが設定されている場合
    tool = JsonToPptxAnalyzeTool(
        client=client,
        default_template_id="0bb238bd-d03a-4f1a-be6f-fe2e0c6e91f7",
    )
    result = tool._run(None)
    assert isinstance(result, str)
    assert "Slide" in result

    # テンプレートIDが指定された場合（default_template_idより優先される）
    result = tool._run("0bb238bd-d03a-4f1a-be6f-fe2e0c6e91f7")
    assert isinstance(result, str)
    assert "Slide" in result


def test_json_to_pptx_execute_tool_template_id(client: ToolsClient) -> None:
    """JsonToPptxExecuteToolのテンプレートID関連のテスト。"""
    tool = JsonToPptxExecuteTool(client=client)
    test_json = '{"slides": []}'
    
    # テンプレートIDが指定されていない場合
    with pytest.raises(ValueError, match="テンプレートIDが指定されていません"):
        tool._run(test_json)
    
    # default_template_idが設定されている場合
    tool = JsonToPptxExecuteTool(
        client=client,
        default_template_id="0bb238bd-d03a-4f1a-be6f-fe2e0c6e91f7",
    )
    result = tool._run(test_json)
    assert isinstance(result, str)
    assert result.startswith("https://")

    # テンプレートIDが指定された場合（default_template_idより優先される）
    result = tool._run(test_json, template_id="0bb238bd-d03a-4f1a-be6f-fe2e0c6e91f7")
    assert isinstance(result, str)
    assert result.startswith("https://")

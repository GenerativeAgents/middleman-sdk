"""LangChainのJSON to PPTX変換ツール。"""

from typing import Any, Dict

from langchain_core.tools import BaseTool

from middleman_ai.client import ToolsClient


class JsonToPptxAnalyzeTool(BaseTool):
    """PPTXテンプレートを解析するLangChainツール。"""

    name: str = "json-to-pptx-analyze"
    description: str = (
        "PPTXテンプレートの構造を解析します。"
        "入力はテンプレートID（UUID）である必要があります。"
        "出力はテンプレートの構造情報です。"
    )

    def __init__(self, client: ToolsClient, **kwargs: Any) -> None:
        """ツールを初期化します。

        Args:
            client: Middleman.ai APIクライアント
            **kwargs: BaseTool用の追加引数
        """
        super().__init__(**kwargs)
        self.client = client

    def _run(self, template_id: str) -> Dict[str, Any]:
        """同期的にPPTXテンプレートを解析します。

        Args:
            template_id: テンプレートID（UUID）

        Returns:
            Dict[str, Any]: テンプレートの構造情報
        """
        return self.client.json_to_pptx_analyze_v2(template_id)

    async def _arun(self, template_id: str) -> Dict[str, Any]:
        """非同期的にPPTXテンプレートを解析します。

        Args:
            template_id: テンプレートID（UUID）

        Returns:
            Dict[str, Any]: テンプレートの構造情報
        """
        # 現時点では同期メソッドを呼び出し
        return self._run(template_id)


class JsonToPptxExecuteTool(BaseTool):
    """JSONからPPTXを生成するLangChainツール。"""

    name: str = "json-to-pptx-execute"
    description: str = (
        "テンプレートIDとプレゼンテーションJSONを指定し、PPTXを生成します。"
        "入力は「テンプレートID,JSON」の形式である必要があります（カンマ区切り）。"
        "出力は生成されたPPTXのURLです。"
    )

    def __init__(self, client: ToolsClient, **kwargs: Any) -> None:
        """ツールを初期化します。

        Args:
            client: Middleman.ai APIクライアント
            **kwargs: BaseTool用の追加引数
        """
        super().__init__(**kwargs)
        self.client = client

    def _run(self, input_str: str) -> str:
        """同期的にJSONからPPTXを生成します。

        Args:
            input_str: 「テンプレートID,JSON」形式の入力文字列

        Returns:
            str: 生成されたPPTXのURL

        Raises:
            ValueError: 入力形式が不正な場合
            json.JSONDecodeError: JSON形式が不正な場合
        """
        try:
            import json

            template_id, json_str = input_str.split(",", 1)
            presentation = json.loads(json_str)
            return self.client.json_to_pptx_execute_v2(template_id, presentation)
        except ValueError as e:
            raise ValueError(
                "入力は「テンプレートID,JSON」形式である必要があります"
            ) from e
        except json.JSONDecodeError as e:
            raise ValueError("不正なJSON形式です") from e

    async def _arun(self, input_str: str) -> str:
        """非同期的にJSONからPPTXを生成します。

        Args:
            input_str: 「テンプレートID,JSON」形式の入力文字列

        Returns:
            str: 生成されたPPTXのURL
        """
        # 現時点では同期メソッドを呼び出し
        return self._run(input_str)

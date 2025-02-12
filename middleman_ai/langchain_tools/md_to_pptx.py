"""LangChainのMarkdown to PPTX変換ツール。"""

from typing import Any

from langchain_core.tools import BaseTool
from pydantic import Field

from middleman_ai.client import ToolsClient


class MdToPptxTool(BaseTool):
    """Markdown文字列をPPTXに変換するLangChainツール。"""

    name: str = "md-to-pptx"
    description: str = (
        "Markdown文字列をPPTXに変換します。"
        "入力は有効なMarkdown文字列である必要があります。"
        "出力は生成されたPPTXのURLです。"
    )
    client: ToolsClient = Field(..., exclude=True)

    def __init__(self, client: ToolsClient, **kwargs: Any) -> None:
        """ツールを初期化します。

        Args:
            client: Middleman.ai APIクライアント
            **kwargs: BaseTool用の追加引数
        """
        kwargs["client"] = client
        super().__init__(**kwargs)

    def _run(self, text: str) -> str:
        """同期的にMarkdown文字列をPPTXに変換します。

        Args:
            text: 変換対象のMarkdown文字列

        Returns:
            str: 生成されたPPTXのURL
        """
        return self.client.md_to_pptx(text)

    async def _arun(self, text: str) -> str:
        """非同期的にMarkdown文字列をPPTXに変換します。

        Args:
            text: 変換対象のMarkdown文字列

        Returns:
            str: 生成されたPPTXのURL
        """
        # 現時点では同期メソッドを呼び出し
        return self._run(text)

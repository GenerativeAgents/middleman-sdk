"""LangChainのMarkdown to PDF変換ツール。"""

from typing import Any

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from middleman_ai.client import ToolsClient


class MdToPdfInput(BaseModel):
    """Markdown to PDF変換用の入力スキーマ。"""

    text: str = Field(
        ...,
        description="変換対象のMarkdown文字列。有効なMarkdown形式である必要があります。",
    )


class MdToPdfTool(BaseTool):
    """Markdown文字列をPDFに変換するLangChainツール。"""

    name: str = "md-to-pdf"
    description: str = (
        "Markdown文字列をPDFに変換します。"
        "入力は有効なMarkdown文字列である必要があります。"
        "出力は生成されたPDFのURLです。"
    )
    args_schema: type[BaseModel] = MdToPdfInput
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
        """同期的にMarkdown文字列をPDFに変換します。

        Args:
            text: 変換対象のMarkdown文字列

        Returns:
            str: 生成されたPDFのURL
        """
        return self.client.md_to_pdf(text)

    async def _arun(self, text: str) -> str:
        """非同期的にMarkdown文字列をPDFに変換します。

        Args:
            text: 変換対象のMarkdown文字列

        Returns:
            str: 生成されたPDFのURL
        """
        # 現時点では同期メソッドを呼び出し
        return self._run(text)

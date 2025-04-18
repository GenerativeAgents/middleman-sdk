"""LangChainのDOCX to Page Images変換ツール。"""

from typing import Any

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from middleman_ai.client import ToolsClient


class DocxToPageImagesInput(BaseModel):
    """DOCX to Page Images変換用の入力スキーマ。"""

    docx_file_path: str = Field(
        ...,
        description="変換対象のDOCXファイルパス。ローカルに存在する有効なDOCXファイルを指定する必要があります。",
    )


class DocxToPageImagesTool(BaseTool):
    """DOCXをページごとの画像に変換するLangChainツール。"""

    name: str = "docx-to-page-images"
    description: str = (
        "DOCXファイルをページごとの画像に変換します。"
        "入力はローカルのDOCXファイルパスである必要があります。"
        "出力は各ページの画像URLのリストを文字列化したものです。"
    )
    args_schema: type[BaseModel] = DocxToPageImagesInput
    client: ToolsClient = Field(..., exclude=True)

    def __init__(self, client: ToolsClient, **kwargs: Any) -> None:
        """ツールを初期化します。

        Args:
            client: Middleman.ai APIクライアント
            **kwargs: BaseTool用の追加引数
        """
        kwargs["client"] = client
        super().__init__(**kwargs)

    def _run(self, docx_file_path: str) -> str:
        """同期的にDOCXをページごとの画像に変換します。

        Args:
            docx_file_path: 変換対象のDOCXファイルパス

        Returns:
            str: 各ページの画像URLのリストを文字列化したもの
        """
        result = self.client.docx_to_page_images(docx_file_path)
        return "\n".join(
            f"Page {page['page_no']}: {page['image_url']}" for page in result
        )

    async def _arun(self, docx_file_path: str) -> str:
        """非同期的にDOCXをページごとの画像に変換します。

        Args:
            docx_file_path: 変換対象のDOCXファイルパス

        Returns:
            str: 各ページの画像URLのリストを文字列化したもの
        """
        return self._run(docx_file_path)

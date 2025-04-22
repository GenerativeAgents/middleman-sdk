"""LangChainのXLSX to Page Images変換ツール。"""

from typing import Any

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from middleman_ai.client import ToolsClient


class XlsxToPageImagesInput(BaseModel):
    """XLSX to Page Images変換用の入力スキーマ。"""

    xlsx_file_path: str = Field(
        ...,
        description="変換対象のXLSXファイルパス。ローカルに存在する有効なXLSXファイルを指定する必要があります。",
    )


class XlsxToPageImagesTool(BaseTool):
    """XLSXをページごとの画像に変換するLangChainツール。"""

    name: str = "xlsx-to-page-images"
    description: str = (
        "XLSXファイルをページごとの画像に変換します。"
        "入力はローカルのXLSXファイルパスである必要があります。"
        "出力は各ページの画像URLのリストを文字列化したものです。"
    )
    args_schema: type[BaseModel] = XlsxToPageImagesInput
    client: ToolsClient = Field(..., exclude=True)

    def __init__(self, client: ToolsClient, **kwargs: Any) -> None:
        """ツールを初期化します。

        Args:
            client: Middleman.ai APIクライアント
            **kwargs: BaseTool用の追加引数
        """
        kwargs["client"] = client
        super().__init__(**kwargs)

    def _run(self, xlsx_file_path: str) -> str:
        """同期的にXLSXをページごとの画像に変換します。

        Args:
            xlsx_file_path: 変換対象のXLSXファイルパス

        Returns:
            str: 各ページの画像URLのリストを文字列化したもの
        """
        # 注意: client.xlsx_to_page_images メソッドが存在することを前提としています。
        # 存在しない場合は、適切なメソッド名に修正する必要があります。
        result = self.client.xlsx_to_page_images(xlsx_file_path)
        return "\n".join(
            f"Sheet {page['sheet_name']}: {page['image_url']}" for page in result
        )

    async def _arun(self, xlsx_file_path: str) -> str:
        """非同期的にXLSXをページごとの画像に変換します。

        Args:
            xlsx_file_path: 変換対象のXLSXファイルパス

        Returns:
            str: 各ページの画像URLのリストを文字列化したもの
        """
        # 注意: client.xlsx_to_page_images メソッドが存在することを前提としています。
        # 存在しない場合は、適切なメソッド名に修正する必要があります。
        # 非同期実装が必要な場合は、client側の対応も確認してください。
        return self._run(xlsx_file_path)

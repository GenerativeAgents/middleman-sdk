"""LangChainのPDF to Page Images変換ツール。"""

from typing import Any

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from middleman_ai.client import ToolsClient


class PdfToPageImagesInput(BaseModel):
    """PDF to Page Images変換用の入力スキーマ。"""

    pdf_file_path: str = Field(
        ...,
        description="変換対象のPDFファイルパス。ローカルに存在する有効なPDFファイルを指定する必要があります。",
    )


class PdfToPageImagesTool(BaseTool):
    """PDFをページごとの画像に変換するLangChainツール。"""

    name: str = "pdf-to-page-images"
    description: str = (
        "PDFファイルをページごとの画像に変換します。"
        "入力はローカルのPDFファイルパスである必要があります。"
        "出力は各ページの画像URLのリストを文字列化したものです。"
    )
    args_schema: type[BaseModel] = PdfToPageImagesInput
    client: ToolsClient = Field(..., exclude=True)

    def __init__(self, client: ToolsClient, **kwargs: Any) -> None:
        """ツールを初期化します。

        Args:
            client: Middleman.ai APIクライアント
            **kwargs: BaseTool用の追加引数
        """
        kwargs["client"] = client
        super().__init__(**kwargs)

    def _run(self, pdf_file_path: str) -> str:
        """同期的にPDFをページごとの画像に変換します。

        Args:
            pdf_file_path: 変換対象のPDFファイルパス

        Returns:
            str: 各ページの画像URLのリストを文字列化したもの
        """
        result = self.client.pdf_to_page_images(pdf_file_path)
        return "\n".join(
            f"Page {page['page_no']}: {page['image_url']}" for page in result
        )

    async def _arun(self, pdf_file_path: str) -> str:
        """非同期的にPDFをページごとの画像に変換します。

        Args:
            pdf_file_path: 変換対象のPDFファイルパス

        Returns:
            str: 各ページの画像URLのリストを文字列化したもの
        """
        # 現時点では同期メソッドを呼び出し
        return self._run(pdf_file_path)

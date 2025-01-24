"""LangChainのPDF to Page Images変換ツール。"""

from typing import Any, Dict, List

from langchain_core.tools import BaseTool

from middleman_ai.client import ToolsClient


class PdfToPageImagesTool(BaseTool):
    """PDFをページごとの画像に変換するLangChainツール。"""

    name: str = "pdf-to-page-images"
    description: str = (
        "PDFファイルをページごとの画像に変換します。"
        "入力はローカルのPDFファイルパスである必要があります。"
        "出力は各ページの画像URLのリストです。"
    )

    def __init__(self, client: ToolsClient, **kwargs: Any) -> None:
        """ツールを初期化します。

        Args:
            client: Middleman.ai APIクライアント
            **kwargs: BaseTool用の追加引数
        """
        super().__init__(**kwargs)
        self.client = client

    def _run(self, pdf_file_path: str) -> List[Dict[str, Any]]:
        """同期的にPDFをページごとの画像に変換します。

        Args:
            pdf_file_path: 変換対象のPDFファイルパス

        Returns:
            List[Dict[str, Any]]: [{"page_no": int, "image_url": str}, ...]
        """
        return self.client.pdf_to_page_images(pdf_file_path)

    async def _arun(self, pdf_file_path: str) -> List[Dict[str, Any]]:
        """非同期的にPDFをページごとの画像に変換します。

        Args:
            pdf_file_path: 変換対象のPDFファイルパス

        Returns:
            List[Dict[str, Any]]: [{"page_no": int, "image_url": str}, ...]
        """
        # 現時点では同期メソッドを呼び出し
        return self._run(pdf_file_path)

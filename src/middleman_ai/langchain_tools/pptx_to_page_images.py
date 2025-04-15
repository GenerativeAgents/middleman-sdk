"""LangChainのPPTX to Page Images変換ツール。"""

from typing import Any

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from middleman_ai.client import ToolsClient


class PptxToPageImagesInput(BaseModel):
    """PPTX to Page Images変換用の入力スキーマ。"""

    pptx_file_path: str = Field(
        ...,
        description="変換対象のPPTXファイルパス。ローカルに存在する有効なPPTXファイルを指定する必要があります。",
    )


class PptxToPageImagesTool(BaseTool):
    """PPTXをスライドごとの画像に変換するLangChainツール。"""

    name: str = "pptx-to-page-images"
    description: str = (
        "PPTXファイルをスライドごとの画像に変換します。"
        "入力はローカルのPPTXファイルパスである必要があります。"
        "出力は各スライドの画像URLのリストを文字列化したものです。"
    )
    args_schema: type[BaseModel] = PptxToPageImagesInput
    client: ToolsClient = Field(..., exclude=True)

    def __init__(self, client: ToolsClient, **kwargs: Any) -> None:
        """ツールを初期化します。

        Args:
            client: Middleman.ai APIクライアント
            **kwargs: BaseTool用の追加引数
        """
        kwargs["client"] = client
        super().__init__(**kwargs)

    def _run(self, pptx_file_path: str) -> str:
        """同期的にPPTXをスライドごとの画像に変換します。

        Args:
            pptx_file_path: 変換対象のPPTXファイルパス

        Returns:
            str: 各スライドの画像URLのリストを文字列化したもの
        """
        result = self.client.pptx_to_page_images(pptx_file_path)
        return "\n".join(
            f"Slide {page['page_no']}: {page['image_url']}" for page in result
        )

    async def _arun(self, pptx_file_path: str) -> str:
        """非同期的にPPTXをスライドごとの画像に変換します。

        Args:
            pptx_file_path: 変換対象のPPTXファイルパス

        Returns:
            str: 各スライドの画像URLのリストを文字列化したもの
        """
        # 現時点では同期メソッドを呼び出し
        return self._run(pptx_file_path)

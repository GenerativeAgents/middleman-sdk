"""Middleman.ai SDKのデータモデルを定義するモジュール。"""

from typing import List, Optional

from pydantic import BaseModel, Field


class MdToPdfResponse(BaseModel):
    """Markdown → PDF変換のレスポンスモデル。"""

    pdf_url: str = Field(..., description="生成されたPDFのダウンロードURL")
    important_remark_for_user: Optional[str] = Field(
        None, description="ユーザーへの重要な注意事項"
    )


class MdToDocxResponse(BaseModel):
    """Markdown → DOCX変換のレスポンスモデル。"""

    docx_url: str = Field(..., description="生成されたDOCXのダウンロードURL")
    important_remark_for_user: Optional[str] = Field(
        None, description="ユーザーへの重要な注意事項"
    )


class MdToPptxResponse(BaseModel):
    """Markdown → PPTX変換のレスポンスモデル。"""

    pptx_url: str = Field(..., description="生成されたPPTXのダウンロードURL")
    important_remark_for_user: Optional[str] = Field(
        None, description="ユーザーへの重要な注意事項"
    )


class PageImage(BaseModel):
    """PDFの1ページ分の画像情報。"""

    page_no: int = Field(..., description="ページ番号")
    image_url: str = Field(..., description="画像のダウンロードURL")


class PdfToPageImagesResponse(BaseModel):
    """PDF → ページ画像変換のレスポンスモデル。"""

    pages: List[PageImage] = Field(..., description="各ページの画像情報")
    important_remark_for_user: Optional[str] = Field(
        None, description="ユーザーへの重要な注意事項"
    )


class JsonToPptxAnalyzeResponse(BaseModel):
    """PPTX テンプレート解析のレスポンスモデル。"""

    slides: List[dict] = Field(..., description="テンプレートの構造情報")
    important_remark_for_user: Optional[str] = Field(
        None, description="ユーザーへの重要な注意事項"
    )


class JsonToPptxExecuteResponse(BaseModel):
    """JSON → PPTX変換実行のレスポンスモデル。"""

    pptx_url: str = Field(..., description="生成されたPPTXのダウンロードURL")
    important_remark_for_user: Optional[str] = Field(
        None, description="ユーザーへの重要な注意事項"
    )

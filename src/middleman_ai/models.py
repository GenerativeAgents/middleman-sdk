"""Middleman.ai SDKのデータモデルを定義するモジュール。"""

from typing import List, Literal

from pydantic import BaseModel, Field


class MdToPdfResponse(BaseModel):
    """Markdown → PDF変換のレスポンスモデル。"""

    pdf_url: str = Field(..., description="生成されたPDFのダウンロードURL")
    important_remark_for_user: str | None = Field(
        None, description="ユーザーへの重要な注意事項"
    )


class MdToDocxResponse(BaseModel):
    """Markdown → DOCX変換のレスポンスモデル。"""

    docx_url: str = Field(..., description="生成されたDOCXのダウンロードURL")
    important_remark_for_user: str | None = Field(
        None, description="ユーザーへの重要な注意事項"
    )


class PageImage(BaseModel):
    """PDFの1ページ分の画像情報。"""

    page_no: int = Field(..., description="ページ番号")
    image_url: str = Field(..., description="画像のダウンロードURL")


class PdfToPageImagesResponse(BaseModel):
    """PDF → ページ画像変換のレスポンスモデル。"""

    pages: List[PageImage] = Field(..., description="各ページの画像情報")
    important_remark_for_user: str | None = Field(
        None, description="ユーザーへの重要な注意事項"
    )


class JsonToPptxAnalyzeResponse(BaseModel):
    """PPTX テンプレート解析のレスポンスモデル。"""

    slides: List[dict] = Field(..., description="テンプレートの構造情報")
    important_remark_for_user: str | None = Field(
        None, description="ユーザーへの重要な注意事項"
    )


class JsonToPptxExecuteResponse(BaseModel):
    """JSON → PPTX変換実行のレスポンスモデル。"""

    pptx_url: str = Field(..., description="生成されたPPTXのダウンロードURL")
    important_remark_for_user: str | None = Field(
        None, description="ユーザーへの重要な注意事項"
    )


class PptxToPageImagesResponse(BaseModel):
    """PPTX → ページ画像変換のレスポンスモデル。"""

    pages: List[PageImage] = Field(..., description="各スライドの画像情報")
    important_remark_for_user: str | None = Field(
        None, description="ユーザーへの重要な注意事項"
    )


class DocxToPageImagesResponse(BaseModel):
    """DOCX → ページ画像変換のレスポンスモデル。"""

    pages: List[PageImage] = Field(..., description="各ページの画像情報")
    important_remark_for_user: str | None = Field(
        None, description="ユーザーへの重要な注意事項"
    )


class XlsxPageImage(BaseModel):
    """XLSXの1シート分の画像情報。"""

    sheet_name: str = Field(..., description="シート名")
    image_url: str = Field(..., description="画像のダウンロードURL")


class XlsxToPageImagesResponse(BaseModel):
    """XLSX → ページ画像変換のレスポンスモデル。"""

    pages: List[XlsxPageImage] = Field(..., description="各シートの画像情報")
    important_remark_for_user: str | None = Field(
        None, description="ユーザーへの重要な注意事項"
    )


class CustomSize(BaseModel):
    """Mermaid画像のカスタムサイズ設定。"""

    width: int = Field(
        ...,
        ge=100,
        le=1200,
        description="画像幅（100-1200ピクセル）",
    )
    height: int = Field(
        ...,
        ge=100,
        le=1200,
        description="画像高さ（100-1200ピクセル）",
    )


class MermaidToImageOptions(BaseModel):
    """Mermaid → 画像変換のオプション設定。"""

    theme: Literal["default", "dark", "forest", "neutral"] | None = Field(
        default=None, description="Mermaidテーマ"
    )
    background_color: str | None = Field(
        default=None, description="背景色（透明またはRGBカラー）"
    )
    custom_size: CustomSize | None = Field(
        default=None, description="カスタムサイズ設定"
    )


class MermaidToImageResponse(BaseModel):
    """Mermaid → 画像変換のレスポンスモデル。"""

    image_url: str = Field(..., description="生成された画像のダウンロードURL")
    format: str = Field(..., description="出力フォーマット（例: png）")
    important_remark_for_user: str | None = Field(
        None, description="ユーザーへの重要な注意事項"
    )


class XlsxPlaceholder(BaseModel):
    """Excelプレースホルダー情報。"""

    key: str = Field(..., description="プレースホルダーのキー")
    description: str = Field(..., description="プレースホルダーの説明")
    cell: str = Field(..., description="セル位置（例: A1, E3）")
    sheet_name: str = Field(..., description="シート名")
    number_format: str | None = Field(None, description="セルの数値フォーマット")


class XlsxToPdfAnalyzeResponse(BaseModel):
    """XLSX → PDF テンプレート解析のレスポンスモデル。"""

    sheet_name: str = Field(..., description="解析対象のシート名")
    placeholders: List[XlsxPlaceholder] = Field(
        ..., description="プレースホルダー一覧"
    )
    placeholders_json_schema: str = Field(
        ..., description="placeholdersオブジェクトのJSON Schema（AI用）"
    )
    important_remark_for_user: str | None = Field(
        None, description="ユーザーへの重要な注意事項"
    )


class XlsxToPdfExecuteResponse(BaseModel):
    """XLSX → PDF 変換実行のレスポンスモデル。"""

    pdf_url: str = Field(..., description="生成されたPDFのダウンロードURL")
    warnings: List[str] = Field(
        default_factory=list, description="変換時の警告メッセージ（例: フォント置換）"
    )
    important_remark_for_user: str | None = Field(
        None, description="ユーザーへの重要な注意事項"
    )

"""Middleman.ai APIクライアントの実装。"""

import json
import logging
from typing import Any, Dict, List, cast

import requests
from pydantic import BaseModel, Field
from pydantic import ValidationError as PydanticValidationError

from .exceptions import (
    BadRequestError,
    ConnectionError,
    ForbiddenError,
    InternalError,
    NotEnoughCreditError,
    NotFoundError,
    ValidationError,
)
from .models import (
    DocxToPageImagesResponse,
    JsonToPptxAnalyzeResponse,
    JsonToPptxExecuteResponse,
    MdToDocxResponse,
    MdToPdfResponse,
    MermaidToImageOptions,
    MermaidToImageResponse,
    PdfToPageImagesResponse,
    PptxToPageImagesResponse,
    XlsxToPageImagesResponse,
    XlsxToPdfAnalyzeResponse,
    XlsxToPdfExecuteResponse,
)

# HTTPステータスコード
HTTP_BAD_REQUEST = 400
HTTP_PAYMENT_REQUIRED = 402
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_UNPROCESSABLE_ENTITY = 422
HTTP_INTERNAL_SERVER_ERROR = 500


class Placeholder(BaseModel):
    name: str = Field(description="The key of the placeholder")
    content: str = Field(description="The content of the placeholder")


class Slide(BaseModel):
    type: str = Field(description="The type of the slide")
    placeholders: list[Placeholder] = Field(description="The placeholders of the slide")

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "placeholders": [
                {"name": p.name, "content": p.content} for p in self.placeholders
            ],
        }


class Presentation(BaseModel):
    slides: list[Slide] = Field(description="The slides of the presentation")

    def to_dict(self) -> list[dict]:
        return [slide.to_dict() for slide in self.slides]


class ToolsClient:
    """Middleman.ai APIクライアント。"""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://middleman-ai.com/",
        timeout: float = 30.0,
    ) -> None:
        """クライアントを初期化します。

        Args:
            api_key: Middleman.aiで発行されたAPIキー
            base_url: APIのベースURL
            timeout: HTTP通信のタイムアウト秒数
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
        )

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """APIレスポンスを処理し、エラーがあれば適切な例外を発生させます。

        Args:
            response: requestsのレスポンスオブジェクト

        Returns:
            Dict[str, Any]: レスポンスのJSONデータ

        Raises:
            NotEnoughCreditError: クレジット不足（402）
            ForbiddenError: 認証エラー（401, 403）
            NotFoundError: リソースが見つからない（404）
            InternalError: サーバーエラー（500）
            ValidationError: バリデーションエラー（422）
            ConnectionError: 接続エラー
        """
        try:
            response.raise_for_status()
            return cast(Dict[str, Any], response.json())
        except requests.exceptions.HTTPError as e:
            error_body = {}
            try:
                error_body = response.json()
            except json.JSONDecodeError:
                pass

            if response.status_code == HTTP_BAD_REQUEST:
                raise BadRequestError() from e
            if response.status_code == HTTP_PAYMENT_REQUIRED:
                raise NotEnoughCreditError() from e
            if response.status_code in (HTTP_UNAUTHORIZED, HTTP_FORBIDDEN):
                raise ForbiddenError() from e
            if response.status_code == HTTP_NOT_FOUND:
                raise NotFoundError() from e
            if response.status_code >= HTTP_INTERNAL_SERVER_ERROR:
                # サーバーエラーの詳細情報をログに出力
                logging.error(
                    f"サーバーエラー発生: "
                    f"status_code={response.status_code}, "
                    f"url={response.url}, \n"
                    f"headers={response.headers}, \n"
                    f"body={error_body if error_body else response.text[:500]}"
                )
                error_message = (
                    f"サーバーエラー: "
                    f"{error_body if error_body else response.text[:500]}"
                )
                raise InternalError(error_message) from e
            if response.status_code == HTTP_UNPROCESSABLE_ENTITY:
                error_message = (
                    f"Validation error: {error_body}" if error_body else str(e)
                )
                raise ValidationError(error_message) from e
            raise BadRequestError(str(e)) from e
        except requests.exceptions.RequestException as e:
            raise ConnectionError() from e
        except json.JSONDecodeError as e:
            raise ValidationError("Invalid JSON response") from e

    def md_to_pdf(self, markdown_text: str, pdf_template_id: str | None = None) -> str:
        """Markdown文字列をPDFに変換し、PDFのダウンロードURLを返します。

        Args:
            markdown_text: 変換対象のMarkdown文字列
            pdf_template_id: テンプレートID(UUID)

        Returns:
            str: 生成されたPDFのURL

        Raises:
            ValidationError: 入力データが不正
            その他、_handle_responseで定義される例外
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/tools/md-to-pdf",
                json={
                    "markdown": markdown_text,
                    "pdf_template_id": pdf_template_id,
                },
                timeout=self.timeout,
            )
            data = self._handle_response(response)
            result = MdToPdfResponse.model_validate(data)
            return result.pdf_url
        except PydanticValidationError as e:
            raise ValidationError(str(e)) from e
        except requests.exceptions.RequestException as e:
            raise ConnectionError() from e

    def md_to_docx(
        self,
        markdown_text: str,
        docx_template_id: str | None = None,
    ) -> str:
        """Markdown文字列をDOCXに変換し、DOCXのダウンロードURLを返します。

        Args:
            markdown_text: 変換対象のMarkdown文字列
            docx_template_id: テンプレートID(UUID)

        Returns:
            str: 生成されたDOCXのURL

        Raises:
            ValidationError: 入力データが不正
            その他、_handle_responseで定義される例外
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/tools/md-to-docx",
                json={
                    "markdown": markdown_text,
                    "docx_template_id": docx_template_id,
                },
                timeout=self.timeout,
            )
            data = self._handle_response(response)
            result = MdToDocxResponse.model_validate(data)
            return result.docx_url
        except PydanticValidationError as e:
            raise ValidationError(str(e)) from e

    def pdf_to_page_images(self, pdf_file_path: str) -> List[Dict[str, Any]]:
        """PDFファイルをアップロードしてページごとに画像化し、それぞれの画像URLを返します。

        Args:
            pdf_file_path: ローカルのPDFファイルパス
            request_id: 任意のリクエストID

        Returns:
            List[Dict[str, Any]]: [{"page_no": int, "image_url": str}, ...]

        Raises:
            ValidationError: 入力データが不正
            その他、_handle_responseで定義される例外
        """
        try:
            with open(pdf_file_path, "rb") as f:
                files = {"pdf_file": (f.name, f.read(), "application/pdf")}
                headers = dict(self.session.headers)
                del headers["Content-Type"]
                # sessionを共有するとContent-Typeがapplicatoin/jsonになるので
                # マルチパートの送信を可能にするために直接requestsを使用
                response = requests.post(
                    f"{self.base_url}/api/v1/tools/pdf-to-page-images",
                    files=files,
                    headers=headers,
                    timeout=self.timeout,
                )
                data = self._handle_response(response)
                result = PdfToPageImagesResponse.model_validate(data)
                return [
                    {"page_no": page.page_no, "image_url": page.image_url}
                    for page in result.pages
                ]
        except PydanticValidationError as e:
            raise ValidationError(str(e)) from e
        except OSError as e:
            raise ValidationError(f"Failed to read PDF file: {e}") from e

    def pptx_to_page_images(self, pptx_file_path: str) -> List[Dict[str, Any]]:
        """PPTXファイルをアップロードしてスライドごとに画像化し、それぞれの画像URLを返します。

        Args:
            pptx_file_path: ローカルのPPTXファイルパス

        Returns:
            List[Dict[str, Any]]: [{"page_no": int, "image_url": str}, ...]

        Raises:
            ValidationError: 入力データが不正
            その他、_handle_responseで定義される例外
        """
        try:
            with open(pptx_file_path, "rb") as f:
                files = {
                    "pptx_file": (
                        f.name,
                        f.read(),
                        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    )
                }
                headers = dict(self.session.headers)
                del headers["Content-Type"]
                # sessionを共有するとContent-Typeがapplicatoin/jsonになるので
                # マルチパートの送信を可能にするために直接requestsを使用
                response = requests.post(
                    f"{self.base_url}/api/v1/tools/pptx-to-page-images",
                    files=files,
                    headers=headers,
                    timeout=self.timeout,
                )
                data = self._handle_response(response)
                result = PptxToPageImagesResponse.model_validate(data)
                return [
                    {"page_no": page.page_no, "image_url": page.image_url}
                    for page in result.pages
                ]
        except PydanticValidationError as e:
            raise ValidationError(str(e)) from e
        except OSError as e:
            raise ValidationError(f"Failed to read PPTX file: {e}") from e

    def docx_to_page_images(self, docx_file_path: str) -> List[Dict[str, Any]]:
        """DOCXファイルをアップロードしてページごとに画像化し、それぞれの画像URLを返します。

        Args:
            docx_file_path: ローカルのDOCXファイルパス

        Returns:
            List[Dict[str, Any]]: [{"page_no": int, "image_url": str}, ...]

        Raises:
            ValidationError: 入力データが不正
            その他、_handle_responseで定義される例外
        """
        try:
            with open(docx_file_path, "rb") as f:
                files = {
                    "docx_file": (
                        f.name,
                        f.read(),
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )
                }
                headers = dict(self.session.headers)
                del headers["Content-Type"]
                # sessionを共有するとContent-Typeがapplicatoin/jsonになるので
                # マルチパートの送信を可能にするために直接requestsを使用
                response = requests.post(
                    f"{self.base_url}/api/v1/tools/docx-to-page-images",
                    files=files,
                    headers=headers,
                    timeout=self.timeout,
                )
                data = self._handle_response(response)
                result = DocxToPageImagesResponse.model_validate(data)
                return [
                    {"page_no": page.page_no, "image_url": page.image_url}
                    for page in result.pages
                ]
        except PydanticValidationError as e:
            raise ValidationError(str(e)) from e
        except OSError as e:
            raise ValidationError(f"Failed to read DOCX file: {e}") from e

    def xlsx_to_page_images(self, xlsx_file_path: str) -> List[Dict[str, Any]]:
        """XLSXファイルをアップロードしてページごとに画像化し、それぞれの画像URLを返します。

        Args:
            xlsx_file_path: ローカルのXLSXファイルパス

        Returns:
            List[Dict[str, Any]]: [{"page_no": int, "image_url": str}, ...]

        Raises:
            ValidationError: 入力データが不正
            その他、_handle_responseで定義される例外
        """
        try:
            with open(xlsx_file_path, "rb") as f:
                files = {
                    "xlsx_file": (
                        f.name,
                        f.read(),
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                }
                headers = dict(self.session.headers)
                del headers["Content-Type"]
                # sessionを共有するとContent-Typeがapplicatoin/jsonになるので
                # マルチパートの送信を可能にするために直接requestsを使用
                response = requests.post(
                    f"{self.base_url}/api/v1/tools/xlsx-to-page-images",
                    files=files,
                    headers=headers,
                    timeout=self.timeout,
                )
                data = self._handle_response(response)
                result = XlsxToPageImagesResponse.model_validate(data)
                return [
                    {"sheet_name": page.sheet_name, "image_url": page.image_url}
                    for page in result.pages
                ]
        except PydanticValidationError as e:
            raise ValidationError(str(e)) from e
        except OSError as e:
            raise ValidationError(f"Failed to read XLSX file: {e}") from e

    def json_to_pptx_analyze_v2(self, pptx_template_id: str) -> List[Dict[str, Any]]:
        """PPTXテンプレートの構造を解析します。

        Args:
            pptx_template_id: テンプレートID(UUID)

        Returns:
            Dict[str, Any]: テンプレート解析結果

        Raises:
            ValidationError: 入力データが不正
            その他、_handle_responseで定義される例外
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/v2/tools/json-to-pptx/analyze",
                json={"pptx_template_id": pptx_template_id},
                timeout=self.timeout,
            )
            data = self._handle_response(response)
            result = JsonToPptxAnalyzeResponse.model_validate(data)
            return result.slides
        except PydanticValidationError as e:
            raise ValidationError(str(e)) from e

    def json_to_pptx_execute_v2(
        self, pptx_template_id: str, presentation: Presentation
    ) -> str:
        """テンプレートIDとプレゼンテーションを指定し、合成したPPTXを生成します。

        Args:
            pptx_template_id: テンプレートID(UUID)
            presentation: プレゼンテーションのJSON構造。以下の形式:
                {
                    "slides": [
                        {
                            "type": str,
                            "placeholders": [
                                {
                                    "name": str,
                                    "content": str
                                },
                                ...
                            ]
                        },
                        ...
                    ]
                }

        Returns:
            str: 生成されたPPTXのダウンロードURL

        Raises:
            ValidationError: 入力データが不正
            その他、_handle_responseで定義される例外
        """
        try:
            request_data = {
                "pptx_template_id": pptx_template_id,
                "presentation": presentation.model_dump(),
            }
            response = self.session.post(
                f"{self.base_url}/api/v2/tools/json-to-pptx/execute",
                json=request_data,
                timeout=self.timeout,
            )
            data = self._handle_response(response)
            result = JsonToPptxExecuteResponse.model_validate(data)
            return result.pptx_url
        except PydanticValidationError as e:
            raise ValidationError(str(e)) from e

    def mermaid_to_image(
        self,
        mermaid_text: str,
        options: MermaidToImageOptions | None = None,
    ) -> str:
        """Mermaidダイアグラムを画像に変換し、画像のダウンロードURLを返します。

        Args:
            mermaid_text: 変換対象のMermaidダイアグラムテキスト
            options: 変換オプション（テーマ、背景色、サイズなど）

        Returns:
            str: 生成された画像のURL

        Raises:
            ValidationError: 入力データが不正
            その他、_handle_responseで定義される例外
        """
        try:
            request_data: Dict[str, Any] = {
                "content": mermaid_text,
            }

            if options is not None:
                options_dict = options.model_dump(exclude_none=True)
                if options_dict:  # 空でない場合のみ追加
                    request_data["options"] = options_dict

            response = self.session.post(
                f"{self.base_url}/api/v1/tools/mermaid-to-image",
                json=request_data,
                timeout=self.timeout,
            )
            data = self._handle_response(response)
            result = MermaidToImageResponse.model_validate(data)
            return result.image_url
        except PydanticValidationError as e:
            raise ValidationError(str(e)) from e
        except requests.exceptions.RequestException as e:
            raise ConnectionError() from e

    def xlsx_to_pdf_analyze(
        self,
        xlsx_template_id: str,
        sheet_name: str | None = None,
    ) -> XlsxToPdfAnalyzeResponse:
        """Excelテンプレートを解析し、プレースホルダー情報を返します。

        Args:
            xlsx_template_id: ExcelテンプレートID(UUID)
            sheet_name: 解析対象のシート名（省略時は最初のシート）

        Returns:
            XlsxToPdfAnalyzeResponse: 解析結果（シート名、プレースホルダー一覧）

        Raises:
            ValidationError: 入力データが不正
            その他、_handle_responseで定義される例外
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/tools/xlsx-to-pdf-analyze",
                json={
                    "xlsx_template_id": xlsx_template_id,
                    "sheet_name": sheet_name,
                },
                timeout=self.timeout,
            )
            data = self._handle_response(response)
            return XlsxToPdfAnalyzeResponse.model_validate(data)
        except PydanticValidationError as e:
            raise ValidationError(str(e)) from e
        except requests.exceptions.RequestException as e:
            raise ConnectionError() from e

    def xlsx_to_pdf_execute(
        self,
        xlsx_template_id: str,
        placeholders: Dict[str, str],
        sheet_name: str | None = None,
    ) -> XlsxToPdfExecuteResponse:
        """Excelテンプレートのプレースホルダーを置換し、PDFに変換します。

        Args:
            xlsx_template_id: ExcelテンプレートID(UUID)
            placeholders: プレースホルダーの値（キー: 名前、値: 置換文字列）
            sheet_name: 処理対象のシート名（省略時は最初のシート）

        Returns:
            XlsxToPdfExecuteResponse: 変換結果（PDF URL、警告メッセージ）

        Raises:
            ValidationError: 入力データが不正
            その他、_handle_responseで定義される例外
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/tools/xlsx-to-pdf-execute",
                json={
                    "xlsx_template_id": xlsx_template_id,
                    "placeholders": placeholders,
                    "sheet_name": sheet_name,
                },
                timeout=self.timeout,
            )
            data = self._handle_response(response)
            return XlsxToPdfExecuteResponse.model_validate(data)
        except PydanticValidationError as e:
            raise ValidationError(str(e)) from e
        except requests.exceptions.RequestException as e:
            raise ConnectionError() from e

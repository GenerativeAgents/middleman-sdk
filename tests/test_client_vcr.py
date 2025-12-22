"""Pythonクライアント用のVCRテストモジュール。"""

import os
from typing import TYPE_CHECKING

import pytest

from middleman_ai.client import Presentation, ToolsClient

if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest  # noqa: F401


@pytest.fixture
def client() -> ToolsClient:
    """テスト用のToolsClientインスタンスを生成します。

    Returns:
        ToolsClient: テスト用のクライアントインスタンス
    """
    return ToolsClient(
        base_url=os.getenv("MIDDLEMAN_BASE_URL") or "https://middleman-ai.com",
        api_key=os.getenv("MIDDLEMAN_API_KEY") or "",
    )


@pytest.mark.vcr()
def test_md_to_pdf_vcr(client: ToolsClient) -> None:
    """ToolsClient.md_to_pdfの実際のAPIを使用したテスト。

    Note:
        このテストは実際のAPIを呼び出し、レスポンスをキャッシュします。
        初回実行時のみAPIを呼び出し、以降はキャッシュを使用します。
    """
    test_markdown = """# Test Heading

    This is a test markdown document.

    ## Section 1
    - Item 1
    - Item 2
    """
    pdf_url = client.md_to_pdf(markdown_text=test_markdown)
    assert pdf_url.startswith("https://")
    assert "/s/" in pdf_url


@pytest.mark.vcr()
def test_md_to_pdf_with_template_id_vcr(client: ToolsClient) -> None:
    """ToolsClient.md_to_pdfの実際のAPIを使用したテスト。

    Note:
        このテストは実際のAPIを呼び出し、レスポンスをキャッシュします。
        初回実行時のみAPIを呼び出し、以降はキャッシュを使用します。
    """
    test_markdown = """# Test Heading

    This is a test markdown document.

    ## Section 1
    - Item 1
    - Item 2
    """
    pdf_url = client.md_to_pdf(
        markdown_text=test_markdown,
        pdf_template_id=os.getenv("MIDDLEMAN_TEST_PDF_TEMPLATE_ID") or "",
    )
    assert pdf_url.startswith("https://")
    assert "/s/" in pdf_url


@pytest.mark.vcr()
def test_md_to_docx_vcr(client: ToolsClient) -> None:
    """ToolsClient.md_to_docxの実際のAPIを使用したテスト。

    Note:
        このテストは実際のAPIを呼び出し、レスポンスをキャッシュします。
        初回実行時のみAPIを呼び出し、以降はキャッシュを使用します。
    """
    test_markdown = """# Test Heading

    This is a test markdown document.

    ## Section 1
    - Item 1
    - Item 2
    """
    docx_url = client.md_to_docx(markdown_text=test_markdown)
    assert docx_url.startswith("https://")
    assert "/s/" in docx_url


@pytest.mark.vcr()
def test_md_to_docx_with_template_id_vcr(client: ToolsClient) -> None:
    """ToolsClient.md_to_docxの実際のAPIを使用したテスト。

    Note:
        このテストは実際のAPIを呼び出し、レスポンスをキャッシュします。
        初回実行時のみAPIを呼び出し、以降はキャッシュを使用します。
    """
    test_markdown = """# Test Heading

    This is a test markdown document.

    ## Section 1
    - Item 1
    - Item 2
    """
    docx_url = client.md_to_docx(
        markdown_text=test_markdown,
        docx_template_id=os.getenv("MIDDLEMAN_TEST_DOCX_TEMPLATE_ID") or "",
    )
    assert docx_url.startswith("https://")
    assert "/s/" in docx_url


# マルチパートの場合リクエストごとにファイルがどこで分割されるかが異なるようなので
# bodyをマッチ判定の対象外にしている
@pytest.mark.vcr(match_on=["method", "scheme", "port", "path", "query"])
def test_pdf_to_page_images_vcr(client: ToolsClient) -> None:
    """ToolsClient.pdf_to_page_imagesの実際のAPIを使用したテスト。

    Note:
        このテストは実際のAPIを呼び出し、レスポンスをキャッシュします。
        初回実行時のみAPIを呼び出し、以降はキャッシュを使用します。
    """
    pdf_file_path = "tests/data/test.pdf"
    pages = client.pdf_to_page_images(pdf_file_path=pdf_file_path)
    assert isinstance(pages, list)
    assert len(pages) == 3
    assert all(isinstance(page, dict) for page in pages)
    assert all("page_no" in page and "image_url" in page for page in pages)
    assert all(page["image_url"].startswith("https://") for page in pages)
    assert all("/s/" in page["image_url"] for page in pages)


@pytest.mark.vcr()
def test_json_to_pptx_analyze_v2_vcr(client: ToolsClient) -> None:
    """ToolsClient.json_to_pptx_analyze_v2の実際のAPIを使用したテスト。

    Note:
        このテストは実際のAPIを呼び出し、レスポンスをキャッシュします。
        初回実行時のみAPIを呼び出し、以降はキャッシュを使用します。
    """
    template_id = (
        os.getenv("MIDDLEMAN_TEST_PPTX_TEMPLATE_ID") or ""
    )  # テスト用のテンプレートID
    slides = client.json_to_pptx_analyze_v2(pptx_template_id=template_id)
    assert isinstance(slides, list)
    assert len(slides) >= 1
    assert all(isinstance(slide, dict) for slide in slides)
    assert all("position" in slide for slide in slides)
    assert all("type" in slide for slide in slides)
    assert all("description" in slide for slide in slides)
    assert all("placeholders" in slide for slide in slides)

    for slide in slides:
        placeholders = slide["placeholders"]
        assert all(isinstance(placeholder, dict) for placeholder in placeholders)
        assert all("name" in placeholder for placeholder in placeholders)
        assert all("description" in placeholder for placeholder in placeholders)


@pytest.mark.vcr()
def test_json_to_pptx_execute_v2_vcr(client: ToolsClient) -> None:
    """ToolsClient.json_to_pptx_execute_v2の実際のAPIを使用したテスト。

    Note:
        このテストは実際のAPIを呼び出し、レスポンスをキャッシュします。
        初回実行時のみAPIを呼び出し、以降はキャッシュを使用します。
    """
    template_id = (
        os.getenv("MIDDLEMAN_TEST_PPTX_TEMPLATE_ID") or ""
    )  # テスト用のテンプレートID
    presentation = {
        "slides": [
            {
                "type": "title",
                "placeholders": [
                    {"name": "title", "content": "Test Title"},
                    {"name": "subtitle", "content": "Test Subtitle"},
                ],
            }
        ]
    }
    pptx_url = client.json_to_pptx_execute_v2(
        pptx_template_id=template_id,
        presentation=Presentation.model_validate(
            presentation,
        ),
    )
    assert isinstance(pptx_url, str)
    assert pptx_url.startswith("https://")
    assert "/s/" in pptx_url


@pytest.mark.vcr(match_on=["method", "scheme", "port", "path", "query"])
def test_pptx_to_page_images_vcr(client: ToolsClient) -> None:
    """ToolsClient.pptx_to_page_imagesの実際のAPIを使用したテスト。

    Note:
        このテストは実際のAPIを呼び出し、レスポンスをキャッシュします。
        初回実行時のみAPIを呼び出し、以降はキャッシュを使用します。
    """
    pptx_file_path = "tests/data/test.pptx"
    pages = client.pptx_to_page_images(pptx_file_path=pptx_file_path)
    assert isinstance(pages, list)
    assert len(pages) > 0
    assert all(isinstance(page, dict) for page in pages)
    assert all("page_no" in page and "image_url" in page for page in pages)
    assert all(page["image_url"].startswith("https://") for page in pages)
    assert all("/s/" in page["image_url"] for page in pages)


@pytest.mark.vcr(match_on=["method", "scheme", "port", "path", "query"])
def test_docx_to_page_images_vcr(client: ToolsClient) -> None:
    """ToolsClient.docx_to_page_imagesの実際のAPIを使用したテスト。

    Note:
        このテストは実際のAPIを呼び出し、レスポンスをキャッシュします。
        初回実行時のみAPIを呼び出し、以降はキャッシュを使用します。
    """
    docx_file_path = "tests/data/test.docx"
    pages = client.docx_to_page_images(docx_file_path=docx_file_path)
    assert isinstance(pages, list)
    assert len(pages) > 0
    assert all(isinstance(page, dict) for page in pages)
    assert all("page_no" in page and "image_url" in page for page in pages)
    assert all(page["image_url"].startswith("https://") for page in pages)
    assert all("/s/" in page["image_url"] for page in pages)


@pytest.mark.vcr(match_on=["method", "scheme", "port", "path", "query"])
def test_xlsx_to_page_images_vcr(client: ToolsClient) -> None:
    """ToolsClient.xlsx_to_page_imagesの実際のAPIを使用したテスト。

    Note:
        このテストは実際のAPIを呼び出し、レスポンスをキャッシュします。
        初回実行時のみAPIを呼び出し、以降はキャッシュを使用します。
    """
    xlsx_file_path = "tests/data/test.xlsx"
    pages = client.xlsx_to_page_images(xlsx_file_path=xlsx_file_path)
    assert isinstance(pages, list)
    assert len(pages) > 0
    assert all(isinstance(page, dict) for page in pages)
    assert all("sheet_name" in page and "image_url" in page for page in pages)
    assert all(page["image_url"].startswith("https://") for page in pages)
    assert all("/s/" in page["image_url"] for page in pages)


@pytest.mark.vcr()
def test_mermaid_to_image_vcr(client: ToolsClient) -> None:
    """ToolsClient.mermaid_to_imageの実際のAPIを使用したテスト。

    Note:
        このテストは実際のAPIを呼び出し、レスポンスをキャッシュします。
        初回実行時のみAPIを呼び出し、以降はキャッシュを使用します。
    """
    test_mermaid = """graph TD
    A[Start] --> B[Process]
    B --> C{Decision}
    C -->|Yes| D[End]
    C -->|No| B"""

    image_url = client.mermaid_to_image(mermaid_text=test_mermaid)
    assert isinstance(image_url, str)
    assert image_url.startswith("https://")
    assert "/s/" in image_url


@pytest.mark.vcr()
def test_mermaid_to_image_with_options_vcr(client: ToolsClient) -> None:
    """ToolsClient.mermaid_to_imageのオプション付きテスト。

    Note:
        このテストは実際のAPIを呼び出し、レスポンスをキャッシュします。
        初回実行時のみAPIを呼び出し、以降はキャッシュを使用します。
    """
    from middleman_ai.models import CustomSize, MermaidToImageOptions

    test_mermaid = """graph LR
    A[User] --> B[API]
    B --> C[Response]
    C --> A"""

    options = MermaidToImageOptions(
        theme="dark",
        background_color="transparent",
        custom_size=CustomSize(width=800, height=600),
    )

    image_url = client.mermaid_to_image(mermaid_text=test_mermaid, options=options)
    assert isinstance(image_url, str)
    assert image_url.startswith("https://")
    assert "/s/" in image_url


@pytest.mark.vcr()
def test_xlsx_to_pdf_analyze_vcr(client: ToolsClient) -> None:
    """ToolsClient.xlsx_to_pdf_analyzeの実際のAPIを使用したテスト。

    Note:
        このテストは実際のAPIを呼び出し、レスポンスをキャッシュします。
        初回実行時のみAPIを呼び出し、以降はキャッシュを使用します。
    """
    template_id = os.getenv("MIDDLEMAN_TEST_XLSX_TEMPLATE_ID") or ""
    result = client.xlsx_to_pdf_analyze(xlsx_template_id=template_id)
    assert result.sheet_name is not None
    assert isinstance(result.placeholders, list)
    assert len(result.placeholders) > 0
    for placeholder in result.placeholders:
        assert placeholder.key is not None
        assert placeholder.cell is not None


@pytest.mark.vcr()
def test_xlsx_to_pdf_execute_vcr(client: ToolsClient) -> None:
    """ToolsClient.xlsx_to_pdf_executeの実際のAPIを使用したテスト。

    Note:
        このテストは実際のAPIを呼び出し、レスポンスをキャッシュします。
        初回実行時のみAPIを呼び出し、以降はキャッシュを使用します。
    """
    template_id = os.getenv("MIDDLEMAN_TEST_XLSX_TEMPLATE_ID") or ""
    placeholders = {
        "company_name": "テスト株式会社",
        "no": "001",
        "date": "2025/01/01",
        "price": "10000",
    }
    result = client.xlsx_to_pdf_execute(
        xlsx_template_id=template_id,
        placeholders=placeholders,
    )
    assert result.pdf_url is not None
    assert result.pdf_url.startswith("https://")
    assert "/s/" in result.pdf_url

# ruff: noqa: PLR2004

"""LangChainツール群のVCRテストモジュール。"""

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
    return ToolsClient(api_key=os.getenv("MIDDLEMAN_API_KEY") or "")


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
    assert "md-to-pdf" in pdf_url
    assert "blob.core.windows.net" in pdf_url


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
    assert "md-to-docx" in docx_url
    assert "blob.core.windows.net" in docx_url


@pytest.mark.vcr()
def test_md_to_pptx_vcr(client: ToolsClient) -> None:
    """ToolsClient.md_to_pptxの実際のAPIを使用したテスト。

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
    pptx_url = client.md_to_pptx(markdown_text=test_markdown)
    assert pptx_url.startswith("https://")
    assert "md-to-pptx" in pptx_url
    assert "blob.core.windows.net" in pptx_url


# マルチパートの場合リクエストごとにファイルがどこで分割されるかが異なるようなので
# bodyをマッチ判定の対象外にしている
@pytest.mark.vcr(match_on=["method", "scheme", "host", "port", "path", "query"])
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
    assert all("blob.core.windows.net" in page["image_url"] for page in pages)


@pytest.mark.vcr()
def test_json_to_pptx_analyze_v2_vcr(client: ToolsClient) -> None:
    """ToolsClient.json_to_pptx_analyze_v2の実際のAPIを使用したテスト。

    Note:
        このテストは実際のAPIを呼び出し、レスポンスをキャッシュします。
        初回実行時のみAPIを呼び出し、以降はキャッシュを使用します。
    """
    template_id = (
        os.getenv("MIDDLEMAN_TEST_TEMPLATE_ID") or ""
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
        os.getenv("MIDDLEMAN_TEST_TEMPLATE_ID") or ""
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
    assert "json-to-pptx" in pptx_url
    assert "blob.core.windows.net" in pptx_url

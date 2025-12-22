# mypy: disable-error-code="var-annotated"
"""Main CLI implementation."""

import json
import os
import sys

import click

from middleman_ai.client import Placeholder, Presentation, Slide, ToolsClient
from middleman_ai.exceptions import MiddlemanBaseException
from middleman_ai.models import CustomSize, MermaidToImageOptions


def get_base_url() -> str:
    """Get base URL from environment variable."""
    base_url = os.getenv("MIDDLEMAN_BASE_URL", "https://middleman-ai.com")
    return base_url


def get_api_key() -> str:
    """Get API key from environment variable."""
    api_key = os.getenv("MIDDLEMAN_API_KEY")
    print(f"API Key: {'設定されています' if api_key else '設定されていません'}")
    if not api_key:
        raise click.ClickException("MIDDLEMAN_API_KEY environment variable is required")
    return api_key


def get_client() -> ToolsClient:
    """Get client from environment variable."""
    base_url = get_base_url()
    api_key = get_api_key()
    return ToolsClient(base_url=base_url, api_key=api_key)


@click.group()
def cli() -> None:
    """Middleman.ai CLI tools."""
    print("Middleman.ai CLI tools を起動しています...")
    pass


@cli.command()
@click.argument("template_id", required=False)
def md_to_pdf(template_id: str | None = None) -> None:
    """Convert Markdown to PDF."""
    print("md_to_pdf コマンドを実行しています...")
    try:
        client = get_client()
        print("標準入力からMarkdownを読み込んでいます...")
        markdown_text = sys.stdin.read()
        print(
            f"読み込んだMarkdown ({len(markdown_text)} 文字): {markdown_text[:50]}..."
        )
        with click.progressbar(length=1, label="PDFに変換中...", show_eta=False) as bar:
            print("APIを呼び出しています...")
            pdf_url = client.md_to_pdf(markdown_text, pdf_template_id=template_id)
            bar.update(1)
        print(f"変換結果URL: {pdf_url}")
        if template_id:
            print(f"使用したテンプレートID: {template_id}")
    except MiddlemanBaseException as e:
        print(f"エラーが発生しました: {e!s}")
        raise click.ClickException(str(e)) from e
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e!s}")
        raise


@cli.command()
@click.argument("template_id", required=False)
def md_to_docx(template_id: str | None = None) -> None:
    """Convert Markdown to DOCX."""
    print("md_to_docx コマンドを実行しています...")
    try:
        client = get_client()
        print("標準入力からMarkdownを読み込んでいます...")
        markdown_text = sys.stdin.read()
        print(
            f"読み込んだMarkdown ({len(markdown_text)} 文字): {markdown_text[:50]}..."
        )
        with click.progressbar(
            length=1, label="DOCXに変換中...", show_eta=False
        ) as bar:
            print("APIを呼び出しています...")
            docx_url = client.md_to_docx(markdown_text, docx_template_id=template_id)
            bar.update(1)
        print(f"変換結果URL: {docx_url}")
        if template_id:
            print(f"使用したテンプレートID: {template_id}")
    except MiddlemanBaseException as e:
        print(f"エラーが発生しました: {e!s}")
        raise click.ClickException(str(e)) from e
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e!s}")
        raise


@cli.command()
@click.argument("pdf_path", type=click.Path(exists=True))
def pdf_to_page_images(pdf_path: str) -> None:
    """Convert PDF pages to images."""
    try:
        client = get_client()
        with click.progressbar(
            length=1, label="PDFを画像に変換中...", show_eta=False
        ) as bar:
            results = client.pdf_to_page_images(pdf_path)
            bar.update(1)
        for page in results:
            print(f"Page {page['page_no']}: {page['image_url']}")
    except MiddlemanBaseException as e:
        raise click.ClickException(str(e)) from e


@cli.command()
@click.argument("pptx_path", type=click.Path(exists=True))
def pptx_to_page_images(pptx_path: str) -> None:
    """Convert PPTX pages to images."""
    try:
        client = get_client()
        with click.progressbar(
            length=1, label="PPTXを画像に変換中...", show_eta=False
        ) as bar:
            results = client.pptx_to_page_images(pptx_path)
            bar.update(1)
        for page in results:
            print(f"Page {page['page_no']}: {page['image_url']}")
    except MiddlemanBaseException as e:
        raise click.ClickException(str(e)) from e


@cli.command()
@click.argument("docx_path", type=click.Path(exists=True))
def docx_to_page_images(docx_path: str) -> None:
    """Convert DOCX pages to images."""
    try:
        client = get_client()
        with click.progressbar(
            length=1, label="DOCXを画像に変換中...", show_eta=False
        ) as bar:
            results = client.docx_to_page_images(docx_path)
            bar.update(1)
        for page in results:
            print(f"Page {page['page_no']}: {page['image_url']}")
    except MiddlemanBaseException as e:
        raise click.ClickException(str(e)) from e


@cli.command()
@click.argument("xlsx_path", type=click.Path(exists=True))
def xlsx_to_page_images(xlsx_path: str) -> None:
    """Convert XLSX pages to images."""
    try:
        client = get_client()
        with click.progressbar(
            length=1, label="XLSXを画像に変換中...", show_eta=False
        ) as bar:
            results = client.xlsx_to_page_images(xlsx_path)
            bar.update(1)
        for page in results:
            print(f"Sheet {page['sheet_name']}: {page['image_url']}")
    except MiddlemanBaseException as e:
        raise click.ClickException(str(e)) from e


@cli.command()
@click.argument("template_id")
def json_to_pptx_analyze(template_id: str) -> None:
    """Analyze PPTX template."""
    try:
        client = get_client()
        with click.progressbar(
            length=1, label="テンプレートを解析中...", show_eta=False
        ) as bar:
            results = client.json_to_pptx_analyze_v2(template_id)
            bar.update(1)
        print(json.dumps(results, indent=2))
    except MiddlemanBaseException as e:
        raise click.ClickException(str(e)) from e


@cli.command()
@click.argument("template_id")
def json_to_pptx_execute(template_id: str) -> None:
    """Execute PPTX template with data from stdin."""
    try:
        client = get_client()
        data = json.loads(sys.stdin.read())
        presentation = Presentation(
            slides=[
                Slide(
                    type=slide["type"],
                    placeholders=[
                        Placeholder(name=p["name"], content=p["content"])
                        for p in slide["placeholders"]
                    ],
                )
                for slide in data["slides"]
            ]
        )
        with click.progressbar(
            length=1, label="PPTXを生成中...", show_eta=False
        ) as bar:
            pptx_url = client.json_to_pptx_execute_v2(template_id, presentation)
            bar.update(1)
        print(pptx_url)
    except (json.JSONDecodeError, KeyError) as e:
        raise click.ClickException(f"Invalid JSON input: {e!s}") from e
    except MiddlemanBaseException as e:
        raise click.ClickException(str(e)) from e


@cli.command()
@click.option(
    "--theme",
    type=click.Choice(["default", "dark", "forest", "neutral"]),
    help="Mermaidテーマ",
)
@click.option("--background-color", help="背景色（例: transparent, #ffffff, #000000")
@click.option("--width", type=int, help="画像幅（100-1200px）")
@click.option("--height", type=int, help="画像高さ（100-1200px）")
def mermaid_to_image(
    theme: str | None,
    background_color: str | None,
    width: int | None,
    height: int | None,
) -> None:
    """Convert Mermaid diagram to image."""
    print("mermaid_to_image コマンドを実行しています...")
    try:
        client = get_client()
        print("標準入力からMermaidダイアグラムを読み込んでいます...")
        mermaid_text = sys.stdin.read()
        print(f"読み込んだMermaid ({len(mermaid_text)} 文字): {mermaid_text[:50]}...")

        # オプション設定
        custom_size = None
        if width is not None and height is not None:
            custom_size = CustomSize(width=width, height=height)
        elif (width is not None) != (height is not None):
            raise click.ClickException(
                "widthとheightは両方指定するか、両方省略してください"
            )

        # 全てNoneの場合はoptionsもNoneにする
        options = None
        if theme is not None or background_color is not None or custom_size is not None:
            options = MermaidToImageOptions(
                theme=theme, background_color=background_color, custom_size=custom_size
            )

        with click.progressbar(
            length=1, label="画像に変換中...", show_eta=False
        ) as bar:
            print("APIを呼び出しています...")
            image_url = client.mermaid_to_image(mermaid_text, options=options)
            bar.update(1)
        print(f"変換結果URL: {image_url}")
    except MiddlemanBaseException as e:
        print(f"エラーが発生しました: {e!s}")
        raise click.ClickException(str(e)) from e
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e!s}")
        raise


@cli.command()
@click.argument("xlsx_template_id")
@click.option("--sheet-name", help="解析対象のシート名（省略時は最初のシート）")
def xlsx_to_pdf_analyze(xlsx_template_id: str, sheet_name: str | None = None) -> None:
    """Analyze Excel template and show placeholders."""
    try:
        client = get_client()
        with click.progressbar(
            length=1, label="テンプレートを解析中...", show_eta=False
        ) as bar:
            result = client.xlsx_to_pdf_analyze(
                xlsx_template_id, sheet_name=sheet_name
            )
            bar.update(1)
        print(f"シート名: {result.sheet_name}")
        print(f"プレースホルダー数: {len(result.placeholders)}")
        for ph in result.placeholders:
            print(f"  - {ph.key}: {ph.description} (セル: {ph.cell})")
        print(f"\nJSON Schema:\n{result.placeholders_json_schema}")
    except MiddlemanBaseException as e:
        raise click.ClickException(str(e)) from e


@cli.command()
@click.argument("xlsx_template_id")
@click.option("--sheet-name", help="処理対象のシート名（省略時は最初のシート）")
def xlsx_to_pdf_execute(xlsx_template_id: str, sheet_name: str | None = None) -> None:
    """Execute Excel to PDF conversion with placeholders from stdin (JSON)."""
    try:
        client = get_client()
        print("標準入力からプレースホルダーJSON を読み込んでいます...")
        placeholders = json.loads(sys.stdin.read())
        with click.progressbar(
            length=1, label="PDFに変換中...", show_eta=False
        ) as bar:
            result = client.xlsx_to_pdf_execute(
                xlsx_template_id, placeholders, sheet_name=sheet_name
            )
            bar.update(1)
        print(f"PDF URL: {result.pdf_url}")
        if result.warnings:
            print("警告:")
            for warning in result.warnings:
                print(f"  - {warning}")
    except json.JSONDecodeError as e:
        raise click.ClickException(f"Invalid JSON input: {e!s}") from e
    except MiddlemanBaseException as e:
        raise click.ClickException(str(e)) from e


@click.command()
def mcp_server() -> None:
    """Run MCP server as a standalone command."""
    _run_mcp_server()


def _run_mcp_server() -> None:
    """Internal function to run MCP server."""
    print("MCP server is running (transport: stdio)...")

    api_key = os.getenv("MIDDLEMAN_API_KEY", "")
    if not api_key:
        print("Warning: MIDDLEMAN_API_KEY environment variable is not set.")

    from ..mcp.server import run_server

    run_server()


# モジュールとして実行された場合のエントリーポイント
if __name__ == "__main__":
    cli()

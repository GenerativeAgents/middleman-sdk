"""Main CLI implementation."""

import json
import os
import sys

import click

from middleman_ai.client import Placeholder, Presentation, Slide, ToolsClient
from middleman_ai.exceptions import MiddlemanBaseException


def get_api_key() -> str:
    """Get API key from environment variable."""
    api_key = os.getenv("MIDDLEMAN_API_KEY")
    print(f"API Key: {'設定されています' if api_key else '設定されていません'}")
    if not api_key:
        raise click.ClickException("MIDDLEMAN_API_KEY environment variable is required")
    return api_key


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
        client = ToolsClient(api_key=get_api_key())
        print("標準入力からMarkdownを読み込んでいます...")
        markdown_text = sys.stdin.read()
        print(
            f"読み込んだMarkdown ({len(markdown_text)} 文字): {markdown_text[:50]}..."
        )
        with click.progressbar(length=1, label="PDFに変換中...", show_eta=False) as bar:  # type: ignore[var-annotated]
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
def md_to_docx() -> None:
    """Convert Markdown to DOCX."""
    print("md_to_docx コマンドを実行しています...")
    try:
        client = ToolsClient(api_key=get_api_key())
        print("標準入力からMarkdownを読み込んでいます...")
        markdown_text = sys.stdin.read()
        print(
            f"読み込んだMarkdown ({len(markdown_text)} 文字): {markdown_text[:50]}..."
        )
        with click.progressbar(  # type: ignore[var-annotated]
            length=1, label="DOCXに変換中...", show_eta=False
        ) as bar:
            print("APIを呼び出しています...")
            docx_url = client.md_to_docx(markdown_text)
            bar.update(1)
        print(f"変換結果URL: {docx_url}")
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
        client = ToolsClient(api_key=get_api_key())
        with click.progressbar(  # type: ignore[var-annotated]
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
        client = ToolsClient(api_key=get_api_key())
        with click.progressbar(  # type: ignore[var-annotated]
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
        client = ToolsClient(api_key=get_api_key())
        with click.progressbar(  # type: ignore[var-annotated]
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
        client = ToolsClient(api_key=get_api_key())
        with click.progressbar(  # type: ignore[var-annotated]
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
        client = ToolsClient(api_key=get_api_key())
        with click.progressbar(  # type: ignore[var-annotated]
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
        client = ToolsClient(api_key=get_api_key())
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
        with click.progressbar(  # type: ignore[var-annotated]
            length=1, label="PPTXを生成中...", show_eta=False
        ) as bar:
            pptx_url = client.json_to_pptx_execute_v2(template_id, presentation)
            bar.update(1)
        print(pptx_url)
    except (json.JSONDecodeError, KeyError) as e:
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

"""Main CLI implementation."""

import json
import os
import sys

import click

from ..client import Placeholder, Presentation, Slide, ToolsClient
from ..exceptions import MiddlemanBaseException


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
def md_to_pdf() -> None:
    """Convert Markdown to PDF."""
    print("md_to_pdf コマンドを実行しています...")
    try:
        client = ToolsClient(api_key=get_api_key())
        print("標準入力からMarkdownを読み込んでいます...")
        markdown_text = sys.stdin.read()
        print(
            f"読み込んだMarkdown ({len(markdown_text)} 文字): {markdown_text[:50]}..."
        )
        with click.progressbar(
            length=1, label="PDFに変換中...", show_eta=False
        ) as bar:  # type: Any
            print("APIを呼び出しています...")
            pdf_url = client.md_to_pdf(markdown_text)
            bar.update(1)
        print(f"変換結果URL: {pdf_url}")
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
        with click.progressbar(
            length=1, label="DOCXに変換中...", show_eta=False
        ) as bar:  # type: Any
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
def md_to_pptx() -> None:
    """Convert Markdown to PPTX."""
    try:
        client = ToolsClient(api_key=get_api_key())
        markdown_text = sys.stdin.read()
        with click.progressbar(
            length=1, label="PPTXに変換中...", show_eta=False
        ) as bar:  # type: Any
            pptx_url = client.md_to_pptx(markdown_text)
            bar.update(1)
        print(pptx_url)
    except MiddlemanBaseException as e:
        raise click.ClickException(str(e)) from e


@cli.command()
@click.argument("pdf_path", type=click.Path(exists=True))
def pdf_to_page_images(pdf_path: str) -> None:
    """Convert PDF pages to images."""
    try:
        client = ToolsClient(api_key=get_api_key())
        with click.progressbar(
            length=1, label="PDFを画像に変換中...", show_eta=False
        ) as bar:  # type: Any
            results = client.pdf_to_page_images(pdf_path)
            bar.update(1)
        for page in results:
            print(f"Page {page['page_no']}: {page['image_url']}")
    except MiddlemanBaseException as e:
        raise click.ClickException(str(e)) from e


@cli.command()
@click.argument("template_id")
def json_to_pptx_analyze(template_id: str) -> None:
    """Analyze PPTX template."""
    try:
        client = ToolsClient(api_key=get_api_key())
        with click.progressbar(
            length=1, label="テンプレートを解析中...", show_eta=False
        ) as bar:  # type: Any
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
        with click.progressbar(
            length=1, label="PPTXを生成中...", show_eta=False
        ) as bar:  # type: Any
            pptx_url = client.json_to_pptx_execute_v2(template_id, presentation)
            bar.update(1)
        print(pptx_url)
    except (json.JSONDecodeError, KeyError) as e:
        raise click.ClickException(f"Invalid JSON input: {e!s}") from e
    except MiddlemanBaseException as e:
        raise click.ClickException(str(e)) from e


# モジュールとして実行された場合のエントリーポイント
if __name__ == "__main__":
    cli()

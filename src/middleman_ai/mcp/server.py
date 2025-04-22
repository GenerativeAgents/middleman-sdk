import os
import sys
from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP

from middleman_ai import ToolsClient
from middleman_ai.client import Placeholder, Presentation, Slide

print("Starting server.py...", file=sys.stderr)
print(f"Python version: {sys.version}", file=sys.stderr)
print(f"Python executable: {sys.executable}", file=sys.stderr)
print(f"Current directory: {os.getcwd()}", file=sys.stderr)


mcp = FastMCP("Middleman Tools")

api_key = os.environ.get("MIDDLEMAN_API_KEY", "")
client = ToolsClient(api_key=api_key)


@mcp.tool()
def md_to_pdf(markdown_text: str, pdf_template_id: str | None = None) -> str:
    """
    Convert Markdown text to PDF and return the download URL.

    Args:
        markdown_text: The Markdown text to convert
        pdf_template_id: Optional ID of the PDF template to use.
        If not provided, the default template will be used

    Returns:
        The URL to download the generated PDF
    """
    return client.md_to_pdf(markdown_text, pdf_template_id=pdf_template_id)


@mcp.tool()
def md_to_docx(markdown_text: str) -> str:
    """
    Convert Markdown text to DOCX and return the download URL.

    Args:
        markdown_text: The Markdown text to convert

    Returns:
        The URL to download the generated DOCX
    """
    return client.md_to_docx(markdown_text)


@mcp.tool()
def pdf_to_page_images(pdf_file_path: str) -> List[Dict[str, Any]]:
    """
    Convert a PDF file to page images and return the image URLs.

    Args:
        pdf_file_path: Path to the local PDF file

    Returns:
        A list of dictionaries with page_no and image_url for each page
    """
    return client.pdf_to_page_images(pdf_file_path)


@mcp.tool()
def pptx_to_page_images(pptx_file_path: str) -> List[Dict[str, Any]]:
    """
    Convert a PPTX file to page images and return the image URLs.

    Args:
        pptx_file_path: Path to the local PPTX file

    Returns:
        A list of dictionaries with page_no and image_url for each page
    """
    return client.pptx_to_page_images(pptx_file_path)


@mcp.tool()
def docx_to_page_images(docx_file_path: str) -> List[Dict[str, Any]]:
    """
    Convert a DOCX file to page images and return the image URLs.

    Args:
        docx_file_path: Path to the local DOCX file

    Returns:
        A list of dictionaries with page_no and image_url for each page
    """
    return client.docx_to_page_images(docx_file_path)


@mcp.tool()
def xlsx_to_page_images(xlsx_file_path: str) -> List[Dict[str, Any]]:
    """
    Convert a XLSX file to page images and return the image URLs.

    Args:
        xlsx_file_path: Path to the local XLSX file

    Returns:
        A list of dictionaries with sheet_name and image_url for each sheet
    """
    return client.xlsx_to_page_images(xlsx_file_path)


@mcp.tool()
def json_to_pptx_analyze(pptx_template_id: str) -> List[Dict[str, Any]]:
    """
    Analyze a PPTX template structure.

    Args:
        pptx_template_id: The template ID (UUID)

    Returns:
        The template analysis result with slide types and placeholders
    """
    return client.json_to_pptx_analyze_v2(pptx_template_id)


@mcp.tool()
def json_to_pptx_execute(pptx_template_id: str, slides: List[Dict[str, Any]]) -> str:
    """
    Generate a PPTX from JSON data using a template.

    Args:
        pptx_template_id: The template ID (UUID)
        slides: A list of slide definitions with type and placeholders

    Returns:
        The URL to download the generated PPTX
    """
    presentation_slides = []
    for slide_data in slides:
        placeholders = []
        for ph in slide_data.get("placeholders", []):
            placeholders.append(Placeholder(name=ph["name"], content=ph["content"]))

        presentation_slides.append(
            Slide(type=slide_data["type"], placeholders=placeholders)
        )

    presentation = Presentation(slides=presentation_slides)
    return client.json_to_pptx_execute_v2(pptx_template_id, presentation)


def run_server() -> None:
    """
    MCPサーバーを実行します。

    Args:
        transport: 使用するトランスポート方式（"stdio", "sse"）
    """
    mcp.run(transport="stdio")


if __name__ == "__main__":
    print("Running server.py as main script", file=sys.stderr)
    run_server()

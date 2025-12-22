import os
import sys
from pathlib import Path
from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP

from middleman_ai import ToolsClient
from middleman_ai.client import Placeholder, Presentation, Slide
from middleman_ai.models import CustomSize, MermaidToImageOptions

print("Starting server.py...", file=sys.stderr)
print(f"Python version: {sys.version}", file=sys.stderr)
print(f"Python executable: {sys.executable}", file=sys.stderr)
print(f"Current directory: {os.getcwd()}", file=sys.stderr)


mcp = FastMCP("Middleman Tools")

api_key = os.environ.get("MIDDLEMAN_API_KEY", "")
base_url = os.environ.get("MIDDLEMAN_BASE_URL", "https://middleman-ai.com/")
client = ToolsClient(api_key=api_key, base_url=base_url)


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
def md_file_to_pdf(md_file_full_path: str, pdf_template_id: str | None = None) -> str:
    """
    Convert a Markdown file to PDF and return the download URL.

    Args:
        md_file_full_path: Path to the local Markdown file
        pdf_template_id: Optional ID of the PDF template to use.
        If not provided, the default template will be used

    Returns:
        The URL to download the generated PDF
    """
    file_path = Path(md_file_full_path)
    if not file_path.exists():
        raise ValueError(f"File not found: {md_file_full_path}")
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {md_file_full_path}")
    if not os.access(file_path, os.R_OK):
        raise ValueError(f"File not readable: {md_file_full_path}")

    with file_path.open("r") as f:
        md_text = f.read()
    return client.md_to_pdf(md_text, pdf_template_id=pdf_template_id)


@mcp.tool()
def md_to_docx(markdown_text: str, docx_template_id: str | None = None) -> str:
    """
    Convert Markdown text to DOCX and return the download URL.

    Args:
        markdown_text: The Markdown text to convert
        docx_template_id: Optional ID of the DOCX template to use.
        If not provided, the default template will be used

    Returns:
        The URL to download the generated DOCX
    """
    return client.md_to_docx(markdown_text, docx_template_id=docx_template_id)


@mcp.tool()
def md_file_to_docx(md_file_full_path: str, docx_template_id: str | None = None) -> str:
    """
    Convert a Markdown file to DOCX and return the download URL.

    Args:
        md_file_full_path: Path to the local Markdown file
        docx_template_id: Optional ID of the DOCX template to use.
        If not provided, the default template will be used

    Returns:
        The URL to download the generated DOCX
    """
    file_path = Path(md_file_full_path)
    if not file_path.exists():
        raise ValueError(f"File not found: {md_file_full_path}")
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {md_file_full_path}")
    if not os.access(file_path, os.R_OK):
        raise ValueError(f"File not readable: {md_file_full_path}")

    with file_path.open("r") as f:
        md_text = f.read()
    return client.md_to_docx(md_text, docx_template_id=docx_template_id)


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


@mcp.tool()
def mermaid_to_image(
    mermaid_text: str,
    theme: str | None = None,
    background_color: str | None = None,
    width: int = -1,
    height: int = -1,
) -> str:
    """
    Convert Mermaid diagram text to image and return the download URL.

    Args:
        mermaid_text: The Mermaid diagram text to convert
        theme: Optional theme for the diagram (default, dark, forest, neutral)
        background_color: Optional background color (transparent or RGB color)
        width: Image width in pixels (100-1200)
        height: Image height in pixels (100-1200)

    Returns:
        The URL to download the generated image
    """
    options = None

    # 内部で使用する型に変換
    actual_width: int | None = None if width == -1 else width
    actual_height: int | None = None if height == -1 else height

    if any([theme, background_color, actual_width, actual_height]):
        custom_size = None
        if actual_width is not None and actual_height is not None:
            custom_size = CustomSize(width=actual_width, height=actual_height)
        elif (actual_width is not None) != (actual_height is not None):
            raise ValueError(
                "Both width and height must be provided together, or both omitted"
            )

        options = MermaidToImageOptions(
            theme=theme,
            background_color=background_color,
            custom_size=custom_size,
        )

    return client.mermaid_to_image(mermaid_text, options=options)


@mcp.tool()
def mermaid_file_to_image(
    mermaid_file_full_path: str,
    theme: str | None = None,
    background_color: str | None = None,
    width: int = -1,
    height: int = -1,
) -> str:
    """
    Convert a Mermaid file to image and return the download URL.

    Args:
        mermaid_file_full_path: Path to the local Mermaid file
        theme: Optional theme for the diagram (default, dark, forest, neutral)
        background_color: Optional background color (transparent or RGB color)
        width: Image width in pixels (100-1200)
        height: Image height in pixels (100-1200)

    Returns:
        The URL to download the generated image
    """
    file_path = Path(mermaid_file_full_path)
    if not file_path.exists():
        raise ValueError(f"File not found: {mermaid_file_full_path}")
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {mermaid_file_full_path}")
    if not os.access(file_path, os.R_OK):
        raise ValueError(f"File not readable: {mermaid_file_full_path}")

    with file_path.open("r") as f:
        mermaid_text = f.read()

    options = None

    # 内部で使用する型に変換
    actual_width: int | None = None if width == -1 else width
    actual_height: int | None = None if height == -1 else height

    if any([theme, background_color, actual_width, actual_height]):
        custom_size = None
        if actual_width is not None and actual_height is not None:
            custom_size = CustomSize(width=actual_width, height=actual_height)
        elif (actual_width is not None) != (actual_height is not None):
            raise ValueError(
                "Both width and height must be provided together, or both omitted"
            )

        options = MermaidToImageOptions(
            theme=theme,
            background_color=background_color,
            custom_size=custom_size,
        )

    return client.mermaid_to_image(mermaid_text, options=options)


@mcp.tool()
def xlsx_to_pdf_analyze(
    xlsx_template_id: str,
    sheet_name: str | None = None,
) -> Dict[str, Any]:
    """
    Analyze an XLSX template and return placeholder information.

    Args:
        xlsx_template_id: The XLSX template ID (UUID)
        sheet_name: Optional sheet name to analyze (default: first sheet)

    Returns:
        A dictionary containing:
        - sheet_name: The analyzed sheet name
        - placeholders: List of placeholder information
        - placeholders_json_schema: JSON schema for the placeholders object
    """
    result = client.xlsx_to_pdf_analyze(xlsx_template_id, sheet_name=sheet_name)
    return {
        "sheet_name": result.sheet_name,
        "placeholders": [p.model_dump() for p in result.placeholders],
        "placeholders_json_schema": result.placeholders_json_schema,
    }


@mcp.tool()
def xlsx_to_pdf_execute(
    xlsx_template_id: str,
    placeholders: Dict[str, str],
    sheet_name: str | None = None,
) -> Dict[str, Any]:
    """
    Replace placeholders in an XLSX template and convert to PDF.

    Args:
        xlsx_template_id: The XLSX template ID (UUID)
        placeholders: Dictionary of placeholder values (key: name, value: text)
        sheet_name: Optional sheet name to process (default: first sheet)

    Returns:
        A dictionary containing:
        - pdf_url: URL to download the generated PDF
        - warnings: List of warning messages from conversion
    """
    result = client.xlsx_to_pdf_execute(
        xlsx_template_id, placeholders, sheet_name=sheet_name
    )
    return {
        "pdf_url": result.pdf_url,
        "warnings": result.warnings,
    }


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

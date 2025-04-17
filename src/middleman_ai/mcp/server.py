import sys
import os
from typing import List, Dict, Any, Literal

print("Starting server.py...", file=sys.stderr)
print(f"Python version: {sys.version}", file=sys.stderr)
print(f"Python executable: {sys.executable}", file=sys.stderr)
print(f"Current directory: {os.getcwd()}", file=sys.stderr)

try:
    from mcp.server.fastmcp import FastMCP
    print("Successfully imported FastMCP", file=sys.stderr)
except ImportError as e:
    print(f"Error importing FastMCP: {e}", file=sys.stderr)
    sys.exit(1)

try:
    from middleman_ai import ToolsClient
    from middleman_ai.client import Presentation, Slide, Placeholder
    print("Successfully imported ToolsClient and models", file=sys.stderr)
except ImportError as e:
    print(f"Error importing ToolsClient: {e}", file=sys.stderr)
    sys.exit(1)

print("Creating FastMCP instance...", file=sys.stderr)
mcp = FastMCP("Middleman Tools")
print("FastMCP instance created", file=sys.stderr)

api_key = os.environ.get("MIDDLEMAN_API_KEY", "")
print(f"API Key: {'Set' if api_key else 'Not set'}", file=sys.stderr)
client = ToolsClient(api_key=api_key)
print("ToolsClient instance created", file=sys.stderr)


@mcp.tool()
def md_to_pdf(markdown_text: str) -> str:
    """
    Convert Markdown text to PDF and return the download URL.

    Args:
        markdown_text: The Markdown text to convert

    Returns:
        The URL to download the generated PDF
    """
    return client.md_to_pdf(markdown_text)


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
def md_to_pptx(markdown_text: str) -> str:
    """
    Convert Markdown text to PPTX and return the download URL.

    Args:
        markdown_text: The Markdown text to convert

    Returns:
        The URL to download the generated PPTX
    """
    return client.md_to_pptx(markdown_text)


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


def run_server(transport: Literal["stdio", "sse"] = "stdio"):
    """
    MCPサーバーを実行します。

    Args:
        transport: 使用するトランスポート方式（"stdio", "sse"）
    """
    print(f"Starting MCP server with transport: {transport}", file=sys.stderr)
    try:
        mcp.run(transport=transport)
    except Exception as e:
        print(f"Error running MCP server: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    print("Running server.py as main script", file=sys.stderr)
    run_server(transport="stdio")

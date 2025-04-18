import os

from middleman_ai import ToolsClient
from middleman_ai.langchain_tools import (
    JsonToPptxAnalyzeTool,
    JsonToPptxExecuteTool,
    MdToDocxTool,
    MdToPdfTool,
    PdfToPageImagesTool,
)


def main() -> None:
    # Initialize client
    client = ToolsClient(api_key=os.getenv("MIDDLEMAN_API_KEY", ""))
    pdf_template_id = os.getenv("MIDDLEMAN_PDF_TEMPLATE_ID", None)
    pptx_template_id = os.getenv("MIDDLEMAN_PPTX_TEMPLATE_ID", None)

    try:
        # Initialize all tools
        md_to_pdf = MdToPdfTool(client=client, default_template_id=pdf_template_id)
        md_to_docx = MdToDocxTool(client=client)
        pdf_to_images = PdfToPageImagesTool(client=client)
        json_to_pptx_analyze = JsonToPptxAnalyzeTool(
            client=client, default_template_id=pptx_template_id
        )
        json_to_pptx_execute = JsonToPptxExecuteTool(
            client=client, default_template_id=pptx_template_id
        )

        # Test each tool's _run method
        markdown_text = "# Sample\nThis is a test."

        # Markdown conversions
        pdf_url = md_to_pdf.run(markdown_text, pdf_template_id=pdf_template_id)
        print(f"Generated PDF URL: {pdf_url}")

        docx_url = md_to_docx.run(markdown_text)
        print(f"Generated DOCX URL: {docx_url}")

        # PDF to images
        images_result = pdf_to_images.run("sample.pdf")
        print(f"Generated image URLs: {images_result}")

        # JSON to PPTX
        template_structure = json_to_pptx_analyze.run("")
        print(f"Template structure: {template_structure}")

        presentation_json = """
        {
            "slides": [
                {
                    "type": "title",
                    "placeholders": [
                        {
                            "name": "title",
                            "content": "Sample Title"
                        }
                    ]
                }
            ]
        }
        """
        pptx_url = json_to_pptx_execute.run(presentation_json)
        print(f"Generated PPTX URL: {pptx_url}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

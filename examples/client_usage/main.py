import os

from middleman_ai import ToolsClient


def main() -> None:
    # Initialize client
    client = ToolsClient(api_key=os.getenv("MIDDLEMAN_API_KEY", ""))

    # Markdown → PDF
    markdown_text = "# Sample\nThis is a test."
    pdf_url = client.md_to_pdf(markdown_text)
    print(f"Generated PDF URL: {pdf_url}")

    # Markdown → DOCX
    docx_url = client.md_to_docx(markdown_text)
    print(f"Generated DOCX URL: {docx_url}")

    # Markdown → PPTX
    pptx_url = client.md_to_pptx(markdown_text)
    print(f"Generated PPTX URL: {pptx_url}")

    # PDF → Page Images
    # Note: Requires a local PDF file
    images = client.pdf_to_page_images("sample.pdf")
    print("Generated image URLs:")
    for page in images:
        print(f"Page {page['page_no']}: {page['image_url']}")

    # JSON → PPTX (analyze)
    template_id = os.getenv("MIDDLEMAN_TEMPLATE_ID", "")
    slides = client.json_to_pptx_analyze_v2(template_id)
    print(f"Template structure: {slides}")

    # JSON → PPTX (execute)
    from middleman_ai.client import Placeholder, Presentation, Slide

    presentation = Presentation(
        slides=[
            Slide(
                type="title",
                placeholders=[Placeholder(name="title", content="Sample Title")],
            )
        ]
    )
    pptx_url = client.json_to_pptx_execute_v2(template_id, presentation)
    print(f"Generated PPTX URL: {pptx_url}")


if __name__ == "__main__":
    main()

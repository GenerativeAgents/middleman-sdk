import os

from middleman_ai import ToolsClient


def main() -> None:
    # Initialize client
    client = ToolsClient(api_key=os.getenv("MIDDLEMAN_API_KEY", ""))

    # Markdown → PDF
    markdown_text = "# Sample\nThis is a test."
    pdf_template_id = os.getenv("MIDDLEMAN_PDF_TEMPLATE_ID", None)
    pdf_url = client.md_to_pdf(markdown_text, pdf_template_id=pdf_template_id)
    print(f"Generated PDF URL (default template): {pdf_url}")

    # Markdown → DOCX
    docx_url = client.md_to_docx(markdown_text)
    print(f"Generated DOCX URL: {docx_url}")

    # PDF → Page Images
    # Note: Requires a local PDF file
    images = client.pdf_to_page_images("sample.pdf")
    print("Generated image URLs:")
    for page in images:
        print(f"Page {page['page_no']}: {page['image_url']}")

    # PPTX → Page Images
    images = client.pptx_to_page_images("sample_template.pptx")
    print("Generated image URLs:")
    for page in images:
        print(f"Page {page['page_no']}: {page['image_url']}")

    # DOCX → Page Images
    images = client.docx_to_page_images("sample.docx")
    print("Generated image URLs:")
    for page in images:
        print(f"Page {page['page_no']}: {page['image_url']}")

    # XLSX → Page Images
    images = client.xlsx_to_page_images("sample.xlsx")
    print("Generated image URLs:")
    for page in images:
        print(f"Sheet {page['sheet_name']}: {page['image_url']}")

    # Mermaid → Image
    mermaid_text = """
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process 1]
    B -->|No| D[Process 2]
    C --> E[End]
    D --> E
    """
    image_url = client.mermaid_to_image(mermaid_text)
    print(f"Generated Mermaid image URL: {image_url}")

    # JSON → PPTX (analyze)
    pptx_template_id = os.getenv("MIDDLEMAN_PPTX_TEMPLATE_ID", "")
    slides = client.json_to_pptx_analyze_v2(pptx_template_id)
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
    pptx_url = client.json_to_pptx_execute_v2(pptx_template_id, presentation)
    print(f"Generated PPTX URL: {pptx_url}")


if __name__ == "__main__":
    main()

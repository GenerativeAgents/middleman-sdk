# mypy: disable-error-code="no-untyped-def"

"""Tests for the CLI implementation."""

import json

import click

from middleman_ai.cli.main import cli


def test_md_to_pdf_cli(runner, mock_client):
    """Test md_to_pdf CLI command."""
    mock_client.md_to_pdf.return_value = "https://example.com/test.pdf"
    result = runner.invoke(cli, ["md-to-pdf"], input="# Test")
    assert result.exit_code == 0
    assert "https://example.com/test.pdf" in result.output
    mock_client.md_to_pdf.assert_called_once_with("# Test", pdf_template_id=None)


def test_md_to_pdf_cli_with_template_id(runner, mock_client):
    mock_client.md_to_pdf.return_value = "https://example.com/test.pdf"
    result = runner.invoke(cli, ["md-to-pdf", "TEMPLATE_ID"], input="# Test")
    assert result.exit_code == 0
    assert "https://example.com/test.pdf" in result.output
    mock_client.md_to_pdf.assert_called_once_with(
        "# Test", pdf_template_id="TEMPLATE_ID"
    )


def test_md_to_docx_cli(runner, mock_client):
    """Test md_to_docx CLI command."""
    mock_client.md_to_docx.return_value = "https://example.com/test.docx"
    result = runner.invoke(cli, ["md-to-docx"], input="# Test")
    assert result.exit_code == 0
    assert "https://example.com/test.docx" in result.output
    mock_client.md_to_docx.assert_called_once_with("# Test", docx_template_id=None)


def test_md_to_docx_cli_with_template_id(runner, mock_client):
    mock_client.md_to_docx.return_value = "https://example.com/test.docx"
    result = runner.invoke(cli, ["md-to-docx", "TEMPLATE_ID"], input="# Test")
    assert result.exit_code == 0
    assert "https://example.com/test.docx" in result.output
    mock_client.md_to_docx.assert_called_once_with(
        "# Test", docx_template_id="TEMPLATE_ID"
    )


def test_pdf_to_page_images_cli(runner, mock_client, tmp_path):
    """Test pdf_to_page_images CLI command."""
    mock_client.pdf_to_page_images.return_value = [
        {"page_no": 1, "image_url": "https://example.com/page1.png"},
        {"page_no": 2, "image_url": "https://example.com/page2.png"},
    ]
    pdf_path = tmp_path / "test.pdf"
    pdf_path.write_bytes(b"dummy pdf content")
    result = runner.invoke(cli, ["pdf-to-page-images", str(pdf_path)])
    assert result.exit_code == 0
    assert "Page 1: https://example.com/page1.png" in result.output
    assert "Page 2: https://example.com/page2.png" in result.output
    mock_client.pdf_to_page_images.assert_called_once_with(str(pdf_path))


def test_json_to_pptx_analyze_cli(runner, mock_client):
    """Test json_to_pptx_analyze CLI command."""
    mock_client.json_to_pptx_analyze_v2.return_value = [
        {"type": "title", "placeholders": [{"name": "title", "content": ""}]}
    ]
    result = runner.invoke(cli, ["json-to-pptx-analyze", "template-123"])
    assert result.exit_code == 0
    assert "title" in result.output
    mock_client.json_to_pptx_analyze_v2.assert_called_once_with("template-123")


def test_json_to_pptx_execute_cli(runner, mock_client):
    """Test json_to_pptx_execute CLI command."""
    mock_client.json_to_pptx_execute_v2.return_value = "https://example.com/result.pptx"
    input_data = {
        "slides": [
            {
                "type": "title",
                "placeholders": [{"name": "title", "content": "Test Title"}],
            }
        ]
    }
    result = runner.invoke(
        cli, ["json-to-pptx-execute", "template-123"], input=json.dumps(input_data)
    )
    assert result.exit_code == 0
    assert "https://example.com/result.pptx" in result.output
    mock_client.json_to_pptx_execute_v2.assert_called_once()


def test_missing_api_key_cli(runner, mocker):
    """Test error handling when API key is missing."""
    mocker.patch(
        "middleman_ai.cli.main.get_api_key",
        side_effect=click.ClickException("API key not set"),
    )
    result = runner.invoke(cli, ["md-to-pdf"], input="# Test")
    assert result.exit_code != 0
    assert "API key not set" in result.output


def test_invalid_json_input_cli(runner, mock_client):
    """Test error handling for invalid JSON input."""
    result = runner.invoke(
        cli, ["json-to-pptx-execute", "template-123"], input="invalid json"
    )
    assert result.exit_code != 0
    assert "Invalid JSON input" in result.output


def test_pptx_to_page_images_cli(runner, mock_client, tmp_path) -> None:
    """Test pptx_to_page_images CLI command."""
    mock_client.pptx_to_page_images.return_value = [
        {"page_no": 1, "image_url": "https://example.com/slide1.png"},
        {"page_no": 2, "image_url": "https://example.com/slide2.png"},
    ]
    pptx_path = tmp_path / "test.pptx"
    pptx_path.write_bytes(b"dummy pptx content")
    result = runner.invoke(cli, ["pptx-to-page-images", str(pptx_path)])
    assert result.exit_code == 0
    assert "Page 1: https://example.com/slide1.png" in result.output
    assert "Page 2: https://example.com/slide2.png" in result.output
    mock_client.pptx_to_page_images.assert_called_once_with(str(pptx_path))


def test_docx_to_page_images_cli(runner, mock_client, tmp_path) -> None:
    """Test docx_to_page_images CLI command."""
    mock_client.docx_to_page_images.return_value = [
        {"page_no": 1, "image_url": "https://example.com/page1.png"},
        {"page_no": 2, "image_url": "https://example.com/page2.png"},
    ]
    docx_path = tmp_path / "test.docx"
    docx_path.write_bytes(b"dummy docx content")
    result = runner.invoke(cli, ["docx-to-page-images", str(docx_path)])
    assert result.exit_code == 0
    assert "Page 1: https://example.com/page1.png" in result.output
    assert "Page 2: https://example.com/page2.png" in result.output
    mock_client.docx_to_page_images.assert_called_once_with(str(docx_path))


def test_xlsx_to_page_images_cli(runner, mock_client, tmp_path) -> None:
    """Test xlsx_to_page_images CLI command."""
    mock_client.xlsx_to_page_images.return_value = [
        {"sheet_name": "Sheet1", "image_url": "https://example.com/sheet1.png"},
        {"sheet_name": "Sheet2", "image_url": "https://example.com/sheet2.png"},
    ]
    xlsx_path = tmp_path / "test.xlsx"
    xlsx_path.write_bytes(b"dummy xlsx content")
    result = runner.invoke(cli, ["xlsx-to-page-images", str(xlsx_path)])
    assert result.exit_code == 0
    assert "Sheet Sheet1: https://example.com/sheet1.png" in result.output
    assert "Sheet Sheet2: https://example.com/sheet2.png" in result.output
    mock_client.xlsx_to_page_images.assert_called_once_with(str(xlsx_path))


def test_mermaid_to_image_cli_without_options(runner, mock_client):
    """Test mermaid_to_image CLI command without options."""
    mock_client.mermaid_to_image.return_value = "https://example.com/mermaid.png"

    mermaid_input = """graph TD
    A[Start] --> B[Process]
    B --> C{Decision}
    C -->|Yes| D[End]
    C -->|No| B"""

    result = runner.invoke(cli, ["mermaid-to-image"], input=mermaid_input)
    assert result.exit_code == 0
    assert "https://example.com/mermaid.png" in result.output
    mock_client.mermaid_to_image.assert_called_once_with(mermaid_input, options=None)


def test_mermaid_to_image_cli_with_all_options(runner, mock_client):
    """Test mermaid_to_image CLI command with all options."""
    mock_client.mermaid_to_image.return_value = "https://example.com/mermaid.png"

    mermaid_input = "graph LR; A --> B"

    result = runner.invoke(
        cli,
        [
            "mermaid-to-image",
            "--theme",
            "forest",
            "--background-color",
            "transparent",
            "--width",
            "800",
            "--height",
            "600",
        ],
        input=mermaid_input,
    )
    assert result.exit_code == 0
    assert "https://example.com/mermaid.png" in result.output

    # options引数をチェック
    call_args = mock_client.mermaid_to_image.call_args
    assert call_args[0][0] == mermaid_input
    options = call_args[1]["options"]
    assert options is not None
    assert options.theme == "forest"
    assert options.background_color == "transparent"
    assert options.custom_size is not None
    assert options.custom_size.width == 800
    assert options.custom_size.height == 600


def test_mermaid_to_image_cli_with_theme_option(runner, mock_client):
    """Test mermaid_to_image CLI command with theme option."""
    mock_client.mermaid_to_image.return_value = "https://example.com/mermaid.png"

    mermaid_input = "graph LR; A --> B"

    result = runner.invoke(
        cli, ["mermaid-to-image", "--theme", "dark"], input=mermaid_input
    )
    assert result.exit_code == 0
    assert "https://example.com/mermaid.png" in result.output

    # options引数をチェック
    call_args = mock_client.mermaid_to_image.call_args
    assert call_args[0][0] == mermaid_input  # mermaid_text
    options = call_args[1]["options"]  # options keyword argument
    assert options is not None
    assert options.theme == "dark"
    assert options.background_color is None
    assert options.custom_size is None


def test_mermaid_to_image_cli_with_background_color_only(runner, mock_client):
    """Test mermaid_to_image CLI command with background-color option only."""
    mock_client.mermaid_to_image.return_value = "https://example.com/mermaid.png"

    mermaid_input = "graph LR; A --> B"

    result = runner.invoke(
        cli, ["mermaid-to-image", "--background-color", "#ff0000"], input=mermaid_input
    )
    assert result.exit_code == 0
    assert "https://example.com/mermaid.png" in result.output

    # options引数をチェック
    call_args = mock_client.mermaid_to_image.call_args
    assert call_args[0][0] == mermaid_input
    options = call_args[1]["options"]
    assert options is not None
    assert options.theme is None
    assert options.background_color == "#ff0000"
    assert options.custom_size is None


def test_mermaid_to_image_cli_with_width_height_only(runner, mock_client):
    """Test mermaid_to_image CLI command with width and height options only."""
    mock_client.mermaid_to_image.return_value = "https://example.com/mermaid.png"

    mermaid_input = "graph LR; A --> B"

    result = runner.invoke(
        cli,
        ["mermaid-to-image", "--width", "1000", "--height", "800"],
        input=mermaid_input,
    )
    assert result.exit_code == 0
    assert "https://example.com/mermaid.png" in result.output

    # options引数をチェック
    call_args = mock_client.mermaid_to_image.call_args
    assert call_args[0][0] == mermaid_input
    options = call_args[1]["options"]
    assert options is not None
    assert options.theme is None
    assert options.background_color is None
    assert options.custom_size is not None
    assert options.custom_size.width == 1000
    assert options.custom_size.height == 800


def test_mermaid_to_image_cli_width_height_validation(runner, mock_client):
    """Test mermaid_to_image CLI command width/height validation."""
    mermaid_input = "graph LR; A --> B"

    # width のみ指定(エラーになるべき)
    result = runner.invoke(
        cli, ["mermaid-to-image", "--width", "800"], input=mermaid_input
    )
    assert result.exit_code != 0
    assert "widthとheightは両方指定するか、両方省略してください" in result.output

    # height のみ指定(エラーになるべき)
    result = runner.invoke(
        cli, ["mermaid-to-image", "--height", "600"], input=mermaid_input
    )
    assert result.exit_code != 0
    assert "widthとheightは両方指定するか、両方省略してください" in result.output


def test_mermaid_to_image_cli_invalid_theme_choice(runner, mock_client):
    """Test mermaid_to_image CLI command with invalid theme choice."""
    mermaid_input = "graph LR; A --> B"

    result = runner.invoke(
        cli, ["mermaid-to-image", "--theme", "invalid"], input=mermaid_input
    )
    assert result.exit_code != 0
    assert "Invalid value for '--theme'" in result.output

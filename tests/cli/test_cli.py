"""Tests for the CLI implementation."""

import json
import os

import click

from middleman_ai.cli.main import cli

# Set dummy API key for tests
os.environ["MIDDLEMAN_API_KEY"] = "test-key"


def test_md_to_pdf(runner, mock_client):
    """Test md_to_pdf CLI command."""
    mock_client.md_to_pdf.return_value = "https://example.com/test.pdf"
    result = runner.invoke(cli, ["md-to-pdf"], input="# Test")
    assert result.exit_code == 0
    assert "https://example.com/test.pdf" in result.output
    mock_client.md_to_pdf.assert_called_once_with("# Test")


def test_md_to_docx(runner, mock_client):
    """Test md_to_docx CLI command."""
    mock_client.md_to_docx.return_value = "https://example.com/test.docx"
    result = runner.invoke(cli, ["md-to-docx"], input="# Test")
    assert result.exit_code == 0
    assert "https://example.com/test.docx" in result.output
    mock_client.md_to_docx.assert_called_once_with("# Test")


def test_md_to_pptx(runner, mock_client):
    """Test md_to_pptx CLI command."""
    mock_client.md_to_pptx.return_value = "https://example.com/test.pptx"
    result = runner.invoke(cli, ["md-to-pptx"], input="# Test")
    assert result.exit_code == 0
    assert "https://example.com/test.pptx" in result.output
    mock_client.md_to_pptx.assert_called_once_with("# Test")


def test_pdf_to_page_images(runner, mock_client, tmp_path):
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


def test_json_to_pptx_analyze(runner, mock_client):
    """Test json_to_pptx_analyze CLI command."""
    mock_client.json_to_pptx_analyze_v2.return_value = [
        {"type": "title", "placeholders": [{"name": "title", "content": ""}]}
    ]
    result = runner.invoke(cli, ["json-to-pptx-analyze", "template-123"])
    assert result.exit_code == 0
    assert "title" in result.output
    mock_client.json_to_pptx_analyze_v2.assert_called_once_with("template-123")


def test_json_to_pptx_execute(runner, mock_client):
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


def test_missing_api_key(runner, mocker):
    """Test error handling when API key is missing."""
    mocker.patch(
        "middleman_ai.cli.main.get_api_key",
        side_effect=click.ClickException("API key not set"),
    )
    result = runner.invoke(cli, ["md-to-pdf"], input="# Test")
    assert result.exit_code != 0
    assert "API key not set" in result.output


def test_invalid_json_input(runner, mock_client):
    """Test error handling for invalid JSON input."""
    result = runner.invoke(
        cli, ["json-to-pptx-execute", "template-123"], input="invalid json"
    )
    assert result.exit_code != 0
    assert "Invalid JSON input" in result.output

"""ToolsClientのテストモジュール。"""

from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest
import requests

from middleman_ai.client import (
    HTTP_FORBIDDEN,
    HTTP_INTERNAL_SERVER_ERROR,
    HTTP_NOT_FOUND,
    HTTP_PAYMENT_REQUIRED,
    HTTP_UNAUTHORIZED,
    ToolsClient,
)
from middleman_ai.exceptions import (
    ConnectionError,
    ForbiddenError,
    InternalError,
    NotEnoughCreditError,
    NotFoundError,
    ValidationError,
)
from middleman_ai.models import CustomSize, MermaidToImageOptions

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


@pytest.fixture
def client() -> ToolsClient:
    """テスト用のToolsClientインスタンスを生成します。"""
    return ToolsClient(api_key="test_api_key")


@pytest.fixture
def mock_response() -> Mock:
    """モックレスポンスを生成します。"""
    response = Mock(spec=requests.Response)
    response.status_code = 200
    response.json.return_value = {"pdf_url": "https://example.com/test.pdf"}
    return response


def test_init(client: ToolsClient) -> None:
    """初期化のテスト。"""
    assert client.api_key == "test_api_key"
    assert client.base_url == "https://middleman-ai.com"
    assert client.timeout == 30.0
    assert client.session.headers["Authorization"] == "Bearer test_api_key"
    assert client.session.headers["Content-Type"] == "application/json"


def test_md_to_pdf_success(
    client: ToolsClient, mocker: "MockerFixture", mock_response: Mock
) -> None:
    """md_to_pdf成功時のテスト。"""
    mock_post = mocker.patch.object(client.session, "post", return_value=mock_response)

    result = client.md_to_pdf("# Test")

    assert result == "https://example.com/test.pdf"
    mock_post.assert_called_once_with(
        "https://middleman-ai.com/api/v1/tools/md-to-pdf",
        json={"markdown": "# Test", "pdf_template_id": None},
        timeout=30.0,
    )


def test_md_to_pdf_success_with_template_id(
    client: ToolsClient, mocker: "MockerFixture", mock_response: Mock
) -> None:
    """md_to_pdf成功時のテスト。"""
    mock_post = mocker.patch.object(client.session, "post", return_value=mock_response)

    result = client.md_to_pdf(
        "# Test",
        pdf_template_id="00000000-0000-0000-0000-000000000001",
    )

    assert result == "https://example.com/test.pdf"
    mock_post.assert_called_once_with(
        "https://middleman-ai.com/api/v1/tools/md-to-pdf",
        json={
            "markdown": "# Test",
            "pdf_template_id": "00000000-0000-0000-0000-000000000001",
        },
        timeout=30.0,
    )


@pytest.mark.parametrize(
    "status_code,expected_exception",
    [
        (HTTP_PAYMENT_REQUIRED, NotEnoughCreditError),
        (HTTP_UNAUTHORIZED, ForbiddenError),
        (HTTP_FORBIDDEN, ForbiddenError),
        (HTTP_NOT_FOUND, NotFoundError),
        (HTTP_INTERNAL_SERVER_ERROR, InternalError),
    ],
)
def test_md_to_pdf_http_errors(
    client: ToolsClient,
    mocker: "MockerFixture",
    mock_response: Mock,
    status_code: int,
    expected_exception: type[Exception],
) -> None:
    """md_to_pdf HTTP エラー時のテスト。"""
    mock_response.status_code = status_code
    mock_response.url = "https://example.com/api/test"  # URLを追加
    mock_response.headers = {"content-type": "application/json"}  # headersを追加
    mock_response.text = ""  # textを追加
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
    mocker.patch.object(client.session, "post", return_value=mock_response)

    with pytest.raises(expected_exception):
        client.md_to_pdf("# Test")


def test_md_to_pdf_connection_error(
    client: ToolsClient, mocker: "MockerFixture"
) -> None:
    """md_to_pdf 接続エラー時のテスト。"""
    mocker.patch.object(
        client.session,
        "post",
        side_effect=requests.exceptions.RequestException(),
    )

    with pytest.raises(ConnectionError):
        try:
            client.md_to_pdf("# Test")
        except requests.exceptions.RequestException as e:
            raise ConnectionError() from e


def test_md_to_pdf_validation_error(
    client: ToolsClient, mocker: "MockerFixture", mock_response: Mock
) -> None:
    """md_to_pdf バリデーションエラー時のテスト。"""
    mock_response.json.return_value = {"invalid": "response"}
    mocker.patch.object(client.session, "post", return_value=mock_response)

    with pytest.raises(ValidationError):
        client.md_to_pdf("# Test")


def test_md_to_pdf_timeout_error(client: ToolsClient, mocker: "MockerFixture") -> None:
    """md_to_pdf タイムアウトエラー時のテスト。"""
    mocker.patch.object(
        client.session,
        "post",
        side_effect=requests.exceptions.Timeout("Connection timed out"),
    )

    with pytest.raises(ConnectionError):
        client.md_to_pdf("# Test")


def test_pptx_to_page_images_success(
    client: ToolsClient, mocker: "MockerFixture", mock_response: Mock
) -> None:
    """pptx_to_page_images成功時のテスト。"""
    mock_response.json.return_value = {
        "pages": [
            {"page_no": 1, "image_url": "https://example.com/page1.png"},
            {"page_no": 2, "image_url": "https://example.com/page2.png"},
        ]
    }
    mock_post = mocker.patch.object(requests, "post", return_value=mock_response)

    result = client.pptx_to_page_images("tests/data/test.pptx")

    assert len(result) == 2
    assert result[0]["page_no"] == 1
    assert result[0]["image_url"] == "https://example.com/page1.png"
    assert result[1]["page_no"] == 2
    assert result[1]["image_url"] == "https://example.com/page2.png"
    mock_post.assert_called_once()


def test_pptx_to_page_images_file_error(client: ToolsClient) -> None:
    """pptx_to_page_images ファイルエラー時のテスト。"""
    with pytest.raises(ValidationError, match="Failed to read PPTX file"):
        client.pptx_to_page_images("nonexistent.pptx")


def test_docx_to_page_images_success(
    client: ToolsClient, mocker: "MockerFixture", mock_response: Mock
) -> None:
    """docx_to_page_images成功時のテスト。"""
    mock_response.json.return_value = {
        "pages": [
            {"page_no": 1, "image_url": "https://example.com/page1.png"},
            {"page_no": 2, "image_url": "https://example.com/page2.png"},
        ]
    }
    mock_post = mocker.patch.object(requests, "post", return_value=mock_response)

    mocker.patch("os.path.isfile", return_value=True)

    mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data="test data"))

    result = client.docx_to_page_images("tests/data/test.docx")

    assert len(result) == 2
    assert result[0]["page_no"] == 1
    assert result[0]["image_url"] == "https://example.com/page1.png"
    assert result[1]["page_no"] == 2
    assert result[1]["image_url"] == "https://example.com/page2.png"
    mock_post.assert_called_once()
    mock_open.assert_called_once_with("tests/data/test.docx", "rb")


def test_docx_to_page_images_file_error(client: ToolsClient) -> None:
    """docx_to_page_images ファイルエラー時のテスト。"""
    with pytest.raises(ValidationError, match="Failed to read DOCX file"):
        client.docx_to_page_images("nonexistent.docx")


def test_xlsx_to_page_images_success(
    client: ToolsClient, mocker: "MockerFixture", mock_response: Mock
) -> None:
    """xlsx_to_page_images成功時のテスト。"""
    mock_response.json.return_value = {
        "pages": [
            {"sheet_name": "Sheet1", "image_url": "https://example.com/page1.png"},
            {"sheet_name": "Sheet2", "image_url": "https://example.com/page2.png"},
        ]
    }
    mock_post = mocker.patch.object(requests, "post", return_value=mock_response)

    result = client.xlsx_to_page_images("tests/data/test.xlsx")

    assert len(result) == 2
    assert result[0]["sheet_name"] == "Sheet1"
    assert result[0]["image_url"] == "https://example.com/page1.png"
    assert result[1]["sheet_name"] == "Sheet2"
    assert result[1]["image_url"] == "https://example.com/page2.png"
    mock_post.assert_called_once()


def test_xlsx_to_page_images_file_error(client: ToolsClient) -> None:
    """xlsx_to_page_images ファイルエラー時のテスト。"""
    with pytest.raises(ValidationError, match="Failed to read XLSX file"):
        client.xlsx_to_page_images("nonexistent.xlsx")


def test_mermaid_to_image_without_options(
    client: ToolsClient, mocker: "MockerFixture", mock_response: Mock
) -> None:
    """mermaid_to_image オプションなし成功時のテスト。"""
    mock_response.json.return_value = {
        "image_url": "https://example.com/mermaid.png",
        "format": "png",
        "important_remark_for_user": "The URL expires in 1 hour.",
    }
    mock_post = mocker.patch.object(client.session, "post", return_value=mock_response)

    result = client.mermaid_to_image("graph TD; A-->B")

    assert result == "https://example.com/mermaid.png"
    mock_post.assert_called_once_with(
        "https://middleman-ai.com/api/v1/tools/mermaid-to-image",
        json={
            "content": "graph TD; A-->B"
        },
        timeout=30.0,
    )


def test_mermaid_to_image_success_with_options(
    client: ToolsClient, mocker: "MockerFixture", mock_response: Mock
) -> None:
    """mermaid_to_image オプション付き成功時のテスト。"""

    mock_response.json.return_value = {
        "image_url": "https://example.com/mermaid.png",
        "format": "png",
        "important_remark_for_user": "The URL expires in 1 hour.",
    }
    mock_post = mocker.patch.object(client.session, "post", return_value=mock_response)

    options = MermaidToImageOptions(
        theme="dark",
        background_color="transparent",
        custom_size=CustomSize(width=800, height=600),
    )

    result = client.mermaid_to_image("graph LR; A-->B", options=options)

    assert result == "https://example.com/mermaid.png"
    mock_post.assert_called_once_with(
        "https://middleman-ai.com/api/v1/tools/mermaid-to-image",
        json={
            "content": "graph LR; A-->B",
            "options": {
                "theme": "dark",
                "background_color": "transparent",
                "custom_size": {"width": 800, "height": 600},
            },
        },
        timeout=30.0,
    )


@pytest.mark.parametrize(
    "status_code,expected_exception",
    [
        (HTTP_PAYMENT_REQUIRED, NotEnoughCreditError),
        (HTTP_UNAUTHORIZED, ForbiddenError),
        (HTTP_FORBIDDEN, ForbiddenError),
        (HTTP_NOT_FOUND, NotFoundError),
        (HTTP_INTERNAL_SERVER_ERROR, InternalError),
    ],
)
def test_mermaid_to_image_error_responses(
    client: ToolsClient,
    mocker: "MockerFixture",
    status_code: int,
    expected_exception: type,
) -> None:
    """mermaid_to_image エラーレスポンス時のテスト。"""
    mock_response = Mock(spec=requests.Response)
    mock_response.status_code = status_code
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
    mock_response.json.return_value = {}
    mock_response.url = "https://middleman-ai.com/api/v1/tools/mermaid-to-image"
    mock_response.headers = {}
    mock_response.text = ""

    mock_post = mocker.patch.object(client.session, "post", return_value=mock_response)

    with pytest.raises(expected_exception):
        client.mermaid_to_image("graph TD; A-->B")

    mock_post.assert_called_once()


def test_mermaid_to_image_connection_error(
    client: ToolsClient, mocker: "MockerFixture"
) -> None:
    """mermaid_to_image 接続エラー時のテスト。"""
    mock_post = mocker.patch.object(
        client.session, "post", side_effect=requests.exceptions.ConnectionError()
    )

    with pytest.raises(ConnectionError):
        client.mermaid_to_image("graph TD; A-->B")

    mock_post.assert_called_once()


def test_mermaid_to_image_validation_error(
    client: ToolsClient, mocker: "MockerFixture", mock_response: Mock
) -> None:
    """mermaid_to_image バリデーションエラー時のテスト。"""
    mock_response.json.return_value = {"invalid": "response"}
    mock_post = mocker.patch.object(client.session, "post", return_value=mock_response)

    with pytest.raises(ValidationError):
        client.mermaid_to_image("graph TD; A-->B")

    mock_post.assert_called_once()


def test_xlsx_to_pdf_analyze_success(
    client: ToolsClient, mocker: "MockerFixture", mock_response: Mock
) -> None:
    """xlsx_to_pdf_analyze 成功時のテスト。"""
    mock_response.json.return_value = {
        "sheet_name": "Sheet1",
        "placeholders": [
            {
                "key": "name",
                "description": "名前",
                "cell": "A1",
                "sheet_name": "Sheet1",
                "number_format": None,
            },
            {
                "key": "amount",
                "description": "金額",
                "cell": "B2",
                "sheet_name": "Sheet1",
                "number_format": "#,##0",
            },
        ],
        "placeholders_json_schema": '{"type": "object"}',
        "important_remark_for_user": "Use the JSON schema to understand the structure.",
    }
    mock_post = mocker.patch.object(client.session, "post", return_value=mock_response)

    result = client.xlsx_to_pdf_analyze("00000000-0000-0000-0000-000000000001")

    assert result.sheet_name == "Sheet1"
    assert len(result.placeholders) == 2
    assert result.placeholders[0].key == "name"
    assert result.placeholders[0].description == "名前"
    assert result.placeholders[0].cell == "A1"
    assert result.placeholders[1].key == "amount"
    assert result.placeholders[1].number_format == "#,##0"
    assert "type" in result.placeholders_json_schema
    mock_post.assert_called_once_with(
        "https://middleman-ai.com/api/v1/tools/xlsx-to-pdf-analyze",
        json={
            "xlsx_template_id": "00000000-0000-0000-0000-000000000001",
            "sheet_name": None,
        },
        timeout=30.0,
    )


def test_xlsx_to_pdf_analyze_with_sheet_name(
    client: ToolsClient, mocker: "MockerFixture", mock_response: Mock
) -> None:
    """xlsx_to_pdf_analyze シート名指定時のテスト。"""
    mock_response.json.return_value = {
        "sheet_name": "CustomSheet",
        "placeholders": [],
        "placeholders_json_schema": "{}",
    }
    mock_post = mocker.patch.object(client.session, "post", return_value=mock_response)

    result = client.xlsx_to_pdf_analyze(
        "00000000-0000-0000-0000-000000000001",
        sheet_name="CustomSheet",
    )

    assert result.sheet_name == "CustomSheet"
    mock_post.assert_called_once_with(
        "https://middleman-ai.com/api/v1/tools/xlsx-to-pdf-analyze",
        json={
            "xlsx_template_id": "00000000-0000-0000-0000-000000000001",
            "sheet_name": "CustomSheet",
        },
        timeout=30.0,
    )


@pytest.mark.parametrize(
    "status_code,expected_exception",
    [
        (HTTP_PAYMENT_REQUIRED, NotEnoughCreditError),
        (HTTP_UNAUTHORIZED, ForbiddenError),
        (HTTP_FORBIDDEN, ForbiddenError),
        (HTTP_NOT_FOUND, NotFoundError),
        (HTTP_INTERNAL_SERVER_ERROR, InternalError),
    ],
)
def test_xlsx_to_pdf_analyze_http_errors(
    client: ToolsClient,
    mocker: "MockerFixture",
    mock_response: Mock,
    status_code: int,
    expected_exception: type[Exception],
) -> None:
    """xlsx_to_pdf_analyze HTTP エラー時のテスト。"""
    mock_response.status_code = status_code
    mock_response.url = "https://middleman-ai.com/api/v1/tools/xlsx-to-pdf-analyze"
    mock_response.headers = {"content-type": "application/json"}
    mock_response.text = ""
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
    mocker.patch.object(client.session, "post", return_value=mock_response)

    with pytest.raises(expected_exception):
        client.xlsx_to_pdf_analyze("00000000-0000-0000-0000-000000000001")


def test_xlsx_to_pdf_analyze_validation_error(
    client: ToolsClient, mocker: "MockerFixture", mock_response: Mock
) -> None:
    """xlsx_to_pdf_analyze バリデーションエラー時のテスト。"""
    mock_response.json.return_value = {"invalid": "response"}
    mocker.patch.object(client.session, "post", return_value=mock_response)

    with pytest.raises(ValidationError):
        client.xlsx_to_pdf_analyze("00000000-0000-0000-0000-000000000001")


def test_xlsx_to_pdf_execute_success(
    client: ToolsClient, mocker: "MockerFixture", mock_response: Mock
) -> None:
    """xlsx_to_pdf_execute 成功時のテスト。"""
    mock_response.json.return_value = {
        "pdf_url": "https://example.com/output.pdf",
        "warnings": [],
        "important_remark_for_user": "The URL expires in 1 hour.",
    }
    mock_post = mocker.patch.object(client.session, "post", return_value=mock_response)

    result = client.xlsx_to_pdf_execute(
        "00000000-0000-0000-0000-000000000001",
        {"name": "テスト", "amount": "1000"},
    )

    assert result.pdf_url == "https://example.com/output.pdf"
    assert result.warnings == []
    mock_post.assert_called_once_with(
        "https://middleman-ai.com/api/v1/tools/xlsx-to-pdf-execute",
        json={
            "xlsx_template_id": "00000000-0000-0000-0000-000000000001",
            "placeholders": {"name": "テスト", "amount": "1000"},
            "sheet_name": None,
        },
        timeout=30.0,
    )


def test_xlsx_to_pdf_execute_with_warnings(
    client: ToolsClient, mocker: "MockerFixture", mock_response: Mock
) -> None:
    """xlsx_to_pdf_execute 警告付きの成功時のテスト。"""
    mock_response.json.return_value = {
        "pdf_url": "https://example.com/output.pdf",
        "warnings": ["Font 'MS Gothic' was replaced with 'Noto Sans CJK JP'"],
    }
    mock_post = mocker.patch.object(client.session, "post", return_value=mock_response)

    result = client.xlsx_to_pdf_execute(
        "00000000-0000-0000-0000-000000000001",
        {"name": "テスト"},
        sheet_name="Sheet2",
    )

    assert result.pdf_url == "https://example.com/output.pdf"
    assert len(result.warnings) == 1
    assert "Font" in result.warnings[0]
    mock_post.assert_called_once_with(
        "https://middleman-ai.com/api/v1/tools/xlsx-to-pdf-execute",
        json={
            "xlsx_template_id": "00000000-0000-0000-0000-000000000001",
            "placeholders": {"name": "テスト"},
            "sheet_name": "Sheet2",
        },
        timeout=30.0,
    )


@pytest.mark.parametrize(
    "status_code,expected_exception",
    [
        (HTTP_PAYMENT_REQUIRED, NotEnoughCreditError),
        (HTTP_UNAUTHORIZED, ForbiddenError),
        (HTTP_FORBIDDEN, ForbiddenError),
        (HTTP_NOT_FOUND, NotFoundError),
        (HTTP_INTERNAL_SERVER_ERROR, InternalError),
    ],
)
def test_xlsx_to_pdf_execute_http_errors(
    client: ToolsClient,
    mocker: "MockerFixture",
    mock_response: Mock,
    status_code: int,
    expected_exception: type[Exception],
) -> None:
    """xlsx_to_pdf_execute HTTP エラー時のテスト。"""
    mock_response.status_code = status_code
    mock_response.url = "https://middleman-ai.com/api/v1/tools/xlsx-to-pdf-execute"
    mock_response.headers = {"content-type": "application/json"}
    mock_response.text = ""
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
    mocker.patch.object(client.session, "post", return_value=mock_response)

    with pytest.raises(expected_exception):
        client.xlsx_to_pdf_execute(
            "00000000-0000-0000-0000-000000000001",
            {"name": "テスト"},
        )


def test_xlsx_to_pdf_execute_validation_error(
    client: ToolsClient, mocker: "MockerFixture", mock_response: Mock
) -> None:
    """xlsx_to_pdf_execute バリデーションエラー時のテスト。"""
    mock_response.json.return_value = {"invalid": "response"}
    mocker.patch.object(client.session, "post", return_value=mock_response)

    with pytest.raises(ValidationError):
        client.xlsx_to_pdf_execute(
            "00000000-0000-0000-0000-000000000001",
            {"name": "テスト"},
        )


def test_xlsx_to_pdf_execute_connection_error(
    client: ToolsClient, mocker: "MockerFixture"
) -> None:
    """xlsx_to_pdf_execute 接続エラー時のテスト。"""
    mocker.patch.object(
        client.session,
        "post",
        side_effect=requests.exceptions.ConnectionError(),
    )

    with pytest.raises(ConnectionError):
        client.xlsx_to_pdf_execute(
            "00000000-0000-0000-0000-000000000001",
            {"name": "テスト"},
        )


def test_xlsx_to_pdf_analyze_connection_error(
    client: ToolsClient, mocker: "MockerFixture"
) -> None:
    """xlsx_to_pdf_analyze 接続エラー時のテスト。"""
    mocker.patch.object(
        client.session,
        "post",
        side_effect=requests.exceptions.ConnectionError(),
    )

    with pytest.raises(ConnectionError):
        client.xlsx_to_pdf_analyze("00000000-0000-0000-0000-000000000001")

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
    assert client.timeout == 30.0  # noqa: PLR2004
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
        json={"markdown": "# Test"},
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

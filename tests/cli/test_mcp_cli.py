"""MCPサーバーCLIのテストモジュール。"""

from typing import TYPE_CHECKING

import pytest
from click.testing import CliRunner

from middleman_ai.cli.main import mcp_server as mcp_command
from middleman_ai.mcp import server as mcp_server

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


@pytest.fixture
def runner() -> CliRunner:
    """Click CLIランナーを生成します。"""
    return CliRunner()


def test_mcp_command(runner: CliRunner, mocker: "MockerFixture") -> None:
    """mcpコマンドのテスト。"""
    mock_run_server = mocker.patch.object(mcp_server, "run_server")

    mocker.patch("os.getenv", return_value="mock_api_key")

    result = runner.invoke(mcp_command)

    assert result.exit_code == 0, (
        f"予期しない終了コード: {result.exit_code}\nOutput:\n{result.output}"
    )

    assert "MCP server is running" in result.output

    mock_run_server.assert_called_once_with()

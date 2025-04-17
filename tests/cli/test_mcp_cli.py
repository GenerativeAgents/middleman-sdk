"""MCPサーバーCLIのテストモジュール。"""

from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest
from click.testing import CliRunner

from middleman_ai.cli.main import cli

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


@pytest.fixture
def runner():
    """Click CLIランナーを生成します。"""
    return CliRunner()


def test_mcp_command(runner, mocker: "MockerFixture"):
    """mcpコマンドのテスト。"""
    mock_run_server = mocker.patch("middleman_ai.cli.main.run_server")
    
    mocker.patch("os.getenv", return_value="mock_api_key")
    
    result = runner.invoke(cli, ["mcp", "server"])
    
    assert result.exit_code == 0
    
    assert "MCPサーバーを実行しています" in result.output
    
    mock_run_server.assert_called_once_with(transport="stdio")

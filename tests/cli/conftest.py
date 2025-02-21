"""Test configuration for CLI tests."""

import pytest
from click.testing import CliRunner
from pytest_mock import MockerFixture
from unittest.mock import Mock


@pytest.fixture
def runner() -> CliRunner:
    """Create a CLI runner."""
    return CliRunner()


@pytest.fixture
def mock_client(mocker: MockerFixture) -> Mock:
    """Create a mock client."""
    mock = Mock()
    mocker.patch("middleman_ai.cli.main.ToolsClient", return_value=mock)
    mocker.patch("middleman_ai.cli.main.get_api_key", return_value="test-key")
    return mock

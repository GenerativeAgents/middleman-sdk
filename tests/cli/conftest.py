"""Test configuration for CLI tests."""

from unittest.mock import Mock

import pytest


@pytest.fixture
def runner():
    """Create a CLI runner."""
    return pytest.CliRunner()


@pytest.fixture
def mock_client(mocker):
    """Create a mock client."""
    mock = Mock()
    mocker.patch("middleman_ai.cli.main.ToolsClient", return_value=mock)
    mocker.patch("middleman_ai.cli.main.get_api_key", return_value="test-key")
    return mock

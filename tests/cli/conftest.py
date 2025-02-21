"""Test configuration for CLI tests."""

from unittest.mock import Mock

import click.testing
import pytest
from pytest_mock import MockerFixture


@pytest.fixture
def runner() -> click.testing.CliRunner:
    """Create a CLI runner."""
    return click.testing.CliRunner()


@pytest.fixture
def mock_client(mocker: MockerFixture) -> Mock:
    """Create a mock client."""
    mock = Mock()
    mocker.patch("middleman_ai.cli.main.ToolsClient", return_value=mock)
    mocker.patch("middleman_ai.cli.main.get_api_key", return_value="test-key")
    return mock

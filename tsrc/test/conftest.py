""" Fixtures for tsrc testing. """

from pathlib import Path
from typing import Any, Iterator

import pytest
from cli_ui.tests import MessageRecorder

import tsrc

from .helpers.cli import tsrc_cli  # noqa
from .helpers.git_server import git_server  # noqa


@pytest.fixture()
def tmp_path(tmpdir: Any) -> Path:
    """Convert py.path.Local() to Path() objects."""
    return Path(tmpdir.strpath)


@pytest.fixture
def workspace_path(tmp_path: Path) -> Path:
    res = tmp_path / "work"
    res.mkdir()
    return res


@pytest.fixture
def workspace(workspace_path: Path) -> tsrc.Workspace:
    return tsrc.Workspace(workspace_path)


@pytest.fixture()
def message_recorder() -> Iterator[MessageRecorder]:
    res = MessageRecorder()
    res.start()
    yield res
    res.stop()

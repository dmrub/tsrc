from pathlib import Path
from typing import List, Optional, Tuple, cast  # noqa

import tsrc
import tsrc.manifest


class LocalManifest:
    """Represent a manifest repository that has been cloned locally
    inside `<workspace>/.tsrc/manifest`.

    Usage:

    >>> local_manifest = LocalManifest(Path(workspace / ".tsrc/manifest")

    # First, update the cloned repository using a remote git URL and a
    # branch:
    >>> manifest.update("git@acme.com/manifest.git", branch="devel")

    # Then, read the `manifest.yml` file from the clone repository:
    >>> manifest = local_manifest.get_manifest()

    """

    def __init__(
        self, clone_path: Path, manifest_filename="manifest.yml", remote_repo=True
    ) -> None:
        self.clone_path = clone_path
        self.manifest_filename = manifest_filename
        self.remote_repo = remote_repo

    def update(self, url: str, *, branch: str) -> None:
        if self.clone_path.exists():
            if self.remote_repo:
                self._reset_manifest_clone(url, branch=branch)
        else:
            self._clone_manifest(url, branch=branch)

    def get_manifest(self) -> tsrc.manifest.Manifest:
        return tsrc.manifest.load(self.clone_path / self.manifest_filename)

    def _reset_manifest_clone(self, url: str, *, branch: str) -> None:
        tsrc.git.run(self.clone_path, "remote", "set-url", "origin", url)

        tsrc.git.run(self.clone_path, "fetch")
        tsrc.git.run(self.clone_path, "checkout", "-B", branch)
        # fmt: off
        tsrc.git.run(
            self.clone_path, "branch", branch,
            "--set-upstream-to", f"origin/{branch}"
        )
        # fmt: on
        ref = f"origin/{branch}"
        tsrc.git.run(self.clone_path, "reset", "--hard", ref)

    def _clone_manifest(self, url: str, *, branch: str) -> None:
        parent = self.clone_path.parent
        name = self.clone_path.name
        parent.mkdir(parents=True, exist_ok=True)
        tsrc.git.run(self.clone_path.parent, "clone", url, "--branch", branch, name)

import subprocess
from pathlib import Path
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

import pytest


E2E_TESTS_PATH = Path(__file__).parent


def _run_semgrep(
    config: Optional[Union[str, Path]] = None,
    *,
    target_name: str = "basic",
    extra_options: Optional[List[Union[str, Path]]] = None,
    stderr: bool = False
) -> str:
    if extra_options is None:
        extra_options = []

    if config is not None:
        extra_options.extend(["--config", config])

    return subprocess.check_output(
        [
            "python",
            "-m",
            "semgrep",
            "--json",
            "--strict",
            *extra_options,
            Path("targets") / target_name,
        ],
        encoding="utf-8",
        stderr=subprocess.STDOUT if stderr else None,
    )


@pytest.fixture
def run_semgrep(monkeypatch, tmp_path):
    monkeypatch.setenv("PYTHONPATH", str(E2E_TESTS_PATH.parents[1].resolve()))

    (tmp_path / "targets").symlink_to(Path(E2E_TESTS_PATH / "targets").resolve())
    (tmp_path / "rules").symlink_to(Path(E2E_TESTS_PATH / "rules").resolve())

    monkeypatch.chdir(tmp_path)

    yield _run_semgrep

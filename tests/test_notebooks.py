"""Run the tutorial notebooks, in a temporary directory with a copy of the example inputs (their paths are relative to the repository root)."""

import shutil

import nbformat
import pytest
from nbclient import NotebookClient

from conftest import ROOT_DIR_PATH


@pytest.mark.parametrize("nb_path", sorted(ROOT_DIR_PATH.glob("*.ipynb")), ids=lambda p: p.name)
def test_notebook(nb_path, tmp_path):
    ## outputs (e.g. examples/outputs) are written in tmp_path, not in the repository
    shutil.copytree(ROOT_DIR_PATH / "examples" / "inputs", tmp_path / "examples" / "inputs")
    nb = nbformat.read(nb_path, as_version=4)
    NotebookClient(
        nb,
        timeout=600,
        kernel_name="python3",
        resources={"metadata": {"path": str(tmp_path)}},
    ).execute()

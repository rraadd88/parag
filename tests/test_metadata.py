import yaml

import parag

from conftest import ROOT_DIR_PATH


def test_citation_version():
    """The version in CITATION.cff matches the package version (see the release checklist in README.md)."""
    cff = yaml.safe_load(open(ROOT_DIR_PATH / "CITATION.cff"))
    assert str(cff["version"]).lstrip("v") == parag.__version__

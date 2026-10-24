from pathlib import Path

import pytest

ROOT_DIR_PATH = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def net_data():
    """Demo nodes and edges from the latent space of single-cell data (bundled with scanpy)."""
    import scanpy as sc

    from parag.core import get_net_data

    nodes, edges = get_net_data(sc.datasets.pbmc68k_reduced())
    return {"nodes": nodes, "edges": edges}


@pytest.fixture(scope="session")
def net_cols():
    return {
        "col_node_id": "cell id",
        "col_source": "cell id1",
        "col_target": "cell id2",
        "col_subset_id": "bulk_labels",
    }

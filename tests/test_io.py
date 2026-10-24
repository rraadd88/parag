import json

import networkx as nx
import numpy as np
import pandas as pd
import pytest
import xgi

from parag.io import from_hif, read_hif, to_hif, validate_hif, write_hif

from conftest import ROOT_DIR_PATH


@pytest.fixture(scope="module")
def communities():
    """Network communities (undirected)."""
    G = nx.karate_club_graph()
    nodes = (
        pd.Series({i: list(t) for i, t in enumerate(list(nx.community.girvan_newman(G))[3])})
        .explode()
        .to_frame("node id")
        .reset_index()
        .rename(columns={"index": "community id"})
        .astype({"node id": int})
        .loc[:, ["node id", "community id"]]
    )
    edges = pd.DataFrame(G.edges, columns=["source", "target"])
    return {"nodes": nodes, "edges": edges}


@pytest.mark.parametrize("mode", ["subsets", "pairwise"])
def test_round_trip(communities, mode):
    nodes, edges = communities["nodes"], communities["edges"]
    hif = to_hif(nodes, edges, "node id", "source", "target", "community id", mode=mode)
    assert validate_hif(hif)
    d = from_hif(json.loads(json.dumps(hif)))
    pd.testing.assert_frame_equal(d["nodes"], nodes, check_dtype=False)
    pd.testing.assert_frame_equal(d["edges"], edges, check_dtype=False)
    ## read by XGI
    H = xgi.convert.from_hif_dict(hif)
    assert H.num_nodes == len(nodes)
    assert H.num_edges == (nodes["community id"].nunique() if mode == "subsets" else len(edges))


def test_directed_file(tmp_path):
    """Directed pairwise edges (drug -> side effect), written to and read from a file."""
    edges = pd.read_csv(ROOT_DIR_PATH / "examples/inputs/ChSe-Decagon_monopharmacy.csv")
    nodes = pd.concat(
        [
            edges.loc[:, ["# STITCH"]].drop_duplicates().rename(columns={"# STITCH": "node id"}).assign(subset="drug"),
            edges.loc[:, ["Individual Side Effect", "Side Effect Name"]]
            .drop_duplicates(subset=["Individual Side Effect"])
            .rename(columns={"Individual Side Effect": "node id"})
            .assign(subset="side effect"),
        ],
        axis=0,
        ignore_index=True,
    )
    hif = to_hif(nodes, edges, "node id", "# STITCH", "Individual Side Effect", "subset", mode="pairwise", directed=True)
    d = from_hif(read_hif(write_hif(hif, f"{tmp_path}/drugs.json")))
    ## missing values are null in JSON, i.e. None after reading
    pd.testing.assert_frame_equal(d["nodes"].replace({None: np.nan}), nodes, check_dtype=False)
    pd.testing.assert_frame_equal(d["edges"], edges, check_dtype=False)
    assert type(xgi.convert.from_hif_dict(hif)).__name__ == "DiHypergraph"


def test_overlapping_membership():
    """A HIF written by another library (XGI), with nodes in multiple hyperedges."""
    hif = dict(xgi.convert.to_hif_dict(xgi.Hypergraph([[1, 2, 3], [3, 4], [4, 5, 6, 7]])))
    with pytest.raises(ValueError):
        from_hif(hif)
    d = from_hif(hif, subset_rule="largest")
    assert d["nodes"]["subset"].tolist() == [0, 0, 0, 2, 2, 2, 2]
    assert len(d["edges"]) == 3 + 1 + 6  # clique expansion
    assert from_hif(hif, subset_rule="first")["nodes"]["subset"].tolist() == [0, 0, 0, 1, 2, 2, 2]


def test_invalid():
    assert not validate_hif({"nodes": []}, errors="warn")


def test_input_errors(communities):
    with pytest.raises(ValueError):
        to_hif(**communities, col_node_id="node id", col_source="source", col_target="target", mode="subsets")
    with pytest.raises(KeyError):
        to_hif(**communities, col_node_id="missing", col_source="source", col_target="target", col_subset_id="community id")

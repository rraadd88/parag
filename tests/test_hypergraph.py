import numpy as np

from parag.hypergraph import get_degreeby_subset, plot_degreeby_subset, to_net


def test_get_degreeby_subset(net_data, net_cols):
    df = get_degreeby_subset(**net_data, **net_cols)
    ## fractions of the degrees by subsets
    assert np.allclose(df.set_index("source").sum(axis=1), 1)


def test_plot_degreeby_subset(net_data, net_cols):
    cfg, df = plot_degreeby_subset(
        net_data["nodes"].sort_values("bulk_labels"),
        net_data["edges"],
        **net_cols,
        plot=False,
    )
    assert len(cfg["data"][0]["values"]) == len(df)


def test_to_net(net_data, net_cols):
    cfg, df = to_net(**net_data, **net_cols, show_node_names=False)
    assert {"signals", "data", "marks", "scales"} <= set(cfg)

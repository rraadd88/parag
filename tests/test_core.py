def test_get_net_data(net_data):
    nodes, edges = net_data["nodes"], net_data["edges"]
    ## 5 cells per label
    assert (nodes.groupby("bulk_labels", observed=True).size() == 5).all()
    assert set(edges["cell id1"]) | set(edges["cell id2"]) <= set(nodes["cell id"])
    assert len(edges) > 0

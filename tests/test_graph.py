from parag.graph import to_net


def test_to_net(net_data, net_cols):
    cfg, nodes = to_net(
        **net_data,
        **net_cols,
        defaults=dict(radius=165, textSize=8, textOffset=7),
    )
    assert {"signals", "data", "marks"} <= set(cfg)
    assert nodes["name"].notna().any()

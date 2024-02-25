# AUTOGENERATED! DO NOT EDIT! File to edit: ../03_hypergraph.ipynb.

# %% auto 0
__all__ = ['get_degreeby_subset', 'plot_degreeby_subset', 'to_net']

# %% ../03_hypergraph.ipynb 3
import logging
import pandas as pd
from roux.lib.io import read_dict

def get_degreeby_subset(
    nodes: pd.DataFrame,
    edges: pd.DataFrame,
    col_node_id: str,
    col_source: str,
    col_target: str,
    col_subset_id: str,
) -> pd.DataFrame:
    """Get degrees by subsets (groups) of the source nodes

    Args:
        nodes (pd.DataFrame): nodes
        edges (pd.DataFrame): edges
        col_node_id (str): column with node ids
        col_source (str): column with source ids
        col_target (str): column with target ids
        col_subset_id (str): column with subset ids

    Returns:
        pd.DataFrame: table
    """
    import networkx as nx

    G = nx.from_pandas_edgelist(edges, col_source, col_target)

    return (
        nodes.loc[:, [col_node_id]]
        .rename(columns={col_node_id: "source"})
        .assign(
            **{
                "target": lambda df: df["source"].apply(
                    lambda x: list(G.neighbors(x)) if x in G.nodes else None
                )
            }
        )
        .explode("target")
        .log.dropna()
        .merge(
            right=nodes.loc[:, [col_node_id, col_subset_id]].rename(
                columns={col_node_id: "target"}
            ),
            on="target",
            how="left",
        )
        .groupby("source")[col_subset_id]
        .agg(lambda x: x.value_counts(normalize=True).to_dict())
        .apply(pd.Series)
        .fillna(0)
        .reset_index()
    )


def plot_degreeby_subset(
    nodes: pd.DataFrame,
    edges: pd.DataFrame,
    col_node_id: str,
    col_source: str,
    col_target: str,
    col_subset_id: str,
    order: list = None,
    hue_order: list = None,
    config_base_path: str = None,
    cmap_subsets: str = None,
    show_text: bool = True,
    plot: bool = True,
    **kws_display_plot,
) -> tuple:
    """Plot bar plot of degrees by subsets

    Args:
        nodes (pd.DataFrame): nodes
        edges (pd.DataFrame): edges
        col_node_id (str): column with node ids
        col_source (str): column with sources
        col_target (str): column with targets
        col_subset_id (str): column with subset ids
        order (list, optional): order of subsets. Defaults to None.
        hue_order (list, optional): order of colors. Defaults to None.
        config_base_path (str, optional): base vega config. Defaults to None.
        cmap_subsets (str, optional): colormap. Defaults to None.
        show_text (bool, optional): show text. Defaults to True.
        plot (bool, optional): plot or not. Defaults to True.

    Returns:
        tuple: vega config, degrees
    """
    degreebysubset = get_degreeby_subset(
        nodes,
        edges,
        col_node_id=col_node_id,
        col_source=col_source,
        col_target=col_target,
        col_subset_id=col_subset_id,
    )
    if order is not None:
        degreebysubset = degreebysubset.set_index("source").loc[order, :].reset_index()
    # degreebysubset.head(1)

    if config_base_path is None:
        from parag.utils import get_src_path

        config_base_path = f"{get_src_path()}/data/stacked_bars.json"
    cfg_bars = read_dict(config_base_path)

    ## data
    cfg_bars["data"][0]["values"] = list(degreebysubset.T.to_dict().values())

    # if cmap_subsets is None:
    #     import seaborn as sns # for the matching color palette
    #     cmap_subsets=sns.color_palette("colorblind")


    if hue_order is None:
        subsets = degreebysubset.set_index("source").columns.tolist()
    else:
        subsets = hue_order
    from parag.utils import get_colors

    to_subset_color = get_colors(
        subsets,
        cmap_subsets=cmap_subsets,
    )
    # to_subset_color=dict(zip(subsets,get_ncolors(len(subsets),cmap=cmap_subsets)))

    ## "fields"
    cfg_bars["data"][0]["transform"][0]["fields"] = degreebysubset.set_index(
        "source"
    ).columns.tolist()

    ## formula
    expr = (
        ",".join([f"if(datum.key==='{f}','{c}'" for f, c in to_subset_color.items()])
    ) + ",'#fff'"
    ## close brackets
    expr += ")" * (expr.count("(") - expr.count(")"))

    cfg_bars["data"][0]["transform"][1]["expr"] = expr

    # "if(datum.key==='CD4+/CD45RO+ Memory','green',if(datum.key==='CD4+/CD25 T Reg','#f0f','red'))"

    ## todo set the text
    if not show_text:
        cfg_bars["marks"] = cfg_bars["marks"][:1]
    if plot:
        from parag.utils import display_plot

        display_plot(cfg_bars.copy(), **kws_display_plot)
    return cfg_bars, degreebysubset


# parameters
def to_net(
    nodes: pd.DataFrame,
    edges: pd.DataFrame,
    col_node_id: str,
    col_source: str,
    col_target: str,
    col_subset_id: str,
    show_node_names: bool = True,
    defaults: dict = None,
    dbug: bool = False,
) -> tuple:
    """Plot interactive hypergraph 'representation'.

    Args:
        nodes (pd.DataFrame): nodes
        edges (pd.DataFrame): edges
        col_node_id (str): column with node ids
        col_source (str): column with sources
        col_target (str): column with targets
        col_subset_id (str): column with subset ids
        show_node_names (bool, optional): show node names. Defaults to True.
        defaults (dict, optional): defaults provided to the vega config. Defaults to None.
        dbug (bool, optional): debug mode. Defaults to False.

    Returns:
        tuple: vega config, degrees
    """
    from parag.graph import to_net

    # %run parag/graph.py
    cfg_base, df1 = to_net(
        nodes=nodes,
        edges=edges,
        col_node_id=col_node_id,
        col_source=col_source,
        col_target=col_target,
        col_subset_id=col_subset_id,
        plot=dbug,
        defaults=dict(
            radius=165,
            textSize=8,
            textOffset=7,
        ),
    )

    ## sorted bars
    cfg_bars, degreebysubset = plot_degreeby_subset(
        nodes,
        edges,
        col_node_id=col_node_id,
        col_source=col_source,
        col_target=col_target,
        col_subset_id=col_subset_id,
        config_base_path=None,
        cmap_subsets=None,
        plot=dbug,
        order=df1.log.query(expr="`parent`==3")["name"].tolist(),
        hue_order=df1[col_subset_id].dropna().unique(),
    )

    cfg_hyg = dict(zip(cfg_base.keys(), cfg_base.values()))

    cfg_hyg["scales"] = cfg_bars["scales"]

    cfg_hyg["signals"] += cfg_bars["signals"]
    cfg_hyg["data"] += cfg_bars["data"]
    cfg_hyg["marks"] += cfg_bars["marks"]

    ## removal of unsupported signals
    for i,d in enumerate(cfg_hyg['signals']):
        if d['name'] in ['rotate','startAngle','endAngle','extent',"layout"]:
            del cfg_hyg['signals'][i]['bind']
    
    ## aes
    if not show_node_names:
        for k in ["opacity", "fillOpacity", "strokeOpacity"]:
            cfg_hyg["marks"][0]["encode"]["enter"][k] = {"value": 0}
            cfg_hyg["marks"][0]["encode"]["update"][k] = {"value": 0}

    from parag.utils import display_plot
    
    try:
        display_plot(
            cfg_hyg.copy(),
            defaults=defaults,
        )
    except DisplayError:
        logging.error("plot not displayed, check the config.")
    return cfg_hyg, degreebysubset


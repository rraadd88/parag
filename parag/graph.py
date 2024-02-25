# AUTOGENERATED! DO NOT EDIT! File to edit: ../02_graph.ipynb.

# %% auto 0
__all__ = ['center_subset_label', 'get_preprocessed', 'to_net']

# %% ../02_graph.ipynb 3
import logging

logging.basicConfig(level=logging.INFO)
import pandas as pd
from roux.lib.io import read_dict, to_dict, read_ps, read_table, to_table
import roux.lib.df as rd  # noqa

from IPython.display import display
import pandas as pd

from roux.lib.str import linebreaker


def center_subset_label(
    ds1: pd.Series,
) -> pd.Series:
    """
    Removes the subset label except at the middle.
    """
    i = ds1.index.tolist()[len(ds1) // 2]
    # print(i,ds1.index)
    k = ds1.loc[i]
    ds1.loc[:] = ""
    ds1.loc[i] = linebreaker(k, 10)
    return ds1


def get_preprocessed(
    nodes: pd.DataFrame,
    edges: pd.DataFrame,
    col_node_id: str,
    col_node_name: str,
    col_subset_id: str,
    col_subset_name: str,
    _col_node_id: str,
    _col_node_name: str,
    _col_node_parent: str,
    _col_source: str,
    _col_target: str,
    _col_subset_name: str,
    col_source: str,
    col_target: str,
    remove_orphans: bool,
    testn: int = None,
    verbose: bool = False,
) -> tuple:
    """Get preprocessed nodes and edges

    Args:
        nodes (pd.DataFrame): node data
        edges (pd.DataFrame): edge data
        col_node_id (str): node id
        col_node_name (str): node name
        col_source (str): source column
        col_target (str): target column
        col_subset_id (str): subset id
        col_subset_name (str): subset name
        _col_node_id (str): vega node id
        _col_node_name (str): vega node name
        _col_node_parent (str): vega parent key
        _col_source (str): vega source key
        _col_target (str): vega source key
        _col_subset_name (str): vega subset name key
        remove_orphans (bool): remove orphan/unconnected nodes
        testn (int, optional): test n nodes. Defaults to None.
        verbose (bool, optional): verbose. Defaults to False.

    Returns:
        tuple: nodes, edges
    """
    df1 = nodes.loc[
        :, list(set([col_node_id, col_node_name, col_subset_id, col_subset_name]))
    ].log.drop_duplicates(
        subset=list(
            set(
                [
                    col_node_id,
                    col_node_name,
                    # col_node_parent,
                ]
            )
        ),
    )

    df2 = (
        edges.loc[:, [col_source, col_target]]
        .drop_duplicates()
        .rename(
            columns={
                col_source: _col_source,
                col_target: _col_target,
            },
        )
        .astype(
            {
                # _col_source: int,
                # _col_target: int,
            }
        )
    )
    if not testn is None:
        df1 = df1.head(testn)
        logging.warning(f"testing {testn} nodes")
    if verbose:
        print(df1.head())

    ## reset the node indexing
    ## need to start from 2
    nodes = df1[col_node_id].unique().tolist()
    if verbose:
        print(nodes)
    if remove_orphans:
        if verbose:
            print(len(nodes))
        nodes = [
            i
            for i in set(df2[_col_source].tolist() + df2[_col_target].tolist())
            if i in nodes
        ]
        if verbose:
            print(f"filtered by edges: {len(nodes)}")
        # df1=df1.log.query(expr=f"`{col_node_id}` in {nodes}")

    to_node_index = dict(zip(nodes, range(4, len(nodes) + 4)))

    df1 = (
        df1.assign(**{_col_node_id: lambda df: df[col_node_id].map(to_node_index)})
        .rename(
            columns={
                col_node_name: _col_node_name,
            },
        )
        .astype(
            {
                # _col_node_id: int,
                # _col_node_parent: int,
            }
        )
        # .astype(
        #     {
        #         _col_node_name: str,
        #     }
        # )
        # .sort_values(_col_node_name)
        # .rename(
        #     columns={
        #         col_node_id:_col_node_id,
        #         # col_node_parent:_col_node_parent,
        #     },
        #     errors='raise',
        # )
    )
    if verbose:
        print(
            df1.loc[
                :,
                list(
                    set([_col_node_id, _col_node_name, col_subset_id, col_subset_name])
                ),
            ]
        ).head()
        print(df1.columns.tolist())

    ## subsets
    df1 = df1.astype({col_subset_id: str})
    df1 = (
        df1.log.dropna(
            subset=list(
                set([_col_node_id, _col_node_name, col_subset_id, col_subset_name])
            )
        )
        # .sort_values([col_subset_name,_col_node_name])
        .groupby(
            col_subset_id,
            group_keys=False,
            sort=False,
        )
        .apply(
            lambda df: df.assign(
                **{
                    _col_subset_name: lambda df_: center_subset_label(
                        df_[col_subset_name].copy()
                    ),
                },
            )
        )
    )

    ## add the placeholder without parent
    df1_ = pd.DataFrame(
        {
            _col_node_id: [
                1,
                2,
                3,
            ],
            _col_node_name: [
                "1",
                "2",
                "3",
            ],
            _col_node_parent: [
                None,
                1,
                2,
            ],
        }
    )
    df1 = df1.assign(**{_col_node_parent: 3}).astype(
        {
            # _col_node_id: int,
            # _col_node_name: str,
            # _col_node_parent: int,
        }
    )
    df1 = pd.concat(
        [df1_, df1],
        axis=0,
    )

    if verbose:
        print(df1.iloc[5, :].T.to_dict())
    df1 = df1.fillna({_col_node_name: df1[_col_node_id].astype(int).astype(str)})

    if verbose:
        print(df1.head(1 if testn is None else testn))
        print(df1[_col_node_id].nunique())

    ## edges
    df2 = (
        df2
        # filter by nodes
        .log.query(expr=f"{_col_source} in {nodes} and {_col_target} in {nodes}")
        .assign(
            **{
                _col_source: lambda df: df[_col_source].map(to_node_index),
                _col_target: lambda df: df[_col_target].map(to_node_index),
            }
        )
        .rd.assert_no_na()
    )
    return df1, df2, to_node_index


def to_net(
    col_node_id: str,
    col_source: str,
    col_target: str,
    col_subset_id: str,
    # data
    nodes: pd.DataFrame = None,
    edges: pd.DataFrame = None,
    nodes_path: str = None,
    edges_path: str = None,
    # labels
    col_node_name: str = None,
    # col_node_parent='parent',
    col_subset_name: str = None,  #'gene set name',
    ## aes
    cmap_subsets=None,  # 'nipy_spectral'
    ## switches
    remove_orphans: bool = True,
    show_node_names: bool = True,
    ## knobs
    off_subset_name: int = 15,
    ## io
    config_base_path: str = None,  # 'inputs/edge_bundle.json',
    defaults: dict = None,
    use_urls: bool = False,
    out: str = None,
    plot: bool = True,
    ## etc
    testn: int = None,
    verbose: bool = False,
) -> tuple:
    """
    Plots the interactive pairwise graph.

    Args:
        nodes (pd.DataFrame): node data
        edges (pd.DataFrame): edge data
        col_node_id (str): node id
        col_node_name (str): node name
        col_source (str): source column
        col_target (str): target column
        col_subset_id (str): subset id
        col_subset_name (str): subset name
        nodes_path (str, optional): path to nodes file. Defaults to None.
        edges_path (str, optional): path to edges file. Defaults to None.
        cmap_subsets (_type_, optional): colormap. Defaults to None.
        show_node_names (bool, optional): show node names. Defaults to True.
        off_subset_name (int, optional): offset of the subset names from the node names. Defaults to 15.
        config_base_path (str, optional): vega config path. Defaults to None.
        defaults (dict, optional): default vega settings. Defaults to None.
        use_urls (bool, optional): use urls in the vega config. Defaults to False.
        out (str, optional): output format. Defaults to None.
        plot (bool, optional): plot or not. Defaults to True.
        testn (int, optional): test n nodes. Defaults to None.
        verbose (bool, optional): verbose. Defaults to False.

    Returns:
        tuple: vega config, nodes
    """
    _col_node_id = "id"
    _col_node_name = "name"
    _col_node_parent = "parent"
    _col_source = "source"
    _col_target = "target"
    _col_subset_name = "subset name"

    if config_base_path is None:
        from parag.utils import get_src_path

        config_base_path = f"{get_src_path()}/data/edge_bundle_subsets.json"
    d1 = read_dict(config_base_path)
    d1["marks"][1]["encode"]["update"]["dx"][
        "signal"
    ] = f"textOffset * (datum.leftside ? -{off_subset_name} : {off_subset_name})"

    ## nodes
    if col_node_name is None:
        col_node_name = col_node_id
        # _col_node_name=_col_node_id
    if col_subset_name is None:
        col_subset_name = col_subset_id
    if not nodes_path is None and not edges_path is None:
        df1 = pd.DataFrame(read_dict(nodes_path))
        df2 = pd.DataFrame(read_dict(edges_path))
    else:
        df1, df2, to_node_index = get_preprocessed(
            nodes,
            edges,
            col_node_id=col_node_id,
            col_node_name=col_node_name,
            col_subset_id=col_subset_id,
            col_subset_name=col_subset_name,
            _col_node_parent=_col_node_parent,
            _col_node_id=_col_node_id,
            _col_node_name=_col_node_name,
            col_source=col_source,
            col_target=col_target,
            _col_source=_col_source,
            _col_target=_col_target,
            _col_subset_name=_col_subset_name,
            testn=testn,
            verbose=verbose,
            remove_orphans=remove_orphans,
        )

    # ## reset the parent indexing
    # ## need to start from 1
    # parents=df1[_col_node_parent].unique().tolist()
    # to_parent_index=dict(zip(parents,range(4,len(parents)+4)))
    # df1[_col_node_parent]=df1[_col_node_parent].map(to_parent_index)
    # return df1
    ## color by subset
    from parag.utils import get_colors

    to_subset_color = get_colors(
        subsets=df1[col_subset_id].dropna().unique(),  # todo use hue_order
    )
    if verbose:
        print(to_subset_color)
    d1["marks"][0]["encode"]["update"]["fill"] = [
        {"test": f"datum.id === {str(int(k))}", "value": v}
        for k, v in df1.set_index(_col_node_id)[col_subset_id]
        .map(to_subset_color)
        .to_dict()
        .items()
    ] + d1["marks"][0]["encode"]["update"]["fill"]
    d1["marks"][1]["encode"]["update"]["fill"] = [
        {"test": f"datum.id === {str(int(k))}", "value": v}
        for k, v in df1.set_index(_col_node_id)[col_subset_id]
        .map(to_subset_color)
        .to_dict()
        .items()
    ] + d1["marks"][1]["encode"]["update"]["fill"]

    ### save
    # print(df1[_col_node_parent].value_counts().loc[[1,2]]==1)
    # d1['marks'][0]['encode']['update']['fill']
    ## remove other columns
    # df1=df1.loc[:,[_col_node_id,_col_node_name,
    #                 # col_node_parent,
    #                ]]
    assert all(df1[_col_node_parent].value_counts().loc[[1, 2]] == 1)
    assert df1[_col_node_parent].isnull().sum() == 1
    if verbose:
        print(df2.head(1 if testn is None else testn))
        print(len(df2))

    if use_urls:
        d1["data"][0]["url"] = to_dict(
            df1.T.apply(lambda x: x.dropna().to_dict()).tolist(),
            "vega/nodes.json",
        )

        d1["data"][-2]["url"] = to_dict(
            df2.T.apply(lambda x: x.dropna().to_dict()).tolist(),
            "vega/edges.json",
        )
    else:
        del d1["data"][0]["url"]
        d1["data"][0]["values"] = df1.T.apply(lambda x: x.dropna().to_dict()).tolist()

        del d1["data"][-2]["url"]
        d1["data"][-2]["values"] = df2.T.apply(lambda x: x.dropna().to_dict()).tolist()
    if not show_node_names:
        d1["marks"][0]["encode"]["update"]["fontSize"] = 0
    if plot:
        from parag.utils import display_plot

        display_plot(d1.copy(), defaults=defaults)
    if out is None:
        return d1, df1
    elif out == "cfg":
        return d1
    else:  # out=='df':
        return df1

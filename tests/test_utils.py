from pathlib import Path

from parag.utils import display_plot, get_colors, get_src_path


def test_get_src_path():
    assert (Path(get_src_path()) / "data" / "stacked_bars.json").exists()


def test_display_plot():
    display_plot(
        {
            "description": "A simple bar chart with embedded data.",
            "data": {"values": [{"a": "A", "b": 28}, {"a": "B", "b": 55}]},
            "mark": "bar",
            "encoding": {
                "x": {"field": "a", "type": "nominal"},
                "y": {"field": "b", "type": "quantitative"},
            },
        },
        method="vegalite",
    )


def test_get_colors():
    colors = get_colors(subsets=range(5), cmap_subsets=None, test=True)
    assert list(colors) == list(range(5))
    assert all(c.startswith("#") for c in colors.values())

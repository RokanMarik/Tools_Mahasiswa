import os
import tempfile
from journal_analyzer.core.visualizer import Visualizer


def test_create_bar_chart():
    with tempfile.TemporaryDirectory() as tmpdir:
        viz = Visualizer(output_dir=tmpdir)
        path = viz.create_bar_chart(
            title="Test Chart",
            labels=["A", "B", "C"],
            values=[10, 20, 15],
            filename="test_bar",
        )
        assert os.path.exists(path)
        assert path.endswith("test_bar.png")


def test_create_line_chart():
    with tempfile.TemporaryDirectory() as tmpdir:
        viz = Visualizer(output_dir=tmpdir)
        path = viz.create_line_chart(
            title="Trend",
            x_labels=["2020", "2021", "2022"],
            y_values=[5, 10, 15],
            filename="test_line",
        )
        assert os.path.exists(path)


def test_create_summary_visualization():
    with tempfile.TemporaryDirectory() as tmpdir:
        viz = Visualizer(output_dir=tmpdir)
        stats = {"mean": 75.3, "median": 78.0, "std": 12.1, "min": 45, "max": 98, "n": 200}
        path = viz.create_summary_visualization(stats, filename="test_summary")
        assert os.path.exists(path)

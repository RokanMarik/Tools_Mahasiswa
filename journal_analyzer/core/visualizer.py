import os


class Visualizer:
    """Generates matplotlib charts for data analysis results."""

    def __init__(self, output_dir: str = "output/visualizations"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def create_bar_chart(
        self,
        title: str,
        labels: list[str],
        values: list[float],
        filename: str = "bar_chart",
        xlabel: str = "",
        ylabel: str = "Nilai",
    ) -> str:
        """Create a bar chart and save to file."""
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(labels, values, color="steelblue")
        ax.set_title(title)
        if xlabel:
            ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.tight_layout()

        path = os.path.join(self.output_dir, f"{filename}.png")
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path

    def create_line_chart(
        self,
        title: str,
        x_labels: list[str],
        y_values: list[float],
        filename: str = "line_chart",
        xlabel: str = "",
        ylabel: str = "Nilai",
    ) -> str:
        """Create a line chart and save to file."""
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x_labels, y_values, marker="o", linewidth=2, markersize=8)
        ax.set_title(title)
        if xlabel:
            ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()

        path = os.path.join(self.output_dir, f"{filename}.png")
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path

    def create_summary_visualization(
        self,
        stats: dict,
        filename: str = "summary",
    ) -> str:
        """Create a summary visualization showing key statistics."""
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.axis("off")

        lines = ["Statistik Deskriptif", ""]
        lines.append(f"N = {stats.get('n', 'N/A')}")
        lines.append(f"Mean = {stats.get('mean', 'N/A')}")
        lines.append(f"Median = {stats.get('median', 'N/A')}")
        lines.append(f"Std Dev = {stats.get('std', 'N/A')}")
        lines.append(f"Min = {stats.get('min', 'N/A')}")
        lines.append(f"Max = {stats.get('max', 'N/A')}")

        ax.text(0.5, 0.5, "\n".join(lines), ha="center", va="center",
                fontsize=14, family="monospace",
                bbox=dict(boxstyle="round,pad=1", facecolor="lightblue", alpha=0.5))

        path = os.path.join(self.output_dir, f"{filename}.png")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return path

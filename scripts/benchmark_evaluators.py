"""Benchmark des fonctions d'evaluation et de l'alpha-beta.

Le script mesure, pour le plateau initial, le score, le temps et le nombre
de noeuds explores pour chaque evaluateur et pour plusieurs profondeurs.

"""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from time import perf_counter


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ai.evaluators import AdvancedEvaluator, MaterialEvaluator, MobilityEvaluator
from ai.search import SearchStats, alphabeta
from models.board import Board


OUTPUT_DIR = ROOT_DIR / "docs" / "benchmarks"
DEFAULT_DEPTHS = (1,  3,  5)


def run_benchmark(depths: tuple[int, ...] = DEFAULT_DEPTHS) -> list[dict[str, object]]:
    evaluators = [
        MaterialEvaluator(),
        MobilityEvaluator(),
        AdvancedEvaluator(),
    ]

    rows: list[dict[str, object]] = []
    for evaluator in evaluators:
        for depth in depths:
            board = Board.initial_board()
            stats = SearchStats()
            start = perf_counter()
            score, _ = alphabeta(
                board,
                depth,
                float("-inf"),
                float("inf"),
                True,
                evaluator,
                stats,
                move_ordering=True,
            )
            elapsed = perf_counter() - start
            rows.append(
                {
                    "evaluator": evaluator.get_name(),
                    "depth": depth,
                    "score": round(score, 3),
                    "nodes_explored": stats.nodes_explored,
                    "time_seconds": round(elapsed, 4),
                }
            )

    return rows


def write_csv(rows: list[dict[str, object]]) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "evaluator_benchmark.csv"

    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=["evaluator", "depth", "score", "nodes_explored", "time_seconds"],
        )
        writer.writeheader()
        writer.writerows(rows)

    return output_path


def print_markdown_table(rows: list[dict[str, object]]) -> None:
    print("| Evaluateur | Profondeur | Score | Noeuds | Temps (s) |")
    print("|---|---:|---:|---:|---:|")
    for row in rows:
        print(
            f"| {row['evaluator']} | {row['depth']} | {row['score']} | "
            f"{row['nodes_explored']} | {row['time_seconds']} |"
        )


def try_generate_figures(rows: list[dict[str, object]]) -> list[Path]:
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return []

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    grouped: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        grouped.setdefault(str(row["evaluator"]), []).append(row)

    figure_paths: list[Path] = []
    palette = {
        "Material": "#1f77b4",
        "Material+Mobility": "#ff7f0e",
        "Advanced": "#2ca02c",
    }

    for metric, filename, ylabel in (
        ("time_seconds", "benchmark_time.png", "Temps (s)"),
        ("nodes_explored", "benchmark_nodes.png", "Noeuds explores"),
        ("score", "benchmark_score.png", "Score"),
    ):
        plt.figure(figsize=(9, 5))
        for evaluator_name, evaluator_rows in grouped.items():
            evaluator_rows = sorted(evaluator_rows, key=lambda item: int(item["depth"]))
            depths = [int(item["depth"]) for item in evaluator_rows]
            values = [float(item[metric]) for item in evaluator_rows]
            plt.plot(depths, values, marker="o", label=evaluator_name)

        plt.title(f"Evolution de {ylabel.lower()} selon la profondeur")
        plt.xlabel("Profondeur")
        plt.ylabel(ylabel)
        plt.grid(True, alpha=0.3)
        plt.legend()
        output_path = OUTPUT_DIR / filename
        plt.tight_layout()
        plt.savefig(output_path, dpi=160)
        plt.close()
        figure_paths.append(output_path)

    try:
        plt.style.use("seaborn-v0_8-whitegrid")
    except Exception:
        pass

    dashboard_path = OUTPUT_DIR / "benchmark_dashboard.png"
    fig, axes = plt.subplots(1, 3, figsize=(18, 5), constrained_layout=True)
    fig.suptitle("Comparaison des fonctions d'evaluation", fontsize=16, fontweight="bold")

    for evaluator_name, evaluator_rows in grouped.items():
        evaluator_rows = sorted(evaluator_rows, key=lambda item: int(item["depth"]))
        depths = [int(item["depth"]) for item in evaluator_rows]
        color = palette.get(evaluator_name, None)

        axes[0].plot(
            depths,
            [float(item["time_seconds"]) for item in evaluator_rows],
            marker="o",
            linewidth=2.4,
            markersize=7,
            label=evaluator_name,
            color=color,
        )
        axes[1].plot(
            depths,
            [int(item["nodes_explored"]) for item in evaluator_rows],
            marker="o",
            linewidth=2.4,
            markersize=7,
            label=evaluator_name,
            color=color,
        )
        axes[2].plot(
            depths,
            [float(item["score"]) for item in evaluator_rows],
            marker="o",
            linewidth=2.4,
            markersize=7,
            label=evaluator_name,
            color=color,
        )

    chart_specs = [
        (axes[0], "Temps de calcul", "Profondeur", "Temps (s)"),
        (axes[1], "Noeuds explores", "Profondeur", "Noeuds"),
        (axes[2], "Score retourne", "Profondeur", "Score"),
    ]

    for axis, title, xlabel, ylabel in chart_specs:
        axis.set_title(title, fontweight="bold")
        axis.set_xlabel(xlabel)
        axis.set_ylabel(ylabel)
        axis.set_xticks(sorted({int(row["depth"]) for row in rows}))
        axis.grid(True, alpha=0.25)

    axes[0].legend(loc="upper left", frameon=True)
    axes[2].axhline(0, color="#666666", linewidth=1, linestyle="--", alpha=0.7)

    for axis in axes:
        for line in axis.lines:
            x_data = line.get_xdata()
            y_data = line.get_ydata()
            if len(x_data) == len(y_data):
                for x_value, y_value in zip(x_data, y_data):
                    label = f"{y_value:.2f}" if isinstance(y_value, float) else str(y_value)
                    axis.annotate(
                        label,
                        (x_value, y_value),
                        textcoords="offset points",
                        xytext=(0, 8),
                        ha="center",
                        fontsize=8,
                        alpha=0.85,
                    )

    fig.patch.set_facecolor("#f8f9fb")
    for axis in axes:
        axis.set_facecolor("#ffffff")

    fig.savefig(dashboard_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    figure_paths.append(dashboard_path)

    return figure_paths


def main() -> None:
    rows = run_benchmark()
    csv_path = write_csv(rows)
    print(f"CSV genere: {csv_path}")
    print_markdown_table(rows)

    figure_paths = try_generate_figures(rows)
    if figure_paths:
        for figure_path in figure_paths:
            print(f"Figure generee: {figure_path}")
    else:
        print("Matplotlib indisponible: figures non generees.")


if __name__ == "__main__":
    main()
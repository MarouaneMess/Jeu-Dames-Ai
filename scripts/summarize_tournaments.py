"""Resume des resultats de tournoi a partir de tournaments/tournament_summary.csv.

Le script regroupe les parties par couple de niveaux et calcule les moyennes,
les taux de victoire et le temps moyen.

Usage:
    python scripts/summarize_tournaments.py
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
TOURNAMENT_CSV = ROOT_DIR / "tournaments" / "tournament_summary.csv"
OUTPUT_DIR = ROOT_DIR / "docs" / "benchmarks"


def load_rows() -> list[dict[str, str]]:
    with TOURNAMENT_CSV.open("r", encoding="utf-8", newline="") as csvfile:
        return list(csv.DictReader(csvfile))


def summarize(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    buckets: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        buckets[(row["white_level"], row["black_level"])].append(row)

    summary_rows: list[dict[str, object]] = []
    for (white_level, black_level), items in sorted(buckets.items()):
        total = len(items)
        white_wins = sum(int(item["white_wins"]) for item in items)
        black_wins = sum(int(item["black_wins"]) for item in items)
        draws = sum(int(item["draws"]) for item in items)
        avg_time = sum(float(item["time_seconds"]) for item in items) / total

        summary_rows.append(
            {
                "white_level": white_level,
                "black_level": black_level,
                "matches": total,
                "white_wins_avg": round(white_wins / total, 2),
                "black_wins_avg": round(black_wins / total, 2),
                "draws_avg": round(draws / total, 2),
                "white_win_rate": round(white_wins / (total * 50) * 100, 1),
                "black_win_rate": round(black_wins / (total * 50) * 100, 1),
                "draw_rate": round(draws / (total * 50) * 100, 1),
                "avg_time_seconds": round(avg_time, 2),
            }
        )

    return summary_rows


def write_markdown(summary_rows: list[dict[str, object]]) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "tournament_summary.md"

    lines = [
        "# Resume des tournois",
        "",
        "| Blanc | Noir | Lots | Victoires blanches moy. | Victoires noires moy. | Nuls moy. | Taux blanc | Taux noir | Taux nul | Temps moyen (s) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for row in summary_rows:
        lines.append(
            f"| {row['white_level']} | {row['black_level']} | {row['matches']} | "
            f"{row['white_wins_avg']} | {row['black_wins_avg']} | {row['draws_avg']} | "
            f"{row['white_win_rate']}% | {row['black_win_rate']}% | {row['draw_rate']}% | {row['avg_time_seconds']} |"
        )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


def try_generate_victory_graph(summary_rows: list[dict[str, object]]) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return None

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "tournament_dashboard.png"

    ordered_rows = sorted(
        summary_rows,
        key=lambda row: (
            -float(row["white_win_rate"]),
            -float(row["matches"]),
            str(row["white_level"]),
            str(row["black_level"]),
        ),
    )

    labels = [f"{row['white_level']} vs {row['black_level']}" for row in ordered_rows]
    white_wins = [int(round(float(row["white_wins_avg"]) * int(row["matches"]))) for row in ordered_rows]
    black_wins = [int(round(float(row["black_wins_avg"]) * int(row["matches"]))) for row in ordered_rows]
    draws = [int(round(float(row["draws_avg"]) * int(row["matches"]))) for row in ordered_rows]

    y_positions = list(range(len(summary_rows)))
    plt.style.use("seaborn-v0_8-whitegrid")

    fig, ax_left = plt.subplots(1, 1, figsize=(12, 8))
    fig.patch.set_facecolor("#f6f7fb")
    ax_left.set_facecolor("#ffffff")

    ax_left.barh(y_positions, white_wins, color="#4C78A8", label="Blanc")
    ax_left.barh(y_positions, black_wins, left=white_wins, color="#F58518", label="Noir")
    left_draws = [w + b for w, b in zip(white_wins, black_wins)]
    ax_left.barh(y_positions, draws, left=left_draws, color="#54A24B", label="Nuls")

    ax_left.set_yticks(y_positions)
    ax_left.set_yticklabels(labels)
    ax_left.invert_yaxis()
    ax_left.set_xlabel("Nombre de parties")
    ax_left.set_title("Résultats par couple d'IA", fontweight="bold")
    ax_left.grid(axis="x", alpha=0.22)
    ax_left.legend(loc="lower right", frameon=True)

    for index, row in enumerate(ordered_rows):
        white_rate = float(row["white_win_rate"])
        black_rate = float(row["black_win_rate"])
        draw_rate = float(row["draw_rate"])
        ax_left.text(
            white_wins[index] / 2,
            index,
            f"{white_rate:.1f}%",
            va="center",
            ha="center",
            color="white",
            fontsize=9,
            fontweight="bold",
        )
        ax_left.text(
            white_wins[index] + black_wins[index] / 2,
            index,
            f"{black_rate:.1f}%",
            va="center",
            ha="center",
            color="white",
            fontsize=9,
            fontweight="bold",
        )
        ax_left.text(
            white_wins[index] + black_wins[index] + draws[index] / 2,
            index,
            f"{draw_rate:.1f}%",
            va="center",
            ha="center",
            color="white",
            fontsize=9,
            fontweight="bold",
        )

    fig.suptitle("Tournois entre intelligences artificielles", fontsize=18, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)

    return output_path


def main() -> None:
    rows = load_rows()
    summary_rows = summarize(rows)
    output_path = write_markdown(summary_rows)
    print(f"Resume genere: {output_path}")

    graph_path = try_generate_victory_graph(summary_rows)
    if graph_path is not None:
        print(f"Graphique genere: {graph_path}")

    print("| Blanc | Noir | Lots | Victoires blanches moy. | Victoires noires moy. | Nuls moy. | Taux blanc | Taux noir | Taux nul | Temps moyen (s) |")
    print("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for row in summary_rows:
        print(
            f"| {row['white_level']} | {row['black_level']} | {row['matches']} | "
            f"{row['white_wins_avg']} | {row['black_wins_avg']} | {row['draws_avg']} | "
            f"{row['white_win_rate']}% | {row['black_win_rate']}% | {row['draw_rate']}% | {row['avg_time_seconds']} |"
        )


if __name__ == "__main__":
    main()
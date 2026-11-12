"""
dfa_visualizer.py
Module for generating graphical DFA state transition diagrams and transition tables.
Uses Matplotlib to render high-resolution academic diagrams for Pattern 1 ("com*").
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd


def get_dfa_transition_table_df() -> pd.DataFrame:
    """Returns the formal DFA State Transition Table as a pandas DataFrame."""
    data = [
        {
            "State": "→ q0 (Initial)",
            "Input 'c, C'": "q1",
            "Input 'o, O'": "qd",
            "Input 'm, M'": "qd",
            "Other ASCII Letters": "qd",
            "Description": "Initial state; awaiting word start"
        },
        {
            "State": "q1",
            "Input 'c, C'": "qd",
            "Input 'o, O'": "q2",
            "Input 'm, M'": "qd",
            "Other ASCII Letters": "qd",
            "Description": "Prefix 'c' verified"
        },
        {
            "State": "q2",
            "Input 'c, C'": "qd",
            "Input 'o, O'": "qd",
            "Input 'm, M'": "q3",
            "Other ASCII Letters": "qd",
            "Description": "Prefix 'co' verified"
        },
        {
            "State": "* q3 (Accepting)",
            "Input 'c, C'": "q3",
            "Input 'o, O'": "q3",
            "Input 'm, M'": "q3",
            "Other ASCII Letters": "q3",
            "Description": "Prefix 'com' matched; accepts any remaining letters"
        },
        {
            "State": "qd (Dead State)",
            "Input 'c, C'": "qd",
            "Input 'o, O'": "qd",
            "Input 'm, M'": "qd",
            "Other ASCII Letters": "qd",
            "Description": "Rejection trap state; self-loops until word boundary"
        }
    ]
    df = pd.DataFrame(data)
    return df


def draw_dfa_diagram(output_path: str = "outputs/dfa_diagram.png", show_title: bool = True):
    """
    Renders a publication-grade state transition diagram for the 5-state DFA.
    Exports the diagram to the specified output PNG path and returns the matplotlib Figure.
    """
    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(-0.5, 5.0)
    ax.axis("off")

    # State coordinates
    coords = {
        "q0": (1.2, 3.2),
        "q1": (3.4, 3.2),
        "q2": (5.6, 3.2),
        "q3": (7.8, 3.2),
        "qd": (4.5, 1.0)
    }

    radius = 0.42

    # Draw states
    for state, (x, y) in coords.items():
        if state == "q3":
            # Accepting state: Double circle with green accent
            outer = patches.Circle((x, y), radius, facecolor="#E8F8F5", edgecolor="#1E8449", linewidth=2.5, zorder=3)
            inner = patches.Circle((x, y), radius - 0.08, facecolor="none", edgecolor="#1E8449", linewidth=1.5, zorder=3)
            ax.add_patch(outer)
            ax.add_patch(inner)
            ax.text(x, y, state, ha="center", va="center", fontsize=15, fontweight="bold", color="#145A32", zorder=4)
        elif state == "qd":
            # Dead/trap state: Reddish hue
            circle = patches.Circle((x, y), radius, facecolor="#FDEDEC", edgecolor="#C0392B", linewidth=2.0, zorder=3)
            ax.add_patch(circle)
            ax.text(x, y, state, ha="center", va="center", fontsize=15, fontweight="bold", color="#922B21", zorder=4)
        else:
            # Regular states: Clean blue accent
            circle = patches.Circle((x, y), radius, facecolor="#EBF5FB", edgecolor="#2980B9", linewidth=2.0, zorder=3)
            ax.add_patch(circle)
            ax.text(x, y, state, ha="center", va="center", fontsize=15, fontweight="bold", color="#1B4F72", zorder=4)

    # 1. Start arrow pointing to q0
    ax.annotate(
        "",
        xy=(coords["q0"][0] - radius, coords["q0"][1]),
        xytext=(0.1, coords["q0"][1]),
        arrowprops=dict(arrowstyle="-|>", color="#1B4F72", lw=2.2, mutation_scale=18),
        zorder=2
    )
    ax.text(0.4, coords["q0"][1] + 0.18, "Start", fontsize=11, fontweight="bold", color="#1B4F72")

    # 2. Main forward transitions: q0 -> q1 -> q2 -> q3
    def draw_straight_transition(s_from, s_to, label):
        x1, y1 = coords[s_from]
        x2, y2 = coords[s_to]
        ax.annotate(
            "",
            xy=(x2 - radius, y2),
            xytext=(x1 + radius, y1),
            arrowprops=dict(arrowstyle="-|>", color="#2980B9", lw=2.0, mutation_scale=16),
            zorder=2
        )
        mid_x = (x1 + x2) / 2.0
        ax.text(mid_x, y1 + 0.18, label, ha="center", va="bottom", fontsize=11, fontweight="bold", color="#154360")

    draw_straight_transition("q0", "q1", "c, C")
    draw_straight_transition("q1", "q2", "o, O")
    draw_straight_transition("q2", "q3", "m, M")

    # 3. Accepting state q3 self-loop on any ASCII letter
    x3, y3 = coords["q3"]
    # Top self-loop arc
    arc_q3 = patches.Arc(
        (x3, y3 + 0.45),
        width=0.7,
        height=0.6,
        angle=0,
        theta1=0,
        theta2=280,
        edgecolor="#1E8449",
        linewidth=2.0,
        zorder=2
    )
    ax.add_patch(arc_q3)
    ax.annotate(
        "",
        xy=(x3 + 0.15, y3 + radius + 0.05),
        xytext=(x3 + 0.22, y3 + radius + 0.22),
        arrowprops=dict(arrowstyle="-|>", color="#1E8449", lw=1.8, mutation_scale=14),
        zorder=2
    )
    ax.text(x3, y3 + 0.88, "[A-Za-z]", ha="center", va="bottom", fontsize=10, fontweight="bold", color="#1E8449")

    # 4. Dead state qd self-loop on any ASCII letter
    xd, yd = coords["qd"]
    arc_qd = patches.Arc(
        (xd, yd - 0.45),
        width=0.7,
        height=0.6,
        angle=0,
        theta1=160,
        theta2=440,
        edgecolor="#C0392B",
        linewidth=2.0,
        zorder=2
    )
    ax.add_patch(arc_qd)
    ax.annotate(
        "",
        xy=(xd + 0.15, yd - radius - 0.05),
        xytext=(xd + 0.22, yd - radius - 0.22),
        arrowprops=dict(arrowstyle="-|>", color="#C0392B", lw=1.8, mutation_scale=14),
        zorder=2
    )
    ax.text(xd, yd - 0.95, "[A-Za-z]", ha="center", va="top", fontsize=10, fontweight="bold", color="#C0392B")

    # 5. Transitions to Dead State qd from q0, q1, q2
    def draw_curve_to_dead(s_from, label, rad_val, text_offset):
        xf, yf = coords[s_from]
        xt, yt = coords["qd"]
        ax.annotate(
            "",
            xy=(xt - 0.2 + (0.15 if s_from == "q2" else (-0.15 if s_from == "q0" else 0)), yt + radius),
            xytext=(xf, yf - radius),
            arrowprops=dict(
                arrowstyle="-|>",
                color="#C0392B",
                lw=1.6,
                mutation_scale=14,
                linestyle="--",
                connectionstyle=f"arc3,rad={rad_val}"
            ),
            zorder=2
        )
        tx, ty = (xf + xt) / 2 + text_offset[0], (yf + yt) / 2 + text_offset[1]
        ax.text(tx, ty, label, fontsize=9, fontweight="bold", color="#922B21", ha="center")

    draw_curve_to_dead("q0", "other letter", 0.18, (-0.45, -0.2))
    draw_curve_to_dead("q1", "other letter", 0.05, (-0.25, 0.1))
    draw_curve_to_dead("q2", "other letter", -0.15, (0.45, -0.15))

    # Legend / Annotation Box
    legend_text = (
        "DFA Definition: M = (Q, Σ, δ, q0, F)\n"
        "• Q = {q0, q1, q2, q3, qd}\n"
        "• Σ = {A-Z, a-z} (ASCII Case-Insensitive)\n"
        "• Initial State: q0 (Start)\n"
        "• Accepting State: F = {q3} (Double Circle)\n"
        "• Dead/Rejection State: qd (Dashed Lines)"
    )
    props = dict(boxstyle="round,pad=0.6", facecolor="#F8F9F9", edgecolor="#BDC3C7", alpha=0.9)
    ax.text(0.1, 0.25, legend_text, fontsize=9.5, verticalalignment="bottom", bbox=props, family="sans-serif")

    if show_title:
        ax.set_title(
            "Deterministic Finite Automaton (DFA) for Words Starting with 'com'\n"
            "M = ({q0, q1, q2, q3, qd}, Σ, δ, q0, {q3})",
            fontsize=13,
            fontweight="bold",
            pad=16,
            color="#1B2631"
        )

    plt.tight_layout()

    # Save to disk
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")

    return fig


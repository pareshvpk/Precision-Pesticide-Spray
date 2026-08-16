"""Render the four-stage precision-spraying workflow as a static PNG for the README."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Stage content: (title, description lines, fill, edge)
stages = [
    ("STAGE 1\nIngestion &\nPre-processing",
     "RGB - HSV\nGaussian blur", "#e8f5e9", "#2e7d32"),
    ("STAGE 2\nFeature Extraction\n& Refinement",
     "HSV threshold mask\nmorphology, contours", "#e3f2fd", "#1565c0"),
    ("STAGE 3\nDecision Logic &\nProportional Map",
     "Severity Index (S)\nPWM duty-cycle map", "#fff3e0", "#ef6c00"),
    ("STAGE 4\nActuation &\nReporting",
     "Spray simulation\nCSV data logging", "#f3e5f5", "#7b1fa2"),
]

fig, ax = plt.subplots(figsize=(13, 3.6))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

box_w, box_h = 0.205, 0.6
centers = [0.13, 0.375, 0.625, 0.87]
cy = 0.46

for (title, desc, fill, edge), cx in zip(stages, centers):
    box = FancyBboxPatch(
        (cx - box_w / 2, cy - box_h / 2), box_w, box_h,
        boxstyle="round,pad=0.012,rounding_size=0.02",
        linewidth=2.2, edgecolor=edge, facecolor=fill, mutation_aspect=0.35,
    )
    ax.add_patch(box)
    ax.text(cx, cy + 0.11, title, ha="center", va="center",
            fontsize=11.5, fontweight="bold", color=edge)
    ax.text(cx, cy - 0.16, desc, ha="center", va="center",
            fontsize=9, color="#37474f")

# Arrows between the boxes
for i in range(len(centers) - 1):
    start = centers[i] + box_w / 2
    end = centers[i + 1] - box_w / 2
    ax.add_patch(FancyArrowPatch(
        (start, cy), (end, cy), arrowstyle="-|>", mutation_scale=20,
        linewidth=2.2, color="#607d8b",
    ))

# Input marker
ax.text(0.13, cy + box_h / 2 + 0.12, "Canopy frame  >",
        ha="center", va="center", fontsize=9.5, style="italic", color="#455a64")

ax.set_title("Four-Stage Precision Pesticide Spraying Pipeline",
             fontsize=14, fontweight="bold", pad=14, color="#1b5e20")

plt.tight_layout()
plt.savefig("assets/workflow.png", dpi=200, bbox_inches="tight")
print("Workflow diagram saved as assets/workflow.png")

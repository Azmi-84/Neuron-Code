import matplotlib.pyplot as plt
import numpy as np

# Define materials
materials = [
    {"name": "Marine-Grade Aluminum (5083)", "color": "skyblue"},
    {"name": "Magnesium Alloy (WE43)", "color": "silver"},
    {"name": "CFRP", "color": "darkgreen"},
    {"name": "GFRP", "color": "lightgreen"},
    {"name": "Fiber Metal Laminate (GLARE)", "color": "orange"},
    {"name": "Carbon Fiber Sandwich", "color": "purple"}
]

# Define lifecycle phases
lifecycle_phases = ['Raw Material', 'Manufacturing', 'Use Phase', 'End of Life']

# Environmental impact data (scale 1-10 where LOWER is better - environmental impact)
environmental_impact = {
    "Marine-Grade Aluminum (5083)": [4, 3, 3, 2],
    "Magnesium Alloy (WE43)": [5, 4, 2, 3],
    "CFRP": [7, 6, 2, 8],
    "GFRP": [6, 5, 3, 7],
    "Fiber Metal Laminate (GLARE)": [5, 6, 2, 4],
    "Carbon Fiber Sandwich": [7, 7, 2, 8]
}

# Create figure
fig, ax = plt.subplots(figsize=(14, 8))

# Set width of bars
barWidth = 0.13
r = np.arange(len(lifecycle_phases))

# Plot bars for each material
for i, material in enumerate(materials):
    ax.bar(
        r + i * barWidth, 
        environmental_impact[material["name"]], 
        width=barWidth, 
        color=material["color"], 
        edgecolor='black',
        alpha=0.7,
        label=material["name"]
    )

# Add key sustainability indicators
# Convert impact to sustainability score (10 - impact)
sustainability_scores = {}
for material in materials:
    impact_values = environmental_impact[material["name"]]
    sustainability_scores[material["name"]] = [10 - impact for impact in impact_values]

# Calculate overall sustainability score (average)
overall_scores = []
for material in materials:
    overall_scores.append(np.mean(sustainability_scores[material["name"]]))

# Smaller axis for overall sustainability
ax2 = fig.add_axes([0.15, 0.15, 0.2, 0.2])
ax2.bar(
    [material["name"] for material in materials],
    overall_scores,
    color=[material["color"] for material in materials],
    alpha=0.7,
    edgecolor='black'
)
ax2.set_title('Overall Sustainability Score', fontsize=10)
ax2.set_xticklabels(['Al', 'Mg', 'CF', 'GF', 'FML', 'CFS'], fontsize=8)
ax2.set_ylim(0, 10)
ax2.grid(True, axis='y', alpha=0.3)

# Add labels and title
ax.set_xlabel('Lifecycle Phase', fontsize=14)
ax.set_ylabel('Environmental Impact (Lower is Better)', fontsize=14)
ax.set_title('Lifecycle Environmental Impact Analysis for Ferry Materials', fontsize=16, fontweight='bold')
ax.set_xticks(r + barWidth * 2.5)
ax.set_xticklabels(lifecycle_phases, fontsize=12)
ax.set_ylim(0, 10)

# Add a legend
ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)

# Add annotations for key insights
ax.annotate('CFRP & Sandwich Composites have\nhigh end-of-life impact', 
            xy=(3.5, 8), xytext=(3.2, 9), 
            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
            fontsize=10, ha='center')

ax.annotate('Aluminum has balanced\nperformance across lifecycle', 
            xy=(1.5, 3), xytext=(1.5, 5), 
            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
            fontsize=10, ha='center')

ax.annotate('Lightweight materials reduce\nfuel use in the use phase', 
            xy=(2.5, 2), xytext=(2.5, 1), 
            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
            fontsize=10, ha='center')

# Add grid
ax.grid(True, axis='y', linestyle='--', alpha=0.7)

plt.tight_layout(rect=[0, 0, 0.85, 1])
plt.savefig('ferry_materials_lifecycle_analysis.png', dpi=300)
plt.show()
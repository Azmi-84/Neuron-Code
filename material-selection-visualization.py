import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Ellipse

# Initial setup for matplotlib
plt.rcParams.update({'font.size': 12})

# Create dataframe for the materials
materials = pd.DataFrame({
    'Material': ['High-Carbon Steel', 'Alloy Steel', 'Stainless Steel', 'Titanium Alloy', 'CFRP', 'GFRP'],
    'Density': [7850, 7850, 8000, 4430, 1600, 2000],
    'YieldStrength_Min': [1200, 1100, 1000, 830, 600, 300],
    'YieldStrength_Max': [1400, 1300, 1200, 900, 1500, 600],
    'FatigueResistance': [5, 5, 4, 5, 5, 4],  # 1-5 scale
    'CorrosionResistance': [3, 3, 5, 5, 5, 4],  # 1-5 scale
    'Cost': [1, 1, 3, 5, 5, 2],  # 1-5 scale (1 is low, 5 is high)
    'Sustainability': [4, 3, 4, 3, 2, 4]  # 1-5 scale
})

# Calculate the mean yield strength for plotting
materials['YieldStrength_Mean'] = (materials['YieldStrength_Min'] + materials['YieldStrength_Max']) / 2

# Part 1: Ashby Chart (Strength vs. Density)
plt.figure(figsize=(10, 8))

# Define colors for each material category
colors = ['#1f77b4', '#1f77b4', '#1f77b4', '#ff7f0e', '#2ca02c', '#2ca02c']  # Blue for steels, orange for Ti, green for composites

# Plot each material as an ellipse to represent the range
for i, row in materials.iterrows():
    width = row['Density'] * 0.2  # 20% of density value for width
    height = (row['YieldStrength_Max'] - row['YieldStrength_Min']) * 1.2  # 120% of range for height
    
    ellipse = Ellipse(xy=(row['Density'], row['YieldStrength_Mean']), 
                      width=width, height=height, 
                      angle=0, color=colors[i], alpha=0.7)
    plt.gca().add_patch(ellipse)
    
    # Add material labels
    plt.text(row['Density'], row['YieldStrength_Mean'], 
             row['Material'], horizontalalignment='center', 
             verticalalignment='center', fontsize=9, weight='bold')

# Add diagonal lines for specific strength (strength/density)
densities = np.linspace(1000, 9000, 100)
for specific_strength in [50, 100, 200, 300]:
    strengths = specific_strength * densities / 1000  # Convert to same units
    plt.plot(densities, strengths, 'k--', alpha=0.5, linewidth=1)
    plt.text(8500, specific_strength * 8500 / 1000, f'σ/ρ = {specific_strength}', 
             fontsize=8, alpha=0.7, rotation=25)

# Set log scales for both axes
plt.xscale('log')
plt.yscale('log')

# Set axis limits
plt.xlim(1000, 10000)
plt.ylim(200, 2000)

# Add labels and title
plt.xlabel('Density (kg/m³)', fontsize=12)
plt.ylabel('Yield Strength (MPa)', fontsize=12)
plt.title('Ashby Chart: Yield Strength vs. Density', fontsize=14)

# Add grid
plt.grid(True, which="both", ls="-", alpha=0.2)

# Save the figure
plt.tight_layout()
plt.savefig('ashby_chart_strength_density.png', dpi=300)

# Part 2: Radar Chart for Material Properties
plt.figure(figsize=(10, 8))

# Categories for radar chart
categories = ['Yield Strength', 'Fatigue\nResistance', 'Corrosion\nResistance', 
              'Lightweight\n(Inverse Density)', 'Cost\nEffectiveness', 'Sustainability']

# Define column names without newlines for data processing
data_columns = ['Yield Strength', 'Fatigue Resistance', 'Corrosion Resistance', 
                'Lightweight', 'Cost Effectiveness', 'Sustainability']

# Normalize data for radar chart
normalized_data = pd.DataFrame({
    'Material': materials['Material'],
    'Yield Strength': (materials['YieldStrength_Mean'] - materials['YieldStrength_Mean'].min()) / 
                      (materials['YieldStrength_Mean'].max() - materials['YieldStrength_Mean'].min()),
    'Fatigue Resistance': (materials['FatigueResistance'] - 1) / 4,  # Scale to 0-1
    'Corrosion Resistance': (materials['CorrosionResistance'] - 1) / 4,  # Scale to 0-1
    'Lightweight': 1 - (materials['Density'] - materials['Density'].min()) / 
                  (materials['Density'].max() - materials['Density'].min()),  # Inverse density
    'Cost Effectiveness': 1 - (materials['Cost'] - 1) / 4,  # Inverse cost (1 is high, 0 is low)
    'Sustainability': (materials['Sustainability'] - 1) / 4  # Scale to 0-1
})

# Number of variables
N = len(categories)

# Create angle for each category
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]  # Close the loop

# Create subplot with polar projection
ax = plt.subplot(111, polar=True)

# Draw one axis per variable and add labels
plt.xticks(angles[:-1], categories, size=10)

# Draw y-axis labels
ax.set_rlabel_position(0)
plt.yticks([0.25, 0.5, 0.75], ["0.25", "0.5", "0.75"], color="grey", size=8)
plt.ylim(0, 1)

# Plot each material
for i, row in normalized_data.iterrows():
    values = [row[col] for col in data_columns]
    values += values[:1]  # Close the loop
    
    # Plot values
    ax.plot(angles, values, linewidth=2, linestyle='solid', label=row['Material'])
    ax.fill(angles, values, alpha=0.1)

# Add legend
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

plt.title('Material Properties Comparison', size=14)
plt.tight_layout()
plt.savefig('material_properties_radar.png', dpi=300)

# Part 3: Bar Chart for Sustainability Metrics
plt.figure(figsize=(12, 6))

# Create bar chart for sustainability metrics
materials_sorted = materials.sort_values('Sustainability', ascending=False)

bar_width = 0.35
x = np.arange(len(materials_sorted))

plt.bar(x, materials_sorted['Sustainability'], bar_width, label='Sustainability', color='green', alpha=0.7)
plt.bar(x + bar_width, materials_sorted['Cost'], bar_width, label='Cost', color='red', alpha=0.7)

plt.xlabel('Materials', fontsize=12)
plt.ylabel('Rating (1-5 scale)', fontsize=12)
plt.title('Sustainability and Cost Comparison', fontsize=14)
plt.xticks(x + bar_width / 2, materials_sorted['Material'], rotation=45, ha='right')
plt.legend()

plt.tight_layout()
plt.savefig('sustainability_cost_comparison.png', dpi=300)

# Part 4: Performance Index Bar Chart
plt.figure(figsize=(12, 6))

# Calculate performance indices
materials['StrengthToDensity'] = materials['YieldStrength_Mean'] / materials['Density']
materials['PerformanceIndex'] = (materials['YieldStrength_Mean'] / materials['Density'] * 0.4 + 
                                materials['FatigueResistance'] / 5 * 0.3 + 
                                materials['CorrosionResistance'] / 5 * 0.2 + 
                                (6 - materials['Cost']) / 5 * 0.1)  # Weighted performance index

# Sort by performance index
materials_sorted = materials.sort_values('PerformanceIndex', ascending=False)

# Create bar chart for performance index
plt.bar(materials_sorted['Material'], materials_sorted['PerformanceIndex'], color='#1f77b4', alpha=0.8)

plt.xlabel('Materials', fontsize=12)
plt.ylabel('Performance Index', fontsize=12)
plt.title('Material Performance Index (Weighted)', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('performance_index.png', dpi=300)

print("All visualizations have been generated and saved:")
print("1. ashby_chart_strength_density.png")
print("2. material_properties_radar.png")
print("3. sustainability_cost_comparison.png")
print("4. performance_index.png")
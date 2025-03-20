import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch

# Create a DataFrame from the materials data
materials = {
    'Material': ['Mild Steel (Carbon Steel)', 'Stainless Steel (316L)', 'Marine-Grade Aluminum Alloy (5083)', 
                 'Titanium Alloy (Ti-6Al-4V)', 'CFRP', 'GFRP'],
    'Density (kg/m³)': [7850, 8000, 2600, 4430, 1600, 2000],
    'Yield Strength Min (MPa)': [250, 250, 200, 800, 600, 250],
    'Yield Strength Max (MPa)': [400, 550, 350, 1100, 1500, 600],
    'Young\'s Modulus Min (GPa)': [200, 200, 70, 110, 70, 20],
    'Young\'s Modulus Max (GPa)': [200, 200, 70, 110, 150, 50],
    'Fracture Toughness Min (MPa√m)': [50, 50, 20, 50, 20, 15],
    'Fracture Toughness Max (MPa√m)': [100, 100, 30, 100, 50, 40],
    'Max Service Temperature (°C)': [400, 870, 200, 200, 600, 250],
    'Relative Cost (arbitrary units)': [1.0, 1.5, 1.2, 5.0, 4.0, 1.8]
}

df = pd.DataFrame(materials)

# Calculate midpoints for properties with ranges
for prop in ['Yield Strength', 'Young\'s Modulus', 'Fracture Toughness']:
    df[f'{prop} (Midpoint)'] = (df[f'{prop} Min (MPa√m)'] + df[f'{prop} Max (MPa√m)']) / 2 if 'Fracture' in prop else (df[f'{prop} Min (MPa)'] + df[f'{prop} Max (MPa)']) / 2 if 'Yield' in prop else (df[f'{prop} Min (GPa)'] + df[f'{prop} Max (GPa)']) / 2

# Set a consistent style
plt.style.use('seaborn-v0_8-whitegrid')
colors = sns.color_palette('viridis', 6)
highlight_color = 'red'

# Create a color map where Stainless Steel is highlighted
material_colors = {}
for i, material in enumerate(df['Material']):
    if material == 'Stainless Steel (316L)':
        material_colors[material] = highlight_color
    else:
        material_colors[material] = colors[i]

# 1. Create a normalized heatmap for all properties
# Normalize the data for heatmap
properties = ['Density (kg/m³)', 'Yield Strength (Midpoint)', 'Young\'s Modulus (Midpoint)', 
              'Fracture Toughness (Midpoint)', 'Max Service Temperature (°C)', 'Relative Cost (arbitrary units)']

# Create a new DataFrame for the heatmap
heatmap_data = df[['Material'] + properties].set_index('Material')

# Normalize each column to 0-1 range
for col in heatmap_data.columns:
    min_val = heatmap_data[col].min()
    max_val = heatmap_data[col].max()
    if min_val != max_val:
        heatmap_data[col] = (heatmap_data[col] - min_val) / (max_val - min_val)

plt.figure(figsize=(14, 8))
# Create a custom colormap that uses red for high values
cmap = sns.color_palette("YlGnBu", as_cmap=True)
heatmap = sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap=cmap, linewidths=0.5)
plt.title('Normalized Material Properties Comparison', fontsize=16)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('materials_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Material Properties Radar Chart
properties = ['Density (kg/m³)', 'Yield Strength (Midpoint)', 'Young\'s Modulus (Midpoint)', 
              'Fracture Toughness (Midpoint)', 'Max Service Temperature (°C)', 'Relative Cost (arbitrary units)']

# Create a normalized version for the radar chart
radar_df = df[['Material'] + properties].copy()
for prop in properties:
    min_val = radar_df[prop].min()
    max_val = radar_df[prop].max()
    # For properties where lower is better, invert the normalization
    if prop in ['Density (kg/m³)', 'Relative Cost (arbitrary units)']:
        radar_df[prop] = 1 - (radar_df[prop] - min_val) / (max_val - min_val)
    else:
        radar_df[prop] = (radar_df[prop] - min_val) / (max_val - min_val)

# Function to create radar chart
def radar_chart(df, properties, title):
    # Number of variables
    N = len(properties)
    
    # Create a figure
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, polar=True)
    
    # Compute angle for each property
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Close the loop
    
    # Draw one line per material and fill area
    for i, material in enumerate(df['Material']):
        values = df.loc[df['Material'] == material, properties].values.flatten().tolist()
        values += values[:1]  # Close the loop
        
        color = material_colors[material]
        linestyle = '-' if material == 'Stainless Steel (316L)' else '--'
        linewidth = 3 if material == 'Stainless Steel (316L)' else 1.5
        alpha = 0.8 if material == 'Stainless Steel (316L)' else 0.5
        
        ax.plot(angles, values, linewidth=linewidth, linestyle=linestyle, color=color, label=material)
        ax.fill(angles, values, color=color, alpha=alpha * 0.2)
    
    # Add property labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(properties, fontsize=10)
    
    # Add a title
    plt.title(title, size=15, fontweight='bold', y=1.1)
    
    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    return fig

radar_fig = radar_chart(radar_df, properties, 'Material Properties Comparison (Higher is Better)')
plt.tight_layout()
plt.savefig('materials_radar.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Bar charts for key properties with ranges
# Create a figure with subplots for each property
fig, axes = plt.subplots(3, 2, figsize=(16, 18))
axes = axes.flatten()

# Properties to plot
range_properties = [
    ('Yield Strength Min (MPa)', 'Yield Strength Max (MPa)', 'Yield Strength (MPa)'),
    ('Young\'s Modulus Min (GPa)', 'Young\'s Modulus Max (GPa)', 'Young\'s Modulus (GPa)'),
    ('Fracture Toughness Min (MPa√m)', 'Fracture Toughness Max (MPa√m)', 'Fracture Toughness (MPa√m)'),
]

# Single value properties
single_properties = [
    'Density (kg/m³)',
    'Max Service Temperature (°C)',
    'Relative Cost (arbitrary units)'
]

# Plot range properties
for i, (min_prop, max_prop, title) in enumerate(range_properties):
    ax = axes[i]
    
    # Create error bars to represent ranges
    x = np.arange(len(df['Material']))
    y = [(min_val + max_val) / 2 for min_val, max_val in zip(df[min_prop], df[max_prop])]
    yerr = [(max_val - min_val) / 2 for min_val, max_val in zip(df[min_prop], df[max_prop])]
    
    # Plot bars with custom colors
    for j, material in enumerate(df['Material']):
        color = material_colors[material]
        ax.bar(x[j], y[j], yerr=yerr[j], capsize=10, color=color, alpha=0.7,
               error_kw={'elinewidth': 2, 'capthick': 2})
    
    ax.set_xticks(x)
    ax.set_xticklabels(df['Material'], rotation=45, ha='right')
    ax.set_title(title, fontsize=14)
    ax.set_ylabel(title.split('(')[0])
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Highlight the chosen material
    chosen_idx = list(df['Material']).index('Stainless Steel (316L)')
    ax.get_xticklabels()[chosen_idx].set_color(highlight_color)
    ax.get_xticklabels()[chosen_idx].set_fontweight('bold')

# Plot single value properties
for i, prop in enumerate(single_properties):
    ax = axes[i+3]
    
    # Plot bars with custom colors
    for j, material in enumerate(df['Material']):
        color = material_colors[material]
        ax.bar(j, df.loc[df['Material'] == material, prop].values[0], color=color, alpha=0.7)
    
    ax.set_xticks(range(len(df['Material'])))
    ax.set_xticklabels(df['Material'], rotation=45, ha='right')
    ax.set_title(prop, fontsize=14)
    ax.set_ylabel(prop.split('(')[0])
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Highlight the chosen material
    chosen_idx = list(df['Material']).index('Stainless Steel (316L)')
    ax.get_xticklabels()[chosen_idx].set_color(highlight_color)
    ax.get_xticklabels()[chosen_idx].set_fontweight('bold')

plt.tight_layout()
plt.savefig('materials_properties.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Create a scatter plot of strength-to-weight ratio vs cost
plt.figure(figsize=(12, 8))

# Calculate strength-to-weight ratio (using midpoint yield strength)
df['Strength-to-Weight'] = df['Yield Strength (Midpoint)'] / df['Density (kg/m³)'] * 1000  # Scaling for better visualization

# Create scatter plot
for i, material in enumerate(df['Material']):
    color = material_colors[material]
    marker_size = 200 if material == 'Stainless Steel (316L)' else 100
    marker_edge = 'black' if material == 'Stainless Steel (316L)' else 'none'
    plt.scatter(df.loc[df['Material'] == material, 'Relative Cost (arbitrary units)'], 
                df.loc[df['Material'] == material, 'Strength-to-Weight'],
                s=marker_size, color=color, label=material, edgecolor=marker_edge, linewidth=2, alpha=0.8)
    
    # Add material label
    plt.text(df.loc[df['Material'] == material, 'Relative Cost (arbitrary units)'].values[0] + 0.05,
             df.loc[df['Material'] == material, 'Strength-to-Weight'].values[0],
             material, fontsize=10)

plt.xlabel('Relative Cost (arbitrary units)', fontsize=12)
plt.ylabel('Strength-to-Weight Ratio (MPa/(kg/m³) × 1000)', fontsize=12)
plt.title('Strength-to-Weight Ratio vs. Cost', fontsize=16)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('strength_weight_cost.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Summary table with material ranking
# Create a scoring system for material selection
weights = {
    'Density (kg/m³)': -0.15,  # Negative weight because lower is better
    'Yield Strength (Midpoint)': 0.2,
    'Young\'s Modulus (Midpoint)': 0.15,
    'Fracture Toughness (Midpoint)': 0.2,
    'Max Service Temperature (°C)': 0.1,
    'Relative Cost (arbitrary units)': -0.2  # Negative weight because lower is better
}

# Normalize all properties to 0-1 scale for scoring
score_df = df.copy()
for prop in weights.keys():
    min_val = score_df[prop].min()
    max_val = score_df[prop].max()
    if min_val != max_val:
        score_df[prop] = (score_df[prop] - min_val) / (max_val - min_val)

# Calculate weighted scores
score_df['Total Score'] = 0
for prop, weight in weights.items():
    score_df['Total Score'] += score_df[prop] * weight

# Rank materials
score_df['Rank'] = score_df['Total Score'].rank(ascending=False).astype(int)

# Create a summary table
summary = score_df[['Material', 'Total Score', 'Rank']].sort_values('Rank')

plt.figure(figsize=(8, 6))
ax = plt.subplot(111, frame_on=False)
ax.xaxis.set_visible(False) 
ax.yaxis.set_visible(False)

# Create a table with material rankings
table_data = []
headers = ['Rank', 'Material', 'Score']
for _, row in summary.iterrows():
    table_data.append([str(row['Rank']), row['Material'], f"{row['Total Score']:.3f}"])

# Create the table
table = plt.table(cellText=table_data, colLabels=headers, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 1.5)

# Highlight the chosen material
for i, row in enumerate(table_data):
    if row[1] == 'Stainless Steel (316L)':
        for j in range(len(row)):
            table[(i+1, j)].set_facecolor(highlight_color)
            table[(i+1, j)].set_text_props(color='white', weight='bold')

plt.title('Material Ranking for Ship Rudder Application', fontsize=16, pad=20)
plt.tight_layout()
plt.savefig('material_ranking.png', dpi=300, bbox_inches='tight')
plt.close()

# Print conclusions about the chosen material
print("Analysis of Stainless Steel (316L) for Ship Rudder Application:")
print("----------------------------------------")
idx = df.index[df['Material'] == 'Stainless Steel (316L)'].tolist()[0]

# Get ranking
rank = summary.loc[summary['Material'] == 'Stainless Steel (316L)', 'Rank'].values[0]
print(f"Overall Ranking: {rank} out of {len(df)}")

# Strengths
strengths = []
if df.loc[idx, 'Max Service Temperature (°C)'] > df['Max Service Temperature (°C)'].median():
    strengths.append(f"Excellent high temperature resistance ({df.loc[idx, 'Max Service Temperature (°C)']}°C)")
if df.loc[idx, 'Yield Strength (Midpoint)'] >= 400:
    strengths.append(f"Good strength properties ({df.loc[idx, 'Yield Strength Min (MPa)']} - {df.loc[idx, 'Yield Strength Max (MPa)']} MPa)")
if df.loc[idx, 'Fracture Toughness (Midpoint)'] >= df['Fracture Toughness (Midpoint)'].median():
    strengths.append(f"Good fracture toughness ({df.loc[idx, 'Fracture Toughness Min (MPa√m)']} - {df.loc[idx, 'Fracture Toughness Max (MPa√m)']} MPa√m)")
if df.loc[idx, 'Relative Cost (arbitrary units)'] < df['Relative Cost (arbitrary units)'].median():
    strengths.append(f"Moderate cost (only {df.loc[idx, 'Relative Cost (arbitrary units)']} relative units)")

print("\nStrengths:")
for s in strengths:
    print(f"- {s}")

# Weaknesses
weaknesses = []
if df.loc[idx, 'Density (kg/m³)'] > df['Density (kg/m³)'].median():
    weaknesses.append(f"High density ({df.loc[idx, 'Density (kg/m³)']} kg/m³)")
if df.loc[idx, 'Strength-to-Weight'] < df['Strength-to-Weight'].median():
    weaknesses.append("Lower strength-to-weight ratio compared to some alternatives")

print("\nConsiderations:")
for w in weaknesses:
    print(f"- {w}")

# Conclusion
print("\nConclusion:")
print("Stainless Steel (316L) is a suitable material for ship rudders due to its excellent corrosion resistance, good mechanical properties, and moderate cost. Its high temperature resistance and good fracture toughness make it durable in marine environments. While heavier than some alternatives, its balance of properties makes it a practical choice for this application.")
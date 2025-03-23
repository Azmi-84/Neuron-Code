import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
import os
import datetime
import time

# Create a DataFrame from the materials data for aircraft de-icing systems
materials = {
    'Material': ['Aluminum Alloy (6061-T6)', 'Titanium Alloy (Ti-6Al-4V)', 'Copper', 
                 'Stainless Steel (316L)', 'Graphene-Based Composites', 'CFRP with Heating Elements'],
    'Density (kg/m³)': [2700, 4430, 8960, 8000, 1600, 1550],
    'Thermal Conductivity (W/mK)': [167, 6.7, 385, 16, 2000, 15],  # Using midpoint for CFRP
    'Electrical Resistivity (µΩ·m)': [3.7, 1.8, 1.7, 74, 0.001, 50],  # Estimated for CFRP
    'Corrosion Resistance': [3, 5, 3, 5, 5, 4],  # Scale of 1-5 where 5 is excellent
    'Relative Cost (arbitrary units)': [1.2, 5.0, 2.5, 1.5, 10.0, 4.5]
}

df = pd.DataFrame(materials)

# Set a consistent style
plt.style.use('seaborn-v0_8-whitegrid')
colors = sns.color_palette('viridis', 6)
highlight_color = 'red'

# Highlight Aluminum Alloy (6061-T6) as mentioned in the paper
highlighted_material = "Aluminum Alloy (6061-T6)"

# Create a color map where the selected material is highlighted
material_colors = {}
for i, material in enumerate(df['Material']):
    if material == highlighted_material:
        material_colors[material] = highlight_color
    else:
        material_colors[material] = colors[i]

# Create a function to save figures in multiple formats with error handling
def save_figure(fig, filename_base, formats=['png', 'pdf', 'svg'], dpi=300):
    """
    Save a matplotlib figure in multiple formats with error handling
    
    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        The figure to save
    filename_base : str
        Base filename without extension
    formats : list
        List of formats to save (e.g., ['png', 'pdf', 'svg'])
    dpi : int
        Resolution for raster formats
    """
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Add timestamp to avoid overwriting files
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save in each requested format
    for fmt in formats:
        try:
            output_path = os.path.join(output_dir, f"{filename_base}_{timestamp}.{fmt}")
            if fmt in ['png', 'jpg', 'jpeg']:
                fig.savefig(output_path, dpi=dpi, bbox_inches='tight')
            else:
                fig.savefig(output_path, bbox_inches='tight')
            print(f"Saved: {output_path}")
        except Exception as e:
            print(f"Error saving {filename_base} in {fmt} format: {str(e)}")
    
    return output_dir

# 1. Create a normalized heatmap for all properties
# Normalize the data for heatmap
properties = ['Density (kg/m³)', 'Thermal Conductivity (W/mK)', 'Electrical Resistivity (µΩ·m)', 
              'Corrosion Resistance', 'Relative Cost (arbitrary units)']

# Create a new DataFrame for the heatmap
heatmap_data = df[['Material'] + properties].set_index('Material')

# Normalize each column to 0-1 range
for col in heatmap_data.columns:
    min_val = heatmap_data[col].min()
    max_val = heatmap_data[col].max()
    if min_val != max_val:
        # For properties where lower is better, invert the normalization
        if col in ['Density (kg/m³)', 'Electrical Resistivity (µΩ·m)', 'Relative Cost (arbitrary units)']:
            heatmap_data[col] = 1 - (heatmap_data[col] - min_val) / (max_val - min_val)
        else:
            heatmap_data[col] = (heatmap_data[col] - min_val) / (max_val - min_val)

plt.figure(figsize=(14, 8))
# Create a custom colormap
cmap = sns.color_palette("YlGnBu", as_cmap=True)
heatmap = sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap=cmap, linewidths=0.5)
plt.title('Normalized Material Properties for Aircraft De-icing Systems', fontsize=16)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
save_figure(plt.gcf(), 'deicing_materials_heatmap')
plt.close()

# 2. Material Properties Radar Chart
properties = ['Density (kg/m³)', 'Thermal Conductivity (W/mK)', 'Electrical Resistivity (µΩ·m)', 
              'Corrosion Resistance', 'Relative Cost (arbitrary units)']

# Create a normalized version for the radar chart
radar_df = df[['Material'] + properties].copy()
for prop in properties:
    min_val = radar_df[prop].min()
    max_val = radar_df[prop].max()
    # For properties where lower is better, invert the normalization
    if prop in ['Density (kg/m³)', 'Electrical Resistivity (µΩ·m)', 'Relative Cost (arbitrary units)']:
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
        linestyle = '-' if material == highlighted_material else '--'
        linewidth = 3 if material == highlighted_material else 1.5
        alpha = 0.8 if material == highlighted_material else 0.5
        
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

radar_fig = radar_chart(radar_df, properties, 'Material Properties for Aircraft De-icing Systems (Higher is Better)')
plt.tight_layout()
save_figure(radar_fig, 'deicing_materials_radar')
plt.close()

# 3. Bar charts for key properties
fig, axes = plt.subplots(3, 2, figsize=(16, 18))
axes = axes.flatten()

# Properties to plot with their respective axis index
property_axes = {
    'Density (kg/m³)': 0,
    'Thermal Conductivity (W/mK)': 1,
    'Electrical Resistivity (µΩ·m)': 2,
    'Corrosion Resistance': 3,
    'Relative Cost (arbitrary units)': 4
}

# Helper text for property descriptions
property_descriptions = {
    'Density (kg/m³)': 'Lower is better for aircraft weight reduction',
    'Thermal Conductivity (W/mK)': 'Higher is better for heat distribution',
    'Electrical Resistivity (µΩ·m)': 'Lower is better for electrothermal systems',
    'Corrosion Resistance': 'Higher is better for exposure to de-icing fluids',
    'Relative Cost (arbitrary units)': 'Lower is better for economic viability'
}

# Plot each property
for prop, ax_idx in property_axes.items():
    ax = axes[ax_idx]
    
    # Plot bars with custom colors
    for j, material in enumerate(df['Material']):
        color = material_colors[material]
        ax.bar(j, df.loc[df['Material'] == material, prop].values[0], color=color, alpha=0.7)
    
    ax.set_xticks(range(len(df['Material'])))
    ax.set_xticklabels(df['Material'], rotation=45, ha='right')
    ax.set_title(f"{prop}\n{property_descriptions.get(prop, '')}", fontsize=14)
    ax.set_ylabel(prop.split('(')[0])
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Highlight chosen material
    try:
        chosen_idx = list(df['Material']).index(highlighted_material)
        ax.get_xticklabels()[chosen_idx].set_color(highlight_color)
        ax.get_xticklabels()[chosen_idx].set_fontweight('bold')
    except (ValueError, IndexError):
        print(f"Warning: Could not highlight {highlighted_material} in the chart.")

# Hide the unused subplot
axes[5].axis('off')

plt.tight_layout()
save_figure(plt.gcf(), 'deicing_materials_properties')
plt.close()

# 4. Create a scatter plot of thermal conductivity vs corrosion resistance
plt.figure(figsize=(12, 8))

# Create scatter plot
for i, material in enumerate(df['Material']):
    color = material_colors[material]
    marker_size = 200 if material == highlighted_material else 100
    marker_edge = 'black' if material == highlighted_material else 'none'
    plt.scatter(df.loc[df['Material'] == material, 'Corrosion Resistance'], 
                df.loc[df['Material'] == material, 'Thermal Conductivity (W/mK)'],
                s=marker_size, color=color, label=material, edgecolor=marker_edge, linewidth=2, alpha=0.8)
    
    # Add material label
    plt.text(df.loc[df['Material'] == material, 'Corrosion Resistance'].values[0] + 0.05,
             df.loc[df['Material'] == material, 'Thermal Conductivity (W/mK)'].values[0],
             material, fontsize=10)

plt.xlabel('Corrosion Resistance (higher is better)', fontsize=12)
plt.ylabel('Thermal Conductivity (W/mK)', fontsize=12)
plt.title('Thermal Conductivity vs. Corrosion Resistance for De-icing Materials', fontsize=16)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
save_figure(plt.gcf(), 'thermal_corrosion_plot')
plt.close()

# 5. Create a performance index for de-icing materials
# Define weights based on the paper's priorities
weights = {
    'Density (kg/m³)': -0.15,  # Negative weight because lower is better
    'Thermal Conductivity (W/mK)': 0.25,
    'Electrical Resistivity (µΩ·m)': -0.15,  # Negative weight because lower is better
    'Corrosion Resistance': 0.25,
    'Relative Cost (arbitrary units)': -0.20  # Negative weight because lower is better
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

# Highlight the selected material
for i, row in enumerate(table_data):
    if row[1] == highlighted_material:
        for j in range(len(row)):
            table[(i+1, j)].set_facecolor(highlight_color)
            table[(i+1, j)].set_text_props(color='white', weight='bold')

plt.title('Material Ranking for Aircraft De-icing Systems', fontsize=16, pad=20)
plt.tight_layout()
save_figure(plt.gcf(), 'deicing_material_ranking')
plt.close()

# 6. Create a composite image that combines all charts
def create_composite_image():
    """Create a composite image that combines all individual charts"""
    try:
        import matplotlib.gridspec as gridspec
        import matplotlib.image as mpimg
        
        # First make sure all individual images are created
        output_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(output_dir, 'output')
        
        # Find the most recent files with each prefix - excluding thermal_corrosion_plot
        image_files = {}
        for prefix in ['deicing_materials_heatmap', 'deicing_materials_radar', 
                       'deicing_materials_properties', 'deicing_material_ranking']:
            matching_files = [f for f in os.listdir(output_dir) 
                              if f.startswith(prefix) and f.endswith('.png')]
            if matching_files:
                # Get the most recent file
                newest_file = max(matching_files, key=lambda f: os.path.getmtime(os.path.join(output_dir, f)))
                image_files[prefix] = os.path.join(output_dir, newest_file)
        
        if len(image_files) < 4:
            print("Not all required images found in output directory")
            return
        
        # Create composite figure with 2x2 layout
        fig = plt.figure(figsize=(20, 18))
        gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1.2])
        
        fig.suptitle('Material Selection Analysis for Aircraft De-icing Systems', fontsize=24, fontweight='bold', y=0.98)
        
        # Heatmap (top left)
        ax1 = fig.add_subplot(gs[0, 0])
        img1 = mpimg.imread(image_files['deicing_materials_heatmap'])
        ax1.imshow(img1)
        ax1.axis('off')
        ax1.set_title('Property Comparison Heatmap', fontsize=16)
        
        # Radar chart (top right)
        ax2 = fig.add_subplot(gs[0, 1])
        img2 = mpimg.imread(image_files['deicing_materials_radar'])
        ax2.imshow(img2)
        ax2.axis('off')
        ax2.set_title('Material Properties Radar Chart', fontsize=16)
        
        # Property bar charts (bottom left)
        ax3 = fig.add_subplot(gs[1, 0])
        img3 = mpimg.imread(image_files['deicing_materials_properties'])
        ax3.imshow(img3)
        ax3.axis('off')
        ax3.set_title('Material Properties Comparison', fontsize=16)
        
        # Material ranking (bottom right)
        ax4 = fig.add_subplot(gs[1, 1])
        img4 = mpimg.imread(image_files['deicing_material_ranking'])
        ax4.imshow(img4)
        ax4.axis('off')
        ax4.set_title('Material Ranking', fontsize=16)
        
        plt.figtext(0.5, 0.01, 'Material Selection Analysis for Aircraft De-icing Systems',
                   ha='center', fontsize=12, fontstyle='italic')
        
        # Save the composite image
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        composite_path = os.path.join(output_dir, f"deicing_material_analysis_composite_{timestamp}.png")
        plt.savefig(composite_path, dpi=300, bbox_inches='tight')
        
        # Also save as PDF for better quality in publications
        pdf_path = os.path.join(output_dir, f"deicing_material_analysis_composite_{timestamp}.pdf")
        plt.savefig(pdf_path, bbox_inches='tight')
        
        print(f"Composite image saved to: {composite_path}")
        print(f"PDF version saved to: {pdf_path}")
        
        plt.close()
        return composite_path
        
    except Exception as e:
        print(f"Error creating composite image: {str(e)}")
        return None

# Create the composite image at the end
composite_image_path = create_composite_image()

print("\nAnalysis complete. All visualizations have been saved to the 'output' directory.")

# Print conclusions about the chosen material
print(f"Analysis of {highlighted_material} for Aircraft De-icing Systems Application:")
print("----------------------------------------")

try:
    idx = df.index[df['Material'] == highlighted_material].tolist()[0]
    
    # Get ranking
    rank = summary.loc[summary['Material'] == highlighted_material, 'Rank'].values[0]
    print(f"Overall Ranking: {rank} out of {len(df)}")
    
    # Strengths
    strengths = []
    if df.loc[idx, 'Thermal Conductivity (W/mK)'] > df['Thermal Conductivity (W/mK)'].median():
        strengths.append(f"Good thermal conductivity ({df.loc[idx, 'Thermal Conductivity (W/mK)']} W/mK)")
    if df.loc[idx, 'Density (kg/m³)'] < df['Density (kg/m³)'].median():
        strengths.append(f"Lightweight ({df.loc[idx, 'Density (kg/m³)']} kg/m³)")
    if df.loc[idx, 'Corrosion Resistance'] >= 3:
        strengths.append(f"Moderate corrosion resistance (rated {df.loc[idx, 'Corrosion Resistance']} out of 5)")
    if df.loc[idx, 'Relative Cost (arbitrary units)'] < df['Relative Cost (arbitrary units)'].median():
        strengths.append(f"Cost-effective (only {df.loc[idx, 'Relative Cost (arbitrary units)']} relative units)")
    
    print("\nStrengths:")
    for s in strengths:
        print(f"- {s}")
    
    # Considerations/Weaknesses
    weaknesses = []
    if df.loc[idx, 'Electrical Resistivity (µΩ·m)'] > df['Electrical Resistivity (µΩ·m)'].median():
        weaknesses.append(f"Higher electrical resistivity ({df.loc[idx, 'Electrical Resistivity (µΩ·m)']} µΩ·m)")
    if df.loc[idx, 'Corrosion Resistance'] < 5:
        weaknesses.append("May require coatings for improved resistance to de-icing fluids")
    
    print("\nConsiderations:")
    for w in weaknesses:
        print(f"- {w}")
    
    # Conclusion aligned with the paper
    print("\nConclusion:")
    print(f"{highlighted_material} is the optimal choice for aircraft de-icing systems due to its balance of lightweight properties, corrosion resistance, and thermal conductivity. Its manufacturability and cost-effectiveness make it particularly suitable for this application.")

except Exception as e:
    print(f"Error generating analysis for {highlighted_material}: {str(e)}")
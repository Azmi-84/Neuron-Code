import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.gridspec as gridspec
from matplotlib.ticker import ScalarFormatter
import os

# Set global plotting parameters for publication quality
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 11
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.7

# Define the materials data
materials = [
    {"name": "Mild Steel", "density": 7850, "yield_low": 250, "yield_high": 400, "color": "#A9A9A9"},
    {"name": "Stainless Steel 316L", "density": 8000, "yield_low": 250, "yield_high": 550, "color": "#87CEFA"},
    {"name": "Aluminum Alloy 5083", "density": 2600, "yield_low": 200, "yield_high": 350, "color": "#00BFFF"},
    {"name": "Titanium Alloy Ti-6Al-4V", "density": 4430, "yield_low": 800, "yield_high": 1100, "color": "#FFD700"},
    {"name": "CFRP", "density": 1600, "yield_low": 600, "yield_high": 1500, "color": "#006400"},
    {"name": "GFRP", "density": 2000, "yield_low": 250, "yield_high": 600, "color": "#90EE90"}
]

# Create a DataFrame for the materials property data
data = {
    'Material': [m["name"] for m in materials],
    'Density (kg/m³)': [7850, 8000, 2600, 4430, 1600, 2000],
    'Yield Strength (MPa)': [325, 400, 275, 950, 1050, 425],
    'Corrosion Resistance': ['Poor', 'Excellent', 'Good', 'Excellent', 'Excellent', 'Good'],
    'Relative Cost': ['Low', 'High', 'Moderate', 'Very High', 'High', 'Moderate'],
    'Sustainability': ['Moderate', 'High', 'High', 'Moderate', 'Variable', 'High'],
    'Specific Strength': [0.041, 0.050, 0.106, 0.214, 0.656, 0.213],
    'Fatigue Resistance': ['Moderate', 'Good', 'Moderate', 'Excellent', 'Good', 'Moderate'],
    'Manufacturability': ['Excellent', 'Good', 'Good', 'Moderate', 'Moderate', 'Good'],
    'Overall Rating': [6, 9, 8, 7, 7, 7]
}
df = pd.DataFrame(data)

# Define performance indices
indices = {
    "Strength to Weight": [0.041, 0.050, 0.106, 0.214, 0.656, 0.213],  # σ/ρ
    "Corrosion Resistance": [0.3, 0.9, 0.7, 0.95, 0.9, 0.8],  # Normalized
    "Cost Efficiency": [0.9, 0.6, 0.75, 0.3, 0.4, 0.65],  # Normalized
    "Overall Performance": [0.56, 0.8, 0.75, 0.72, 0.68, 0.67]  # Combined
}

# Ensure the output directory exists
output_dir = 'material_analysis_output'
os.makedirs(output_dir, exist_ok=True)

# Function to create improved Ashby chart
def create_ashby_chart():
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    
    # Set logarithmic scales
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    # Plot material ranges as ellipses with improved style
    for material in materials:
        # Calculate ellipse parameters
        width = 0.18  # Width factor for the ellipse
        height = material["yield_high"] - material["yield_low"]
        center_x = material["density"]
        center_y = (material["yield_high"] + material["yield_low"]) / 2
        
        # Create and add the ellipse with improved style
        ellipse = patches.Ellipse(
            (center_x, center_y), 
            width * center_x, 
            height * 0.7,  # Adjusted height for better visualization
            facecolor=material["color"],
            alpha=0.8,
            edgecolor='black',
            linewidth=1.5,
            zorder=2
        )
        ax.add_patch(ellipse)
        
        # Add material name label with improved style
        ax.annotate(
            material["name"],
            (center_x, center_y),
            fontsize=10,
            ha='center',
            va='center',
            weight='bold',
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1),
            zorder=3
        )
    
    # Add guideline for constant specific strength with improved style
    x_values = np.logspace(3, 4, 100)  # Density range
    for specific_strength in [0.01, 0.05, 0.1, 0.5]:
        y_values = specific_strength * x_values
        ax.plot(x_values, y_values, '--', color='#555555', linewidth=1.2, zorder=1)
        ax.annotate(
            f"σ/ρ = {specific_strength} MPa/(kg/m³)",
            (x_values[-10], y_values[-10]),
            fontsize=9,
            color='#555555',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=1),
            rotation=38,
            zorder=3
        )
    
    # Customize axis labels and title with improved style
    ax.set_xlabel('Density, ρ (kg/m³)', fontsize=12, weight='bold')
    ax.set_ylabel('Yield Strength, σ (MPa)', fontsize=12, weight='bold')
    ax.set_title('Ashby Chart: Yield Strength vs. Density for Ship Rudder Materials', 
                fontsize=14, fontweight='bold', pad=15)
    
    # Set plot limits
    ax.set_xlim(1200, 12000)
    ax.set_ylim(100, 2000)
    
    # Add custom grid
    ax.grid(True, which='both', linestyle='--', linewidth=0.8, alpha=0.6)
    
    # Add x and y axis ticks with ScalarFormatter to avoid scientific notation
    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.set_major_formatter(ScalarFormatter())
    
    # Add a legend box explaining the chart with improved style
    legend_text = "Materials Selection for Ship Rudders\n" + \
                  "• Ellipses represent property ranges\n" + \
                  "• Diagonal lines show constant specific strength\n" + \
                  "• Higher specific strength (top-left) is better\n" + \
                  "• Optimal materials maximize strength-to-weight ratio"
    
    plt.figtext(0.15, 0.15, legend_text, fontsize=10, 
                bbox=dict(facecolor='white', edgecolor='black', alpha=0.85, boxstyle='round,pad=0.5'))
    
    plt.tight_layout()
    # Save the figure with high quality
    plt.savefig(f'{output_dir}/ashby_chart_improved.png', dpi=300, bbox_inches='tight')
    plt.close()

# Function to create improved performance index chart
def create_performance_index_chart():
    fig = plt.figure(figsize=(14, 10))
    
    # Create a custom color map for gradient bars
    colors = [m["color"] for m in materials]
    
    # Create a 2x2 grid for the charts
    gs = gridspec.GridSpec(2, 2, figure=fig, wspace=0.3, hspace=0.4)
    
    # Plot each performance index with improved style
    for i, (index_name, values) in enumerate(indices.items()):
        ax = fig.add_subplot(gs[i])
        
        # Create horizontal bars for better readability
        material_names = [m["name"] for m in materials]
        y_pos = np.arange(len(material_names))
        
        # Sort materials by performance for each index
        sorted_indices = np.argsort(values)[::-1]  # Descending order
        sorted_names = [material_names[i] for i in sorted_indices]
        sorted_values = [values[i] for i in sorted_indices]
        sorted_colors = [colors[i] for i in sorted_indices]
        
        bars = ax.barh(
            y_pos,
            sorted_values,
            color=sorted_colors,
            alpha=0.9,
            edgecolor='black',
            linewidth=1,
            height=0.7
        )
        
        # Add values at the end of bars
        for j, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(
                width + 0.02,
                bar.get_y() + bar.get_height()/2,
                f'{sorted_values[j]:.3f}',
                ha='left',
                va='center',
                fontsize=9,
                fontweight='bold'
            )
        
        # Add grid lines
        ax.grid(True, axis='x', linestyle='--', alpha=0.7)
        ax.set_axisbelow(True)
        
        # Customize axis labels and title
        ax.set_yticks(y_pos)
        ax.set_yticklabels(sorted_names, fontsize=10)
        ax.set_xlabel('Performance Index Value', fontsize=11, weight='bold')
        ax.set_title(f'{index_name} Index', fontsize=14, fontweight='bold', pad=10)
        
        # Set the x-axis limit to make the chart more readable
        ax.set_xlim(0, max(values) * 1.2)
        
        # Add a thin box around the plot
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(True)
        
    # Add a super title for the entire figure
    fig.suptitle('Performance Indices for Ship Rudder Materials', fontsize=16, fontweight='bold', y=0.98)
    
    # Add a explanation text at the bottom
    explanation = """
    Performance indices normalize material properties to allow direct comparison.
    Higher values indicate better performance for the specific application criteria.
    """
    plt.figtext(0.5, 0.01, explanation, fontsize=10, ha='center', 
                bbox=dict(facecolor='#f0f0f0', edgecolor='gray', alpha=0.9, boxstyle='round,pad=0.5'))
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(f'{output_dir}/performance_indices_improved.png', dpi=300, bbox_inches='tight')
    plt.close()

# Function to create improved materials comparison heatmap
def create_materials_heatmap():
    # Convert categorical data to numeric for visualization
    corrosion_map = {'Poor': 2, 'Moderate': 5, 'Good': 8, 'Excellent': 10}
    cost_map = {'Low': 9, 'Moderate': 6, 'High': 3, 'Very High': 1}  # Inverted for cost (lower is better)
    sustainability_map = {'Variable': 5, 'Moderate': 6, 'High': 9}
    fatigue_map = {'Moderate': 5, 'Good': 8, 'Excellent': 10}
    manufacturability_map = {'Moderate': 5, 'Good': 8, 'Excellent': 10}
    
    # Create a new DataFrame for the heatmap with improved structure
    heatmap_data = df.copy()
    heatmap_data['Corrosion Resistance'] = heatmap_data['Corrosion Resistance'].map(corrosion_map)
    heatmap_data['Relative Cost'] = heatmap_data['Relative Cost'].map(cost_map)
    heatmap_data['Sustainability'] = heatmap_data['Sustainability'].map(sustainability_map)
    heatmap_data['Fatigue Resistance'] = heatmap_data['Fatigue Resistance'].map(fatigue_map)
    heatmap_data['Manufacturability'] = heatmap_data['Manufacturability'].map(manufacturability_map)
    
    # Select columns for the heatmap
    heatmap_cols = ['Corrosion Resistance', 'Relative Cost', 'Sustainability', 
                    'Fatigue Resistance', 'Manufacturability', 'Overall Rating']
    
    # Create the heatmap with improved style
    plt.figure(figsize=(12, 8))
    
    # Create a custom colormap for better visualization
    cmap = LinearSegmentedColormap.from_list('custom_cmap', ['#FFFFFF', '#0343DF'], N=256)
    
    # Set up the heatmap
    ax = plt.gca()
    heatmap = sns.heatmap(
        heatmap_data[heatmap_cols].set_index(heatmap_data['Material']),
        annot=True,
        cmap=cmap,
        linewidths=1,
        linecolor='white',
        cbar_kws={'label': 'Performance Score (Higher is Better)'},
        fmt='.1f',
        vmin=0,
        vmax=10,
        annot_kws={"fontsize": 10, "fontweight": "bold"}
    )
    
    # Customize the color bar
    cbar = heatmap.collections[0].colorbar
    cbar.ax.tick_params(labelsize=10)
    cbar.set_label('Performance Score', fontsize=12, fontweight='bold')
    
    # Customize the x-axis labels
    plt.xticks(rotation=45, ha='right', fontsize=11, fontweight='bold')
    plt.yticks(fontsize=11, fontweight='bold')
    
    # Improve title and layout
    plt.title('Materials Property Comparison for Ship Rudder Applications', fontsize=16, fontweight='bold', pad=20)
    
    # Add a descriptive legend
    legend_text = """
    Scoring Scale:
    • 10: Excellent performance
    • 7-9: Good performance
    • 4-6: Moderate performance
    • 1-3: Poor performance
    
    For cost, lower cost = higher score
    """
    plt.figtext(0.85, 0.15, legend_text, fontsize=9, 
                bbox=dict(facecolor='white', edgecolor='black', alpha=0.85, boxstyle='round,pad=0.5'))
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/materials_heatmap_improved.png', dpi=300, bbox_inches='tight')
    plt.close()

# Function to create combined visualization of all charts
def create_combined_visualization():
    # Create a large figure with subplots
    fig = plt.figure(figsize=(18, 14))
    gs = gridspec.GridSpec(2, 2, figure=fig, wspace=0.3, hspace=0.35)
    
    # 1. Ashby Chart
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    
    # Plot material ranges as ellipses
    for material in materials:
        width = 0.18
        height = material["yield_high"] - material["yield_low"]
        center_x = material["density"]
        center_y = (material["yield_high"] + material["yield_low"]) / 2
        
        ellipse = patches.Ellipse(
            (center_x, center_y), 
            width * center_x, 
            height * 0.7,
            facecolor=material["color"],
            alpha=0.8,
            edgecolor='black',
            linewidth=1.5,
            zorder=2
        )
        ax1.add_patch(ellipse)
        
        ax1.annotate(
            material["name"],
            (center_x, center_y),
            fontsize=9,
            ha='center',
            va='center',
            weight='bold',
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1),
            zorder=3
        )
    
    # Add guideline for constant specific strength
    x_values = np.logspace(3, 4, 100)
    for specific_strength in [0.01, 0.05, 0.1, 0.5]:
        y_values = specific_strength * x_values
        ax1.plot(x_values, y_values, '--', color='#555555', linewidth=1.2, zorder=1)
        ax1.annotate(
            f"σ/ρ = {specific_strength}",
            (x_values[-10], y_values[-10]),
            fontsize=8,
            color='#555555',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=1),
            rotation=38,
            zorder=3
        )
    
    ax1.set_xlabel('Density, ρ (kg/m³)', fontsize=11, weight='bold')
    ax1.set_ylabel('Yield Strength, σ (MPa)', fontsize=11, weight='bold')
    ax1.set_title('Ashby Chart: Yield Strength vs. Density', fontsize=13, fontweight='bold')
    ax1.set_xlim(1200, 12000)
    ax1.set_ylim(100, 2000)
    ax1.grid(True, which='both', linestyle='--', linewidth=0.8, alpha=0.6)
    ax1.xaxis.set_major_formatter(ScalarFormatter())
    ax1.yaxis.set_major_formatter(ScalarFormatter())
    
    # 2. Performance Index Chart (Top Right)
    ax2 = fig.add_subplot(gs[0, 1])
    
    # Get the specific strength index
    strength_to_weight = indices["Strength to Weight"]
    material_names = [m["name"] for m in materials]
    colors = [m["color"] for m in materials]
    
    # Sort materials by specific strength
    sorted_indices = np.argsort(strength_to_weight)[::-1]
    sorted_names = [material_names[i] for i in sorted_indices]
    sorted_values = [strength_to_weight[i] for i in sorted_indices]
    sorted_colors = [colors[i] for i in sorted_indices]
    
    y_pos = np.arange(len(sorted_names))
    bars = ax2.barh(
        y_pos,
        sorted_values,
        color=sorted_colors,
        alpha=0.9,
        edgecolor='black',
        linewidth=1,
        height=0.7
    )
    
    for j, bar in enumerate(bars):
        width = bar.get_width()
        ax2.text(
            width + 0.02,
            bar.get_y() + bar.get_height()/2,
            f'{sorted_values[j]:.3f}',
            ha='left',
            va='center',
            fontsize=9,
            fontweight='bold'
        )
    
    ax2.grid(True, axis='x', linestyle='--', alpha=0.7)
    ax2.set_axisbelow(True)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(sorted_names, fontsize=10)
    ax2.set_xlabel('Specific Strength (σ/ρ)', fontsize=11, weight='bold')
    ax2.set_title('Strength-to-Weight Ratio', fontsize=13, fontweight='bold')
    ax2.set_xlim(0, max(strength_to_weight) * 1.2)
    
    # 3. Heatmap (Bottom)
    ax3 = fig.add_subplot(gs[1, :])
    
    # Convert categorical data to numeric for visualization
    corrosion_map = {'Poor': 2, 'Moderate': 5, 'Good': 8, 'Excellent': 10}
    cost_map = {'Low': 9, 'Moderate': 6, 'High': 3, 'Very High': 1}
    sustainability_map = {'Variable': 5, 'Moderate': 6, 'High': 9}
    fatigue_map = {'Moderate': 5, 'Good': 8, 'Excellent': 10}
    manufacturability_map = {'Moderate': 5, 'Good': 8, 'Excellent': 10}
    
    # Create a new DataFrame for the heatmap
    heatmap_data = df.copy()
    heatmap_data['Corrosion Resistance'] = heatmap_data['Corrosion Resistance'].map(corrosion_map)
    heatmap_data['Relative Cost'] = heatmap_data['Relative Cost'].map(cost_map)
    heatmap_data['Sustainability'] = heatmap_data['Sustainability'].map(sustainability_map)
    heatmap_data['Fatigue Resistance'] = heatmap_data['Fatigue Resistance'].map(fatigue_map)
    heatmap_data['Manufacturability'] = heatmap_data['Manufacturability'].map(manufacturability_map)
    
    # Select columns for the heatmap
    heatmap_cols = ['Corrosion Resistance', 'Relative Cost', 'Sustainability', 
                    'Fatigue Resistance', 'Manufacturability', 'Overall Rating']
    
    # Create a custom colormap for better visualization
    cmap = LinearSegmentedColormap.from_list('custom_cmap', ['#FFFFFF', '#0343DF'], N=256)
    
    # Set up the heatmap
    sns.heatmap(
        heatmap_data[heatmap_cols].set_index(heatmap_data['Material']),
        annot=True,
        cmap=cmap,
        linewidths=1,
        linecolor='white',
        cbar_kws={'label': 'Performance Score (Higher is Better)'},
        fmt='.1f',
        vmin=0,
        vmax=10,
        annot_kws={"fontsize": 10, "fontweight": "bold"},
        ax=ax3
    )
    
    # Customize x-axis labels
    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha='right', fontsize=11, fontweight='bold')
    ax3.set_yticklabels(ax3.get_yticklabels(), fontsize=11, fontweight='bold')
    ax3.set_title('Materials Property Comparison', fontsize=13, fontweight='bold')
    
    # Add main title for the entire figure
    fig.suptitle('Comprehensive Materials Analysis for Ship Rudder Applications', 
                fontsize=16, fontweight='bold', y=0.98)
    
    # Add a legend explaining the analysis
    legend_text = """
    Key Findings:
    • CFRP offers the highest specific strength but at higher cost
    • Stainless Steel 316L provides excellent corrosion resistance
    • Aluminum offers good balance of properties at moderate cost
    • Material selection depends on specific application requirements
    """
    plt.figtext(0.5, 0.01, legend_text, fontsize=10, ha='center', 
                bbox=dict(facecolor='#f0f0f0', edgecolor='gray', alpha=0.9, boxstyle='round,pad=0.5'))
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(f'{output_dir}/comprehensive_materials_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

# Create all visualizations
print("Creating Ashby Chart...")
create_ashby_chart()

print("Creating Performance Index Chart...")
create_performance_index_chart()

print("Creating Materials Heatmap...")
create_materials_heatmap()

print("Creating Combined Visualization...")
create_combined_visualization()

print(f"All visualizations have been saved to the '{output_dir}' directory.")
print("Generated files:")
print(f"1. {output_dir}/ashby_chart_improved.png")
print(f"2. {output_dir}/performance_indices_improved.png")
print(f"3. {output_dir}/materials_heatmap_improved.png")
print(f"4. {output_dir}/comprehensive_materials_analysis.png")
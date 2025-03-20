import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms

# Define the materials data
materials = {
    'Mild Steel': {
        'density': 7850,  # kg/m³
        'yield_strength': (250 + 400) / 2,  # MPa (using midpoint)
        'youngs_modulus': 200,  # GPa
        'fracture_toughness': (50 + 100) / 2,  # MPa√m (using midpoint)
        'max_service_temp': 400,  # °C
        'relative_cost': 1.0,  # arbitrary units
        'color': 'red',
        'label': 'Mild Steel'
    },
    'Stainless Steel 316L': {
        'density': 8000,
        'yield_strength': (250 + 550) / 2,
        'youngs_modulus': 200,
        'fracture_toughness': (50 + 100) / 2,
        'max_service_temp': 870,
        'relative_cost': 1.5,
        'color': 'darkred',
        'label': 'Stainless Steel 316L'
    },
    'Aluminum Alloy 5083': {
        'density': 2600,
        'yield_strength': (200 + 350) / 2,
        'youngs_modulus': 70,
        'fracture_toughness': (20 + 30) / 2,
        'max_service_temp': 200,
        'relative_cost': 1.2,
        'color': 'orange',
        'label': 'Al Alloy 5083'
    },
    'Titanium Alloy': {
        'density': 4430,
        'yield_strength': (800 + 1100) / 2,
        'youngs_modulus': 110,
        'fracture_toughness': (50 + 100) / 2,
        'max_service_temp': 200,
        'relative_cost': 5.0,
        'color': 'purple',
        'label': 'Ti-6Al-4V'
    },
    'CFRP': {
        'density': 1600,
        'yield_strength': (600 + 1500) / 2,
        'youngs_modulus': (70 + 150) / 2,
        'fracture_toughness': (20 + 50) / 2,
        'max_service_temp': 600,
        'relative_cost': 4.0,
        'color': 'brown',
        'label': 'CFRP'
    },
    'GFRP': {
        'density': 2000,
        'yield_strength': (250 + 600) / 2,
        'youngs_modulus': (20 + 50) / 2,
        'fracture_toughness': (15 + 40) / 2,
        'max_service_temp': 250,
        'relative_cost': 1.8,
        'color': 'green',
        'label': 'GFRP'
    }
}

# Function to create confidence ellipse for material properties
def confidence_ellipse(x, y, ax, width, height, angle=0, color='blue', alpha=0.3, label=None):
    """
    Create a confidence ellipse for a material property
    """
    ellipse = Ellipse((x, y), width=width, height=height, angle=angle, 
                      facecolor=color, alpha=alpha, edgecolor=color, linewidth=2)
    ax.add_patch(ellipse)
    
    # Add a label at the center of the ellipse
    if label:
        ax.text(x, y, label, horizontalalignment='center', 
                verticalalignment='center', color='black', fontweight='bold')

# Function to plot material properties on Ashby Charts
def plot_on_ashby_chart(chart_type, materials):
    """
    Plot material properties on the specified Ashby chart type
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Set properties based on chart type
    if chart_type == "modulus_density":
        x_property = 'density'
        y_property = 'youngs_modulus'
        x_label = 'Density, ρ (kg/m³)'
        y_label = 'Young\'s Modulus, E (GPa)'
        title = 'Young\'s Modulus vs Density'
        x_scale = 'log'
        y_scale = 'log'
        
    elif chart_type == "strength_density":
        x_property = 'density'
        y_property = 'yield_strength'
        x_label = 'Density, ρ (kg/m³)'
        y_label = 'Yield Strength, σf (MPa)'
        title = 'Strength vs Density'
        x_scale = 'log'
        y_scale = 'log'
        
    elif chart_type == "modulus_cost":
        x_property = 'relative_cost'
        y_property = 'youngs_modulus'
        x_label = 'Relative Cost per Unit Volume, CRρ (a.u.)'
        y_label = 'Young\'s Modulus, E (GPa)'
        title = 'Modulus vs Relative Cost'
        x_scale = 'log'
        y_scale = 'log'
        
    elif chart_type == "toughness_modulus":
        x_property = 'youngs_modulus'
        y_property = 'fracture_toughness'
        x_label = 'Young\'s Modulus, E (GPa)'
        y_label = 'Fracture Toughness, KIC (MPa√m)'
        title = 'Fracture Toughness vs Modulus'
        x_scale = 'log'
        y_scale = 'log'
        
    elif chart_type == "specific_properties":
        # For specific properties (E/ρ vs σf/ρ)
        x_property = 'specific_strength'
        y_property = 'specific_modulus'
        x_label = 'Specific Strength, σf/ρ (MPa/(kg/m³))'
        y_label = 'Specific Modulus, E/ρ (GPa/(kg/m³))'
        title = 'Specific Modulus vs Specific Strength'
        x_scale = 'log'
        y_scale = 'log'
        
    elif chart_type == "strength_temp":
        x_property = 'max_service_temp'
        y_property = 'yield_strength'
        x_label = 'Maximum Service Temperature, Tmax (°C)'
        y_label = 'Yield Strength, σf (MPa)'
        title = 'Strength vs Max Service Temperature'
        x_scale = 'log'
        y_scale = 'log'
    
    # Calculate specific properties for specific_properties chart
    if chart_type == "specific_properties":
        for material in materials.values():
            material['specific_strength'] = material['yield_strength'] / material['density']
            material['specific_modulus'] = material['youngs_modulus'] / material['density']
    
    # Plot data points for each material
    for name, material in materials.items():
        if chart_type == "specific_properties":
            x = material['specific_strength']
            y = material['specific_modulus']
        else:
            x = material[x_property]
            y = material[y_property]
        
        # Calculate variation range for ellipse dimensions (using 20% as example)
        x_width = x * 0.3
        y_height = y * 0.3
        
        # Plot confidence ellipse
        confidence_ellipse(x, y, ax, width=x_width, height=y_height, 
                          color=material['color'], alpha=0.5, label=material['label'])
    
    # Set chart properties
    ax.set_xscale(x_scale)
    ax.set_yscale(y_scale)
    ax.set_xlabel(x_label, fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.grid(True, which="both", ls="--", alpha=0.3)
    
    # Add legend based on colors
    legend_patches = [plt.Rectangle((0, 0), 1, 1, color=material['color'], alpha=0.5) 
                      for material in materials.values()]
    ax.legend(legend_patches, [material['label'] for material in materials.values()], 
              loc='upper left', fontsize=10)
    
    # Add guideline lines for minimum mass design (if relevant)
    if chart_type == "modulus_density" or chart_type == "strength_density":
        # Add guideline for E/ρ
        x_vals = np.logspace(np.log10(min([m['density'] for m in materials.values()])*0.8), 
                             np.log10(max([m['density'] for m in materials.values()])*1.2), 10)
        y_vals = x_vals  # E/ρ = constant line (just an example)
        ax.plot(x_vals, y_vals, '--', color='black', alpha=0.5, label='E/ρ guideline')
    
    plt.tight_layout()
    return fig, ax

# Generate all charts
chart_types = [
    "modulus_density",
    "strength_density",
    "modulus_cost",
    "toughness_modulus",
    "specific_properties",
    "strength_temp"
]

# Create and display each chart
for chart_type in chart_types:
    fig, ax = plot_on_ashby_chart(chart_type, materials)
    plt.savefig(f'ashby_chart_{chart_type}.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

# Function to analyze and rank materials for ship rudder application
def analyze_rudder_materials(materials):
    """
    Analyze materials for ship rudder application based on key performance indices
    """
    # Define performance indices and their weights
    indices = {
        'strength_to_weight': 0.25,  # Yield strength / density
        'corrosion_resistance': 0.25,  # Qualitative score based on material type
        'cost_effectiveness': 0.20,  # Inverse of relative cost
        'fracture_resistance': 0.15,  # Fracture toughness
        'thermal_stability': 0.15,  # Max service temperature
    }
    
    # Define corrosion resistance scores (qualitative based on material properties)
    corrosion_scores = {
        'Mild Steel': 2,            # Poor without coating
        'Stainless Steel 316L': 9,  # Excellent
        'Aluminum Alloy 5083': 7,   # Good
        'Titanium Alloy': 10,       # Excellent
        'CFRP': 9,                  # Excellent
        'GFRP': 8,                  # Very good
    }
    
    # Calculate normalized performance for each index and material
    performance = {}
    
    # Strength to weight ratio
    stw_values = {name: mat['yield_strength']/mat['density'] for name, mat in materials.items()}
    max_stw = max(stw_values.values())
    for name, value in stw_values.items():
        if name not in performance:
            performance[name] = {}
        performance[name]['strength_to_weight'] = value / max_stw
    
    # Corrosion resistance
    max_corr = max(corrosion_scores.values())
    for name, value in corrosion_scores.items():
        performance[name]['corrosion_resistance'] = value / max_corr
    
    # Cost effectiveness
    cost_eff = {name: 1/mat['relative_cost'] for name, mat in materials.items()}
    max_cost = max(cost_eff.values())
    for name, value in cost_eff.items():
        performance[name]['cost_effectiveness'] = value / max_cost
    
    # Fracture resistance
    frac_values = {name: mat['fracture_toughness'] for name, mat in materials.items()}
    max_frac = max(frac_values.values())
    for name, value in frac_values.items():
        performance[name]['fracture_resistance'] = value / max_frac
    
    # Thermal stability
    temp_values = {name: mat['max_service_temp'] for name, mat in materials.items()}
    max_temp = max(temp_values.values())
    for name, value in temp_values.items():
        performance[name]['thermal_stability'] = value / max_temp
    
    # Calculate weighted total performance
    totals = {}
    for name, indices_perf in performance.items():
        totals[name] = sum(value * indices[index] for index, value in indices_perf.items())
    
    # Rank materials
    ranked_materials = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    
    return ranked_materials, performance

# Analyze and rank materials
ranked_materials, performance = analyze_rudder_materials(materials)

# Print analysis results
print("Materials Ranking for Ship Rudder Application:")
for i, (name, score) in enumerate(ranked_materials):
    print(f"{i+1}. {name}: {score:.4f}")

# Create a visualization of performance indices
def plot_performance_radar(materials, performance, ranked_materials):
    """
    Create radar chart to visualize performance indices for all materials
    """
    import matplotlib.pyplot as plt
    import numpy as np
    
    # Get the indices and material names
    indices = list(next(iter(performance.values())).keys())
    num_indices = len(indices)
    
    # Create angle for each index
    angles = np.linspace(0, 2*np.pi, num_indices, endpoint=False).tolist()
    angles += angles[:1]  # Close the loop
    
    # Create radar plot
    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(polar=True))
    
    # Plot each material
    for name, mat_data in materials.items():
        values = [performance[name][idx] for idx in indices]
        values += values[:1]  # Close the loop
        
        ax.plot(angles, values, linewidth=2, label=name, color=mat_data['color'])
        ax.fill(angles, values, alpha=0.1, color=mat_data['color'])
    
    # Set category labels
    plt.xticks(angles[:-1], indices, fontsize=12)
    
    # Set radial labels
    ax.set_rlabel_position(0)
    plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0], ["0.2", "0.4", "0.6", "0.8", "1.0"], 
               fontsize=10, color="grey")
    plt.ylim(0, 1)
    
    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    plt.title("Material Performance Comparison for Ship Rudder", size=15)
    plt.tight_layout()
    
    return fig, ax

# Create radar chart for performance comparison
fig, ax = plot_performance_radar(materials, performance, ranked_materials)
plt.savefig('material_performance_radar.png', dpi=300, bbox_inches='tight')
plt.close(fig)

# Create bar chart for overall performance scores
def plot_overall_performance(ranked_materials, materials):
    """
    Create bar chart to visualize overall performance scores
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    names = [name for name, _ in ranked_materials]
    scores = [score for _, score in ranked_materials]
    colors = [materials[name]['color'] for name, _ in ranked_materials]
    
    # Create bar chart
    bars = ax.bar(names, scores, color=colors, alpha=0.7)
    
    # Add labels and title
    ax.set_xlabel('Materials', fontsize=12)
    ax.set_ylabel('Overall Performance Score', fontsize=12)
    ax.set_title('Overall Performance Ranking for Ship Rudder Materials', fontsize=14)
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom', fontsize=10)
    
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, max(scores) * 1.1)  # Add some padding at the top
    plt.tight_layout()
    
    return fig, ax

# Create overall performance bar chart
fig, ax = plot_overall_performance(ranked_materials, materials)
plt.savefig('material_overall_performance.png', dpi=300, bbox_inches='tight')
plt.close(fig)

print("\nAnalysis complete. All visualization files have been saved.")
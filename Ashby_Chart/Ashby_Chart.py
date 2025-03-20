import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# --- Step 1: Load and analyze the image ---
chart_img_path = 'Ashby_Chart/ashby_chart1.png'  # Update this with your actual chart image path

try:
    chart_img = Image.open(chart_img_path)
except Exception as e:
    print(f"Error opening image: {e}")
    exit()

# Convert image to numpy array for plotting and get resolution (width, height)
img_array = np.array(chart_img)
img_width, img_height = chart_img.size
print(f"Image resolution: {img_width} x {img_height}")

# --- Step 2: Calibrate the image by clicking two reference points ---
# Display the image and let the user click the bottom-left and top-right calibration points.
plt.figure(figsize=(10, 8))
plt.imshow(img_array)
plt.title("Click on two calibration points:\n 1. Bottom-left of data area\n 2. Top-right of data area")
calibration_pts = plt.ginput(2, timeout=-1)  # Wait indefinitely until two points are clicked
plt.close()

if len(calibration_pts) < 2:
    print("Calibration points not provided. Exiting.")
    exit()

# Convert calibration points to numpy arrays
pt_img_bl = np.array(calibration_pts[0])  # Assumed to be bottom-left pixel coordinate
pt_img_tr = np.array(calibration_pts[1])  # Assumed to be top-right pixel coordinate

# --- Step 3: Input the corresponding data values ---
# For example, if the chart shows Density on the x-axis and Young's modulus on the y-axis,
# you might know that at the bottom-left, x = X_min and y = Y_min, and at the top-right, x = X_max and y = Y_max.
print("Enter the data coordinates for the calibration points.")
bl_input = input("Bottom-left (x y): ").strip().split()
tr_input = input("Top-right (x y): ").strip().split()
try:
    data_bl = np.array([float(bl_input[0]), float(bl_input[1])])
    data_tr = np.array([float(tr_input[0]), float(tr_input[1])])
except Exception as e:
    print(f"Error parsing calibration data: {e}")
    exit()

# --- Step 4: Create the mapping function from data to pixel coordinates ---
def data_to_pixel(x_data, y_data):
    """
    Maps data coordinates (x_data, y_data) to image pixel coordinates.
    Assumes a linear relationship between the two calibration points.
    
    Note: This mapping is based on the assumption that the data area is a rectangle in the image.
    For log-scaled charts, apply the log conversion to x_data and/or y_data as needed.
    """
    # Compute scaling factors for x and y:
    scale_x = (pt_img_tr[0] - pt_img_bl[0]) / (data_tr[0] - data_bl[0])
    scale_y = (pt_img_bl[1] - pt_img_tr[1]) / (data_tr[1] - data_bl[1])  # y increases downward in pixel space

    # Map the data point to pixel coordinates:
    pixel_x = pt_img_bl[0] + (x_data - data_bl[0]) * scale_x
    pixel_y = pt_img_bl[1] - (y_data - data_bl[1]) * scale_y  # subtract because pixel y axis is top-down
    return pixel_x, pixel_y

# --- Step 5: Define the material data and overlay markers on the image ---
# Material properties: using mid-range values as before
materials = {
    'Mild Steel (Carbon Steel)': {
        'density': 7850,            # kg/m³
        'yield_strength': (250+400)/2,   # MPa
        'youngs_modulus': 200,      # GPa
        'fracture_toughness': (50+100)/2, # MPa√m
        'max_service_temp': 400,    # °C
        'relative_cost': 1.0,
        'color': 'blue',
        'marker': 'o'
    },
    'Stainless Steel (316L)': {
        'density': 8000,
        'yield_strength': (250+550)/2,
        'youngs_modulus': 200,
        'fracture_toughness': (50+100)/2,
        'max_service_temp': 870,
        'relative_cost': 1.5,
        'color': 'orange',
        'marker': 'o'
    },
    'Marine-Grade Aluminum Alloy (5083)': {
        'density': 2600,
        'yield_strength': (200+350)/2,
        'youngs_modulus': 70,
        'fracture_toughness': (20+30)/2,
        'max_service_temp': 200,
        'relative_cost': 1.2,
        'color': 'green',
        'marker': 'o'
    },
    'Titanium Alloy (Ti-6Al-4V)': {
        'density': 4430,
        'yield_strength': (800+1100)/2,
        'youngs_modulus': 110,
        'fracture_toughness': (50+100)/2,
        'max_service_temp': 200,
        'relative_cost': 5.0,
        'color': 'purple',
        'marker': 'o'
    },
    'CFRP': {
        'density': 1600,
        'yield_strength': (600+1500)/2,
        'youngs_modulus': (70+150)/2,
        'fracture_toughness': (20+50)/2,
        'max_service_temp': 600,
        'relative_cost': 4.0,
        'color': 'red',
        'marker': 'o'
    },
    'GFRP': {
        'density': 2000,
        'yield_strength': (250+600)/2,
        'youngs_modulus': (20+50)/2,
        'fracture_toughness': (15+40)/2,
        'max_service_temp': 250,
        'relative_cost': 1.8,
        'color': 'brown',
        'marker': 'o'
    }
}

# (Optional) Compute specific properties if needed:
for mat in materials.values():
    mat['specific_strength'] = mat['yield_strength'] / mat['density']
    mat['specific_modulus'] = mat['youngs_modulus'] / mat['density']

# Example: Assume we want to overlay markers for "density" vs "youngs_modulus"
# (If your chart is different, adjust the properties accordingly.)
x_property = 'density'
y_property = 'youngs_modulus'

# NOTE: If your chart expects density in Mg/m³, do the conversion:
def convert_units(prop, value):
    if prop == 'density':
        return value / 1000  # kg/m³ to Mg/m³
    return value

plt.figure(figsize=(10, 8))
plt.imshow(img_array)

# Overlay markers for each material using the calibration mapping
for material, props in materials.items():
    # Get the data values and convert units if necessary:
    x_data = convert_units(x_property, props.get(x_property))
    y_data = props.get(y_property)
    
    # For log–scaled charts, you might do:
    # x_data = np.log10(x_data) if x_property == 'density' else x_data
    # y_data = np.log10(y_data) if y_property == 'youngs_modulus' else y_data
    
    # Map data coordinates to pixel coordinates:
    px, py = data_to_pixel(x_data, y_data)
    
    # Plot the marker and annotate:
    plt.scatter(px, py, color=props['color'], marker=props['marker'], s=150,
                edgecolors='black', zorder=10, alpha=0.8)
    plt.annotate(material, (px, py), xytext=(5, 5), textcoords='offset points',
                 fontsize=9, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

plt.title(f"Overlay of Materials on Ashby Chart\n({y_property.replace('_', ' ').title()} vs {x_property.replace('_', ' ').title()})")
plt.axis('off')  # Hide axis if desired
plt.tight_layout()
plt.show()

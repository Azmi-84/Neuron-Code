import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define a complex function, e.g., f(z) = 1/z
def f(z):
    return 1 / z

# Create a grid of complex numbers with higher resolution for precision
x = np.linspace(-2, 2, 500)
y = np.linspace(-2, 2, 500)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y

# Avoid division by zero with a small epsilon
epsilon = 1e-10
mask = np.abs(Z) < epsilon
Z[mask] = np.nan

# Compute |f(z)|
F = np.abs(f(Z))

# Create a figure with two subplots: 2D and 3D
fig = plt.figure(figsize=(15, 7))

# 2D heatmap plot with improved precision
ax1 = fig.add_subplot(121)
heatmap = ax1.pcolormesh(X, Y, F, shading='auto', cmap='viridis', norm=plt.Normalize(vmin=0, vmax=5))
ax1.set_title('2D Magnitude of f(z) = 1/z')
ax1.set_xlabel('Re(z)')
ax1.set_ylabel('Im(z)')
ax1.axhline(0, color='white', lw=0.5)
ax1.axvline(0, color='white', lw=0.5)
ax1.grid(True, linestyle='--', alpha=0.5)
fig.colorbar(heatmap, ax=ax1, label='|f(z)|')

# 3D surface plot
ax2 = fig.add_subplot(122, projection='3d')
# For better visualization, clip very large values
F_clipped = np.clip(F, 0, 5)
surface = ax2.plot_surface(X, Y, F_clipped, cmap='plasma', 
                          rstride=5, cstride=5, 
                          linewidth=0, antialiased=True)
ax2.set_title('3D Magnitude of f(z) = 1/z')
ax2.set_xlabel('Re(z)')
ax2.set_ylabel('Im(z)')
ax2.set_zlabel('|f(z)|')
ax2.view_init(30, 45)  # Set viewing angle
fig.colorbar(surface, ax=ax2, shrink=0.5, aspect=10, label='|f(z)|')

plt.tight_layout()
plt.savefig('/home/abdullahalazmi/Programming/Neuron_Code/complex_function_3d.png', dpi=300)
plt.show()

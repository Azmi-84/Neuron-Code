import numpy as np
import matplotlib.pyplot as plt

# Circuit parameters
Vin = 10.0  # Input voltage (V)
R = 50e3    # Resistance (Ω)
C = 100e-6  # Capacitance (F)
RC = R * C  # Time constant (s)
V_sat_pos = 12.0  # Positive saturation voltage (V)
V_sat_neg = -12.0  # Negative saturation voltage (V)

# Time parameters
t_max = 10  # Maximum simulation time (s)
dt = 0.01   # Time step (s)
time = np.arange(0, t_max, dt)  # Time array

# Initialize output voltage array
Vout = np.zeros_like(time)

# Calculate output voltage
for i, t in enumerate(time):
    # Ideal integrator equation: Vout = - (Vin/(R*C)) * t
    Vout[i] = - (Vin / RC) * t
    
    # Apply saturation limits
    if Vout[i] >= V_sat_pos:
        Vout[i] = V_sat_pos
    elif Vout[i] <= V_sat_neg:
        Vout[i] = V_sat_neg
        saturation_time = t
        break  # Stop simulation when negative saturation is reached

# Truncate arrays to saturation point
time = time[:i+1]
Vout = Vout[:i+1]

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(time, Vout, linewidth=2)
plt.axhline(y=V_sat_neg, color='r', linestyle='--', label='Negative Saturation')
plt.axhline(y=V_sat_pos, color='g', linestyle='--', label='Positive Saturation')
plt.axvline(x=saturation_time, color='k', linestyle=':', label=f'Saturation at {saturation_time:.2f} s')

plt.title('Op-Amp Integrator Output Voltage vs Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Output Voltage (V)')
plt.grid(True)
plt.legend()
plt.show()

print(f"The op-amp saturates at {V_sat_neg} V after {saturation_time:.2f} seconds")
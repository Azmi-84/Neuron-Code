import numpy as np
import matplotlib.pyplot as plt

# Analog signal (1 Hz sine wave)
t_continuous = np.linspace(0, 1, 1000)
x_analog = np.sin(2 * np.pi * t_continuous)

# Sampling (Discrete-time)
fs = 10  # Sampling frequency (Hz)
t_samples = np.arange(0, 1, 1/fs)
x_discrete = np.sin(2 * np.pi * t_samples)

# Quantization (3-bit ADC → 8 levels)
n_bits = 3
quant_levels = 2 ** n_bits
x_digital = np.round((x_discrete + 1) * (quant_levels - 1)/2)  # Scale to 0-7

# Plot
plt.figure(figsize=(12, 4))
plt.plot(t_continuous, x_analog, label='Analog (Continuous-Time)')
plt.stem(t_samples, x_discrete, linefmt='r-', markerfmt='ro', label='Discrete-Time (Sampled)')
plt.step(t_samples, (2 * x_digital / (quant_levels - 1)) - 1, 'g-', where='post', label='Digital (Quantized)')  # Rescale to [-1, 1]
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.legend()
plt.title('Analog → Discrete-Time → Digital Conversion')
plt.grid(True)
plt.show()
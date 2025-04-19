import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

# Parameters
f_continuous = 5  # Frequency of the analog signal (Hz)
t_max = 1         # Duration of the signal (seconds)
fs_low = 6        # Low sampling rate (causes aliasing)
fs_high = 20      # High sampling rate (Nyquist-compliant)

# Generate continuous-time signal
t_continuous = np.linspace(0, t_max, 1000)  # High-resolution time axis
x_continuous = np.sin(2 * np.pi * f_continuous * t_continuous)

# Sample the signal at two different rates
def sample_signal(fs):
    t_samples = np.arange(0, t_max, 1/fs)  # Discrete time points
    x_samples = np.sin(2 * np.pi * f_continuous * t_samples)
    return t_samples, x_samples

t_low, x_low = sample_signal(fs_low)    # Under-sampled
t_high, x_high = sample_signal(fs_high) # Properly sampled

# Compute FFTs for frequency analysis
def compute_fft(x, fs):
    N = len(x)
    yf = fft(x)
    xf = fftfreq(N, 1/fs)[:N//2]  # Positive frequencies only
    return xf, 2/N * np.abs(yf[0:N//2])

xf_cont, yf_cont = compute_fft(x_continuous, 1000)  # Approx. "true" spectrum
xf_low, yf_low = compute_fft(x_low, fs_low)
xf_high, yf_high = compute_fft(x_high, fs_high)

# Plotting
plt.figure(figsize=(12, 8))

# Time Domain: Continuous vs. Sampled
plt.subplot(2, 2, 1)
plt.plot(t_continuous, x_continuous, label='Continuous Signal')
plt.stem(t_low, x_low, linefmt='r-', markerfmt='ro', basefmt=' ', label=f'Samples (fs={fs_low} Hz)')
plt.title('Time Domain (Under-Sampled)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(t_continuous, x_continuous, label='Continuous Signal')
plt.stem(t_high, x_high, linefmt='g-', markerfmt='go', basefmt=' ', label=f'Samples (fs={fs_high} Hz)')
plt.title('Time Domain (Properly Sampled)')
plt.xlabel('Time (s)')
plt.legend()

# Frequency Domain: FFTs
plt.subplot(2, 2, 3)
plt.plot(xf_cont, yf_cont, label='Continuous Signal Spectrum')
plt.plot(xf_low, yf_low, 'r-', label=f'Sampled (fs={fs_low} Hz)')
plt.axvline(fs_low/2, color='k', linestyle='--', label='Nyquist Frequency (fs/2)')
plt.title('Frequency Domain (Aliasing)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.legend()

plt.subplot(2, 2, 4)
plt.plot(xf_cont, yf_cont, label='Continuous Signal Spectrum')
plt.plot(xf_high, yf_high, 'g-', label=f'Sampled (fs={fs_high} Hz)')
plt.axvline(fs_high/2, color='k', linestyle='--', label='Nyquist Frequency (fs/2)')
plt.title('Frequency Domain (No Aliasing)')
plt.xlabel('Frequency (Hz)')
plt.legend()

plt.tight_layout()
plt.show()
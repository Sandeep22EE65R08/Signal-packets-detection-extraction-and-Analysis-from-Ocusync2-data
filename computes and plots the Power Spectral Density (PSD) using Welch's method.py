import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch, hamming

def plot_psd(ocusync2_data, fs=50e6, nfft_welch=8192):
    """
    This function computes and plots the Power Spectral Density (PSD) using Welch's method.
    
    Parameters:
    - ocusync2_data: Input signal data (numpy array)
    - fs: Sampling frequency (default is 50 MHz)
    - nfft_welch: Number of FFT points for Welch's method (default is 8192)
    """
    # Ensure data length is sufficient for Welch's method
    if len(ocusync2_data) < nfft_welch:
        print("Insufficient data length for Welch's method")
        return

    # Apply Hamming window
    window = hamming(len(ocusync2_data))
    data_windowed = ocusync2_data * window

    # Calculate PSD using Welch's method
    f, Pxx_den = welch(
        data_windowed, fs, nperseg=nfft_welch, return_onesided=False
    )

    # Shift frequency and PSD for negative frequencies
    Pxx_den_shifted_data = np.fft.fftshift(Pxx_den)
    f_shifted_data = np.fft.fftshift(f)

    # Calculate the mean PSD value
    mean_psd_value = np.mean(Pxx_den_shifted_data)
    print(f"Mean PSD Value: {mean_psd_value:.2e} V^2/Hz")

    # Plot the PSD
    plt.figure(figsize=(20, 6))
    plt.semilogy(f_shifted_data / 1e6, Pxx_den_shifted_data)  # Convert frequency to MHz
    plt.axhline(1.1 * Pxx_den_shifted_data.mean(), color='r', linestyle='--', label="Mean PSD")
    plt.xlabel("Frequency [MHz]")
    plt.ylabel("PSD [V**2/Hz]")
    plt.title("Power Spectral Density (PSD)")
    plt.legend()
    
    plt.show()

# Example usage:
plot_psd(ocusync2_data)

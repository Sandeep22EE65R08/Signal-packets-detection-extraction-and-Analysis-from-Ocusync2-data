from scipy.signal import welch, hamming
import numpy as np
import matplotlib.pyplot as plt

def compute_and_plot_psd(ocusync2_data, packets, fs=50e6, nfft_welch=2028, band_found=True, offset=0):
    """
    Computes and plots the Power Spectral Density (PSD) for each detected packet after 
    frequency offset correction and filtering.

    Parameters:
    - ocusync2_data: The input signal data (numpy array)
    - packets: A list of tuples (start_idx, end_idx) indicating detected packet indices
    - fs: Sampling frequency (default is 50 MHz)
    - nfft_welch: Number of FFT points for Welch's method (default is 2028)
    - band_found: Boolean indicating if a suitable band was found for correction (default True)
    - offset: Frequency offset to correct (default 0)
    """
    for idx, (start_idx, end_idx) in enumerate(packets, start=1):
        # Extract corresponding signal samples for the packet
        current_packet = ocusync2_data[start_idx:end_idx]

        # Correct the frequency offset for the packet
        if band_found:
            corrected_packet = DroneSignalProcessor.fshift(current_packet, -offset, fs)

            # Ensure data length is sufficient for Welch's method
            if len(corrected_packet) < nfft_welch:
                print(f"Insufficient data length for Welch's method in Packet {idx}")
                continue

            # Apply Hamming window
            window = hamming(len(corrected_packet))
            data_windowed = corrected_packet * window

            # Calculate PSD using Welch's method
            f, Pxx_den = welch(data_windowed, fs, nperseg=nfft_welch, return_onesided=False)

            # Shift frequency and PSD for negative frequencies
            Pxx_den_shifted = np.fft.fftshift(Pxx_den)
            f_shifted = np.fft.fftshift(f)

            # Calculate the mean PSD value
            mean_psd_value = np.mean(Pxx_den_shifted)
            print(f"Mean PSD Value for Packet {idx}: {mean_psd_value:.2e} V^2/Hz")

            # Plot the PSD
            plt.figure(figsize=(20, 6))
            plt.semilogy(f_shifted / 1e6, Pxx_den_shifted)  # Convert frequency to MHz
            plt.axhline(1.1 * Pxx_den_shifted.mean(), color='r', linestyle='--', label="Mean PSD")
            plt.xlabel("Frequency [MHz]")
            plt.ylabel("PSD [V**2/Hz]")
            plt.title(f"Power Spectral Density (PSD) of Filtered Packet {idx}")
            plt.legend()
            plt.show()
        else:
            print(f"Packet {idx}: No suitable band found for offset correction.")

# Example usage:
compute_and_plot_psd(ocusync2_data, packets, fs=50e6, nfft_welch=2028, band_found=True, offset=offset)

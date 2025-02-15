import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch, hamming

def integrate_power(frequencies, psd, band):
    """Integrate power over a specified frequency band."""
    indices = (frequencies >= band[0]) & (frequencies <= band[1])
    return np.trapz(psd[indices], frequencies[indices])

def compute_snr_and_plot_psd(processor, ocusync2_data, packets, fs=50e6, nfft_welch=2048):
    """
    Computes the SNR and plots the Power Spectral Density (PSD) for extracted packets after 
    frequency offset correction and filtering.

    Parameters:
    - processor: Signal processing object containing the frequency offset correction method.
    - ocusync2_data: Raw signal data (numpy array).
    - packets: List of tuples (start_idx, end_idx) indicating detected packet indices.
    - fs: Sampling frequency in Hz (default is 50 MHz).
    - nfft_welch: Number of FFT points for Welch's method (default is 2048).
    """

    # Signal and noise band definitions
    signal_band = (-8.5e6, 8.5e6)  # Signal is centered around 0 Hz
    noise_band_lower = (-25e6, -8.5e6)
    noise_band_upper = (8.5e6, 25e6)

    for idx, (start_idx, end_idx) in enumerate(packets, start=1):
        current_packet = ocusync2_data[start_idx:end_idx]

        # Estimate frequency offset
        offset, band_found = processor.estimate_offset(current_packet, fs, packet_type="droneid")

        if band_found:
            # Apply frequency shift correction
            corrected_packet = DroneSignalProcessor.fshift(current_packet, -offset, fs)

            # Apply DFT-based low-pass filter
            filtered_packet = dft_filter(corrected_packet, 8.5e6, fs)

            # Ensure sufficient data length for Welch's method
            if len(filtered_packet) < nfft_welch:
                print(f"Packet {idx}: Insufficient data length for Welch's method.")
                continue

            # Apply Hamming window
            window = hamming(len(filtered_packet))
            data_windowed = filtered_packet * window

            # Compute PSD using Welch's method
            f, Pxx_den = welch(data_windowed, fs, nperseg=nfft_welch, return_onesided=False)
            Pxx_den_shifted = np.fft.fftshift(Pxx_den)
            f_shifted = np.fft.fftshift(f)

            # Compute signal and noise power
            signal_power = integrate_power(f_shifted, Pxx_den_shifted, signal_band)
            noise_power_lower = integrate_power(f_shifted, Pxx_den_shifted, noise_band_lower)
            noise_power_upper = integrate_power(f_shifted, Pxx_den_shifted, noise_band_upper)
            total_noise_power = noise_power_lower + noise_power_upper

            # Compute SNR in dB
            snr = signal_power / total_noise_power
            snr_dB = 10 * np.log10(snr)
            print(f"Packet {idx}: SNR = {snr_dB:.2f} dB")

            # Plot PSD
            plt.figure(figsize=(10, 4))
            plt.semilogy(f_shifted / 1e6, Pxx_den_shifted, label="PSD")
            plt.axhline(1.1 * np.mean(Pxx_den_shifted), color='r', linestyle='--', label="Mean PSD")
            plt.axvspan(signal_band[0] / 1e6, signal_band[1] / 1e6, color='green', alpha=0.3, label="Signal Band")
            plt.axvspan(noise_band_lower[0] / 1e6, noise_band_lower[1] / 1e6, color='red', alpha=0.3, label="Noise Band Lower")
            plt.axvspan(noise_band_upper[0] / 1e6, noise_band_upper[1] / 1e6, color='blue', alpha=0.3, label="Noise Band Upper")
            plt.xlabel("Frequency [MHz]")
            plt.ylabel("PSD [V^2/Hz]")
            plt.title(f"Power Spectral Density (PSD) of Filtered Packet {idx}")
            plt.legend()
            plt.grid(True)
            plt.show()
        else:
            print(f"Packet {idx}: No suitable band found for offset correction.")

# Example usage:
compute_snr_and_plot_psd(processor, ocusync2_data, packets)

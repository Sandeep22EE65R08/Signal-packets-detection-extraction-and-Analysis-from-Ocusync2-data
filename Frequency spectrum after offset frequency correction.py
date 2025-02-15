import numpy as np
import matplotlib.pyplot as plt

def plot_corrected_packet_spectra(corrected_packet, packets, fs=50e6, N_fft=2048):
    """
    This function computes and plots the frequency spectrum of frequency-corrected signal packets.
    
    Parameters:
    - corrected_packet: The frequency-corrected signal data (numpy array)
    - packets: A list of tuples (start_idx, end_idx) indicating detected packet indices
    - fs: Sampling frequency (default is 50 MHz)
    - N_fft: Number of FFT points (default is 2048)
    """
    for idx, (start_idx, end_idx) in enumerate(packets, start=1):
        # Extract corresponding signal samples for the packet
        current_packet = corrected_packet[start_idx:end_idx]

        # Compute FFT and shift zero frequency component to the center
        data_fft = np.fft.fftshift(np.fft.fft(current_packet, N_fft))
        freqs = np.fft.fftshift(np.fft.fftfreq(N_fft, 1 / fs))

        # Plot the frequency spectrum of the corrected packet
        plt.figure(figsize=(20, 6))
        plt.plot(freqs, np.abs(data_fft))
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Magnitude')
        plt.title(f'Frequency Spectrum of Corrected Packet {idx}')
        plt.grid(True)
        plt.show()

# Example usage:
plot_corrected_packet_spectra(corrected_packet, packets)

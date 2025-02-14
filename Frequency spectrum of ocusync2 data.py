import numpy as np
import matplotlib.pyplot as plt

def plot_frequency_spectrum(ocusync2_data, sampling_rate):
    """
    This function computes and plots the frequency spectrum of the input signal using FFT.
    
    Parameters:
    - ocusync2_data: Input signal data (numpy array)
    - sampling_rate: The sampling rate of the signal (Hz)
    """
    # Step 1: Perform the FFT
    n = len(ocusync2_data)  # Number of samples
    fft_data = np.fft.fft(ocusync2_data)

    # Step 2: Shift the zero frequency component to the center
    fft_data_shifted = np.fft.fftshift(fft_data)

    # Step 3: Create the frequency axis
    frequencies = np.fft.fftshift(np.fft.fftfreq(n, 1/sampling_rate))

    # Step 4: Plot the magnitude of the shifted FFT
    plt.figure(figsize=(20, 6))
    plt.plot(frequencies, np.abs(fft_data_shifted))
    plt.title('Frequency Spectrum of the Signal')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.show()

# Example usage:
plot_frequency_spectrum(ocusync2_data, 50e6)

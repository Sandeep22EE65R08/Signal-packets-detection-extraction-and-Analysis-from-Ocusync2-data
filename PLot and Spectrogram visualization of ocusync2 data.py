import numpy as np
import matplotlib.pyplot as plt

def load_and_plot_spectrogram(filepath, sampling_rate=50e6):
    """
    Load complex64 data from a .dat file, compute, and plot the spectrogram.
    
    Parameters:
    filepath (str): Path to the .dat file.
    sampling_rate (float): Sampling frequency in Hz. Default is 50 Msps.
    """
    # Step 1: Read the data
    with open(filepath, "rb") as f:
        data = np.fromfile(f, dtype=np.complex64)
    
    # Step 2: Compute and plot spectrogram
    plt.figure(figsize=(12, 6))
    plt.specgram(data, Fs=sampling_rate)
    plt.title('Spectrogram of Original Data', fontsize=14, fontweight='bold')
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.colorbar(label="Intensity (dB)")
    plt.show()
    
    # Step 3: Create a time array in seconds
    time = np.arange(len(data)) / sampling_rate
    
    return data, time

# Example usage
samplefile = "/home/sandeep/Documents/sandeep/ocusync2_50msps.dat"
data, time = load_and_plot_spectrogram(samplefile)

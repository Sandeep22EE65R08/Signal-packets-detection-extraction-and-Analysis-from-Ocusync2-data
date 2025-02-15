import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter1d

def smooth_energy_curve(energy_curve, window_size):
    """
    Smooth the energy curve using a moving average.
    """
    return uniform_filter1d(energy_curve, size=window_size)

def extract_patterns(filtered_packet, energy_threshold, pattern_length, window_size):
    """
    Extract patterns from the filtered packet based on energy drops.
    
    Parameters:
    - filtered_packet: The signal data after filtering.
    - energy_threshold: Energy threshold for pattern detection.
    - pattern_length: The expected length of each pattern in samples.
    - window_size: The window size for smoothing the energy curve.
    
    Returns:
    - extracted_patterns: List of extracted patterns.
    - detected_starts: List of start indices of detected patterns.
    - detected_ends: List of end indices of detected patterns.
    - smoothed_energy: The smoothed energy curve.
    """
    # Compute energy per sample (squared magnitude)
    energy_per_sample = np.abs(filtered_packet)**2

    # Smooth the energy curve
    smoothed_energy = smooth_energy_curve(energy_per_sample, window_size)

    # Detect patterns based on energy threshold
    detected_starts = []
    detected_ends = []
    extracted_patterns = []

    below_threshold = np.where(smoothed_energy < energy_threshold)[0]
    current_start = None

    for i in range(1, len(below_threshold)):
        if below_threshold[i] != below_threshold[i - 1] + 1:
            # End of a low-energy region
            if current_start is not None:
                drop_duration = below_threshold[i - 1] - current_start + 1
                if drop_duration >= pattern_length:
                    end_sample = current_start + pattern_length
                    detected_starts.append(current_start)
                    detected_ends.append(end_sample)
                    extracted_patterns.append(filtered_packet[current_start:end_sample])
            # Start a new region
            current_start = below_threshold[i]
    # Handle the last region
    if current_start is not None and below_threshold[-1] - current_start + 1 >= pattern_length:
        end_sample = current_start + pattern_length
        detected_starts.append(current_start)
        detected_ends.append(end_sample)
        extracted_patterns.append(filtered_packet[current_start:end_sample])

    return extracted_patterns, detected_starts, detected_ends, smoothed_energy

# Assuming `filtered_packet` is already defined
# Parameters
energy_threshold = 0.000387  # Threshold for detection
pattern_length = 3600    # Length of a pattern in samples (72 microseconds at 50Msps)
window_size = 5        # Smoothing window size for energy curve
sampling_rate = 50e6     # Sampling rate in Hz

# Extract patterns
extracted_patterns, detected_starts, detected_ends, smoothed_energy = extract_patterns(
    filtered_packet, energy_threshold, pattern_length, window_size
)

# Debugging Output
print(f"Number of patterns detected: {len(extracted_patterns)}")
for idx, (start, end) in enumerate(zip(detected_starts, detected_ends)):
    print(f"Pattern {idx + 1}: Start Sample = {start}, End Sample = {end}, Length = {end - start}")

# Plot the smoothed energy curve with detected regions highlighted
plt.figure(figsize=(12, 6))
plt.plot(np.arange(len(smoothed_energy)), smoothed_energy, label="Smoothed Energy", color="red")
plt.axhline(y=energy_threshold, color="blue", linestyle="--", label="Energy Threshold")
for start, end in zip(detected_starts, detected_ends):
    plt.axvspan(start, end, color='green', alpha=0.3, label=f"Pattern {detected_starts.index(start) + 1}" if detected_starts.index(start) == 0 else None)
plt.title("Smoothed Energy Curve with Detected Patterns Highlighted")
plt.xlabel("Sample Index")
plt.ylabel("Energy (Squared Magnitude)")
plt.legend()
plt.grid(True)
plt.show()

# Spectrogram for the entire filtered packet
plt.figure(figsize=(20, 6)) 
plt.specgram(filtered_packet, NFFT=256, Fs=sampling_rate, noverlap=128, scale='dB')
plt.title("Spectrogram of the Filtered Packet")
plt.xlabel("Time [s]")
plt.ylabel("Frequency [Hz]")
plt.colorbar(label="Power/Frequency [dB]")
plt.show()

# Visualize Extracted Patterns and their Spectrograms
for idx, pattern in enumerate(extracted_patterns):
    # Plot the extracted pattern
    plt.figure(figsize=(20, 6))
    plt.plot(np.arange(len(pattern)), np.abs(pattern), label=f"Pattern {idx + 1}")
    plt.title(f"Extracted Pattern {idx + 1}")
    plt.xlabel("Sample Number")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot the spectrogram of the extracted pattern
    plt.figure(figsize=(20, 6))
    plt.specgram(pattern, NFFT=256, Fs=sampling_rate, noverlap=128, scale='dB')
    plt.title(f"Spectrogram of Extracted Pattern {idx + 1}")
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [Hz]")
    plt.colorbar(label="Power/Frequency [dB]")
    plt.show()

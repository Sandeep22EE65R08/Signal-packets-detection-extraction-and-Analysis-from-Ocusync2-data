import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

def bandpass_filter(data, sampling_rate, low_cutoff, high_cutoff, order=4):
    """
    Apply a bandpass filter to isolate the desired frequency range.

    Parameters:
        data (np.ndarray): Input signal.
        sampling_rate (float): Sampling rate in Hz.
        low_cutoff (float): Low cutoff frequency in Hz.
        high_cutoff (float): High cutoff frequency in Hz.
        order (int): Filter order.

    Returns:
        filtered_data (np.ndarray): Bandpass-filtered signal.
    """
    nyquist = sampling_rate / 2.0
    low = low_cutoff / nyquist
    high = high_cutoff / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

def detect_packets_energy(data, sampling_rate, window_ms, threshold_factor):
    """
    Detect signal packets based on energy accumulation.

    Parameters:
        data (np.ndarray): Input complex signal.
        sampling_rate (float): Sampling rate in Hz.
        window_ms (float): Window size in milliseconds.
        threshold_factor (float): Multiplier for the energy threshold.

    Returns:
        packets (list): List of (start_index, end_index) for detected packets.
        energy_profile (np.ndarray): Energy profile computed over sliding windows.
        threshold (float): Energy threshold used for detection.
    """
    # Convert window size to samples
    window_samples = int((window_ms / 1000) * sampling_rate)

    # Calculate energy profile using a sliding window
    energy_profile = np.convolve(np.abs(data)**2, np.ones(window_samples), mode='same')

    # Set threshold for detection
    noise_level = np.mean(energy_profile)  # Baseline noise level
    threshold = threshold_factor * noise_level
a
    # Detect packets based on threshold
    detected = energy_profile > threshold
    packets = []
    start = None

    for i, is_high in enumerate(detected):
        if is_high and start is None:
            start = i  # Start of a packet
        elif not is_high and start is not None:
            end = i  # End of the packet
            packets.append((start, end))
            start = None

    # Handle the last packet if it continues to the end
    if start is not None:
        packets.append((start, len(detected)))

    return packets, energy_profile, threshold

# Parameters
sampling_rate = 50e6  # Sampling rate in Hz

window_ms = 0.508  # Window size in milliseconds
threshold_factor = 0.6  # Threshold multiplier
low_cutoff = 5e6  # 15 MHz
high_cutoff = 24e6  # 25 MHz

# Step 1: Apply Bandpass Filter to Isolate 20 MHz Signal
filtered_data = bandpass_filter(ocusync2_data, sampling_rate, low_cutoff, high_cutoff)

# Step 2: Detect Signal Packets
packets, energy_profile, threshold = detect_packets_energy(filtered_data, sampling_rate, window_ms, threshold_factor)

# Step 3: Plot Energy Profile with Detected Regions
plt.figure(figsize=(12, 6))
plt.plot(energy_profile, label="Energy Profile", color="blue")
plt.axhline(y=threshold, color="red", linestyle="--", label="Threshold")
plt.title("Energy Profile with Detected Signal Packets (20 MHz Band)")
plt.xlabel("Sample Index")
plt.ylabel("Energy")
plt.legend()
plt.grid()
plt.show()

# Step 4: Plot and Analyze Detected Packets
print(f"Number of detected packets: {len(packets)}")
for idx, (start_idx, end_idx) in enumerate(packets, start=1):
    start_time = start_idx / sampling_rate
    end_time = end_idx / sampling_rate
    print(f"Packet {idx}: Start Time = {start_time:.6f} s, End Time = {end_time:.6f} s, Duration = {end_time - start_time:.6f} s")

    # Extract corresponding signal samples
    packet_data = filtered_data[start_idx:end_idx]

    # Plot the extracted packet
    plt.figure(figsize=(10, 4))
    plt.plot(np.arange(start_idx, end_idx) / sampling_rate, np.abs(packet_data), label=f"Packet {idx}")
    plt.title(f"Extracted Signal Packet {idx} (20 MHz Band)")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid()
    plt.show()

import numpy as np
import matplotlib.pyplot as plt

def visualize_detected_packets(ocusync2_data, packets, sampling_rate):
    """
    This function visualizes detected signal packets by plotting their spectrograms and 
    printing details such as start time, end time, duration, and number of samples.
    
    Parameters:
    - ocusync2_data: The input signal data (numpy array)
    - packets: A list of tuples (start_idx, end_idx) indicating detected packet indices
    - sampling_rate: The sampling rate of the signal (Hz)
    """
    # Loop through all detected signal packets
    for i, (start_idx, end_idx) in enumerate(packets):
        # Extract the current packet
        current_packet = ocusync2_data[start_idx:end_idx]

        # Create a time array for the current packet
        current_packet_time = np.arange(len(current_packet)) / sampling_rate

        # Plot the spectrogram of the current packet
        plt.figure(figsize=(20, 6))
        plt.specgram(current_packet, NFFT=256, Fs=sampling_rate, noverlap=128, cmap='viridis', scale='dB')
        plt.title(f"Spectrogram of Detected Packet {i + 1}")
        plt.xlabel("Time [s]")
        plt.ylabel("Frequency [Hz]")
        plt.colorbar(label="Power/Frequency [dB]")
        plt.show()

        print(f"Visualizing packet {i + 1}: Start index = {start_idx}, End index = {end_idx}")

    # Step 4: Print the Number of Samples for Each Detected Packet
    print(f"Number of detected packets: {len(packets)}")
    for idx, (start_idx, end_idx) in enumerate(packets, start=1):
        # Calculate start time, end time, and duration
        start_time = start_idx / sampling_rate
        end_time = end_idx / sampling_rate
        duration = end_time - start_time

        # Calculate the number of samples in the packet
        num_samples = end_idx - start_idx  # Number of samples in the packet

        # Print the details of each packet
        print(f"Packet {idx}: Start Time = {start_time:.6f} s, End Time = {end_time:.6f} s, "
              f"Duration = {duration:.6f} s, Number of Samples = {num_samples}")

# Example usage:
visualize_detected_packets(ocusync2_data, packets, sampling_rate)

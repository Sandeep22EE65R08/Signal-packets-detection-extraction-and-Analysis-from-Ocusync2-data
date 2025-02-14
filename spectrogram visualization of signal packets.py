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

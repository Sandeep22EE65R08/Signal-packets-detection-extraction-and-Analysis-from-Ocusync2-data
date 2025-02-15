def lowpass(data: np.ndarray, cutoff: float, sample_rate: float, poles: int = 12):
    # Design the low-pass filter using Butterworth filter
    sos = scipy.signal.butter(poles, cutoff, 'lowpass', fs=sample_rate, output='sos')
    filtered_data = scipy.signal.sosfiltfilt(sos, data)
    return filtered_data, sos

        # Apply low-pass filter to the corrected packet (e.g., 4 MHz cutoff)
filtered_packet, sos = lowpass(corrected_packet, 8.5e6, sampling_rate)

fs=50e6
# Frequency response of the filter
w, h = scipy.signal.sosfreqz(sos, worN=2000, fs=fs)

# Loop through all extracted packets, apply low-pass filter, and plot the filtered packets
for idx, (start_idx, end_idx) in enumerate(packets, start=1):
    # Extract corresponding signal samples for the packet
    current_packet = ocusync2_data[start_idx:end_idx]

    # Correct the frequency offset for the packet (assuming offset is calculated previously)
    offset, band_found = processor.estimate_offset(current_packet, sampling_rate, packet_type="droneid")

    if band_found:
        # Apply frequency shift correction using the static method of DroneSignalProcessor
        corrected_packet = DroneSignalProcessor.fshift(current_packet, -offset, sampling_rate)

        # Apply low-pass filter to the corrected packet (e.g., 4 MHz cutoff)
        filtered_packet, sos = lowpass(corrected_packet, 8.5e6, sampling_rate)

        # Plot the spectrogram for the filtered packet
        plt.figure(figsize=(20, 6))
        plt.specgram(filtered_packet, NFFT=256, Fs=sampling_rate, noverlap=128, scale='dB')
        plt.title(f"Spectrogram of Filtered Packet {idx}")
        plt.xlabel("Time [s]")
        plt.ylabel("Frequency [Hz]")
        plt.colorbar(label="Power/Frequency [dB]")
        plt.show()
    else:
        print(f"Packet {idx}: No suitable band found for offset correction.")

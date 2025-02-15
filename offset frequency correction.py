class DroneSignalProcessor:
    def __init__(self, debug=True):
        self.debug = debug

    @staticmethod
    def fshift(y, offset, Fs):
        """Shift the frequency of the signal."""
        print(f"{len(y)}, offset={offset}, Fs={Fs}")
        x = np.linspace(0.0, len(y) / Fs, len(y))
        return y * np.exp(x * 2j * np.pi * offset)

# Assuming you have already estimated the offset for each packet and stored in 'offset'
for idx, (start_idx, end_idx) in enumerate(packets, start=1):
    # Extract corresponding signal samples for the packet
    current_packet = ocusync2_data[start_idx:end_idx]

    # Correct the frequency offset for the packet
    offset, band_found = processor.estimate_offset(current_packet, sampling_rate, packet_type="droneid")

    if band_found:
        # Apply frequency shift correction using the static method of DroneSignalProcessor
        corrected_packet = DroneSignalProcessor.fshift(current_packet, -offset, sampling_rate)

        # Plot the spectrogram for the corrected packet
        plt.figure(figsize=(20, 6))
        plt.specgram(corrected_packet, NFFT=256, Fs=sampling_rate, noverlap=128, scale='dB')
        plt.title(f"Spectrogram of Detected Packet {idx}")
        plt.xlabel("Time [s]")
        plt.ylabel("Frequency [Hz]")
        plt.colorbar(label="Power/Frequency [dB]")
        plt.show()
    else:
        print(f"Packet {idx}: No suitable band found for offset correction.")

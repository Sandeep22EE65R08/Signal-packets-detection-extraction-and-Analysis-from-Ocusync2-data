class DroneSignalProcessor:
    def __init__(self, debug=True):
        self.debug = debug

    @staticmethod
    def consecutive(data, stepsize=1):
        """Group consecutive elements based on a step size."""
        return np.split(data, np.where(np.diff(data) != stepsize)[0] + 1)

    def estimate_offset(self, y, Fs, packet_type="droneid"):
        """Estimate the frequency offset in the signal."""
        nfft_welch = 2048  # FFT size for PSD calculation

        if len(y) < nfft_welch:
            return None, False

        # Apply Hamming window to the signal
        window = hamming(len(y))
        y = y * window

        # Calculate Power Spectral Density (PSD)
        f, Pxx_den = welch(y, Fs, nfft=nfft_welch, return_onesided=False)
        Pxx_den = np.fft.fftshift(Pxx_den)
        f = np.fft.fftshift(f)

        # Add a fake DC carrier to distinguish signal components
        Pxx_den[nfft_welch // 2 - 10:nfft_welch // 2 + 10] = 1.1 * Pxx_den.mean()

        # Identify candidate frequency bands
        candidate_bands = self.consecutive(np.where(Pxx_den > 1.1 * Pxx_den.mean())[0])

        band_found = False
        offset = 0.0

        for band in candidate_bands:
            start = band[0] - nfft_welch / 2
            end = band[-1] - nfft_welch / 2
            bw = (end - start) * (Fs / nfft_welch)
            fend = start * Fs / nfft_welch
            fstart = end * Fs / nfft_welch

            if self.debug:
                print(f"Candidate band fstart: {fstart:.2f}, fend: {fend:.2f}, bw: {bw / 1e6:.2f} MHz")

            # Check if the candidate band's frequency offset falls within the range of -4 MHz to -24 MHz
            if -24e6 <= fstart - 0.5 * bw <= 0:  # Adjust this condition
                offset = fstart - 0.5 * bw
                band_found = True
                break

        if self.debug:
            print(f"Offset found: {offset / 1000:.2f} kHz")
        return offset, band_found


# Assuming you have the packets already detected, loop through each packet and estimate its offset
for idx, (start_idx, end_idx) in enumerate(packets, start=1):
    start_time = start_idx / sampling_rate
    end_time = end_idx / sampling_rate
    print(f"Packet {idx}: Start Time = {start_time:.6f} s, End Time = {end_time:.6f} s, Duration = {end_time - start_time:.6f} s")

    # Extract corresponding signal samples for the packet
    packet_data = ocusync2_data[start_idx:end_idx]

    # Initialize DroneSignalProcessor to estimate the offset
    processor = DroneSignalProcessor(debug=False)

    # Estimate the frequency offset for this packet
    offset, band_found = processor.estimate_offset(packet_data, sampling_rate, packet_type="droneid")

    if band_found:
        print(f"Packet {idx}: Estimated Frequency Offset = {offset / 1000:.2f} kHz")
    else:
        print(f"Packet {idx}: No suitable band found for offset estimation.")

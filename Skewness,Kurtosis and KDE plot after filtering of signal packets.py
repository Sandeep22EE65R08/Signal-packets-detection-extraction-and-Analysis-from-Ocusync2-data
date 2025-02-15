import seaborn as sns

def moment_based_skew(signal_packet):
    n = len(signal_packet)
    mean = np.mean(signal_packet)
    std = np.std(signal_packet)

    # Divide the formula into two parts
    first_part = n / ((n - 1) * (n - 2))
    second_part = np.sum(((signal_packet - mean) / std) ** 3)

    skewness = first_part * second_part

    return skewness

# Function to calculate kurtosis using the moment-based method
def moment_based_kurtosis(signal_packet):
    """
    Calculate the kurtosis of a distribution using the moment-based method.
    The magnitude of the complex signal will be used.
    """


    n = len(signal_packet)
    mean = np.mean(signal_packet)
    std = np.std(signal_packet)

    # Calculate the kurtosis (subtract 3 for excess kurtosis)
    kurtosis = (1 / n) * np.sum(((signal_packet - mean) / std) ** 4) - 3

    return kurtosis



# Loop through all extracted packets, compute skewness and kurtosis, and plot KDE
for idx, (start_idx, end_idx) in enumerate(packets, start=1):
    # Extract corresponding signal samples for the packet from filtered data
    current_packet = ocusync2_data[start_idx:end_idx]

    # Assuming offset has already been calculated
    corrected_packet = DroneSignalProcessor.fshift(current_packet, -offset, sampling_rate)

    # Apply low-pass filter to the corrected packet
    filtered_packet, sos = lowpass(corrected_packet, 8.5e6, sampling_rate)

    # Compute skewness and kurtosis
    skewness = moment_based_skew(np.abs(filtered_packet))
    kurtosis_value = moment_based_kurtosis(np.abs(filtered_packet))

    # Determine skewness type
    if skewness > 0:
        skewness_description = "Positive Skewness"
    elif skewness < 0:
        skewness_description = "Negative Skewness"
    else:
        skewness_description = "Symmetrical Distribution"

    # Determine kurtosis type
    if kurtosis_value > 3:
        kurtosis_description = "Leptokurtic (Sharp peak)"
    elif kurtosis_value < 3:
        kurtosis_description = "Platykurtic (Flat peak)"
    else:
        kurtosis_description = "Mesokurtic (Normal peak)"

    # Plot the KDE for the current packet
    plt.figure(figsize=(20, 6))

    # Use the magnitude for KDE plotting
    sns.kdeplot(np.abs(filtered_packet), label=f"Packet {idx} KDE", fill=True)  # KDE for magnitude
    plt.title(f"KDE plot of Packet {idx}\n{skewness_description} | {kurtosis_description}")
    plt.xlabel("Amplitude")
    plt.ylabel("Density")
    plt.legend(loc='upper right')
    plt.show()

    # Print the skewness and kurtosis for each packet
    print(f"Packet {idx}: Skewness = {skewness:.4f}, Kurtosis = {kurtosis_value:.4f}")

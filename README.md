# Signal-packets-detection-extraction-and-Analysis-from-Ocusync2-data


# **Digital Signal Processing for Signal Packet Detection & Analysis**  

## **Project Overview**  
Developed a DSP pipeline to detect, extract, and analyze signal packets using spectral analysis, filtering, energy-based detection, frequency offset correction, and pattern recognition techniques.  

## **Key Features**  
- Spectrogram generation for time-frequency analysis  
- PSD computation using Welch’s method for spectral characteristics  
- FFT-based frequency spectrum analysis  
- Energy-based signal packet detection and extraction  
- Frequency offset estimation and correction  
- Low-pass filtering and post-filtering spectral analysis  
- SNR computation for signal quality assessment  
- Pattern detection and extraction using reference templates  
- Statistical analysis (skewness, kurtosis, and KDE plots)  

## **Implementation Steps**  

### **1. Signal Visualization & Spectral Analysis**  
- Generate spectrograms to analyze time-varying frequency content  
- Compute PSD using Welch’s method with a Hamming window  
- Perform FFT to analyze frequency spectrum and shift zero frequency  

### **2. Signal Packet Detection & Extraction**  
- Apply a Butterworth bandpass filter to isolate the desired frequency range  
- Compute energy profile, apply a moving average, and set an adaptive threshold  
- Identify and extract packets based on energy variations  

### **3. Frequency Offset Estimation & Correction**  
- Estimate frequency offset using PSD analysis  
- Apply phase compensation to correct frequency offset  
- Verify correction through spectrogram and FFT-based analysis  

### **4. Post-Filtering Spectral Analysis**  
- Apply a Butterworth low-pass filter  
- Compute and analyze PSD and FFT results after filtering  

### **5. SNR Calculation for Filtered Signal Packets**  
- Compute signal power by integrating PSD within the signal frequency band  
- Compute noise power by integrating PSD within noise bands  
- Calculate SNR (dB) = 10 log10 (P_signal / P_noise)  

### **6. Pattern Detection & Extraction After Filtering**  
- Detect patterns using a sliding window with a predefined reference pattern  
- Identify patterns of 70µs duration using energy thresholding  
- Extract and visualize detected patterns  

### **7. Statistical Analysis**  
- Compute skewness and kurtosis to analyze amplitude distribution  
- Generate Kernel Density Estimation (KDE) plots for visualization  

## **Technologies Used**  
- **Programming:** Python (NumPy, SciPy, Matplotlib)  
- **Signal Processing:** FFT, Welch’s Method, Bandpass and Low-Pass Filtering, Frequency Offset Estimation  
- **Visualization:** Spectrograms, PSD, FFT, KDE Plots  

## **Project Outcome**  
Achieved successful signal packet detection, extraction, and pattern recognition with enhanced SNR. Integrated DSP techniques provided improved signal characterization and frequency analysis.  

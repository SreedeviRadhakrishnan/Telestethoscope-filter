import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import firwin, lfilter
import wave

# Read the wave file
sample_rate, data = wavfile.read(r"C:\Users\91918\Documents\heartsounds\heartsound1.wav")

# Check if the data is mono or stereo
num_channels = 1 if len(data.shape) == 1 else data.shape[1]

# Calculate the time axis in seconds
time = np.arange(0, len(data)) / sample_rate

# Define bandpass filter parameters
lowcutf = 0.5   # Lower cutoff frequency (Hz)
highcutf = 200  # Higher cutoff frequency (Hz)
filter_order = 600  # Filter order

# Design the FIR bandpass filter
nyquist = 0.5 * sample_rate
low = lowcutf / nyquist
high = highcutf / nyquist
b = firwin(filter_order, [low, high], pass_zero=False)

# Apply the filter to each channel
filtered_data = lfilter(b, 1, data, axis=0)

# Plot the original and filtered waveforms
plt.figure(figsize=(10, 6))

# Plot the original waveform
plt.subplot(2, 1, 1)
plt.plot(time, data)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Original Waveform')

# Plot the filtered waveform
plt.subplot(2, 1, 2)
plt.plot(time, filtered_data)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Filtered Waveform')

plt.tight_layout()
plt.show()

# Convert the filtered data to integer format (16-bit PCM)
filtered_data_int = (filtered_data * 32767).astype(np.int16)

# Create a wave file and write the filtered data
output_filename = "filtered_output.wav"
with wave.open(output_filename, 'w') as wf:
    wf.setnchannels(1)  # Set to 1 for mono, 2 for stereo
    wf.setsampwidth(2)  # 2 bytes (16 bits) per sample
    wf.setframerate(sample_rate)
    wf.writeframes(filtered_data_int.tobytes())

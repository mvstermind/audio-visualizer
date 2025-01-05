import numpy as np
from scipy.io import wavfile
import audio_converter as converter
import matplotlib.pyplot as plt


CHUNK_SIZE = 1024


def main():
    files: list[str] = converter.open("beats_db")

    for file in files:
        sample_rate, data = wavfile.read(file)
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)
        data = data.astype(np.float32)

        # plot full waveform first
        plt.figure(figsize=(15, 8))
        plt.subplot(211)
        time = np.arange(len(data)) / sample_rate
        plt.plot(time, data)
        plt.title("Full Waveform")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Amplitude")
        plt.grid(True)

        # plot chunk peaks
        chunk_peaks = []
        chunk_times = []
        max_peak_idx = 0
        max_peak_val = float("-inf")

        for i in range(len(data) // CHUNK_SIZE):
            start = i * CHUNK_SIZE
            chunk = data[start : start + CHUNK_SIZE]
            peak = np.max(np.abs(chunk))
            chunk_peaks.append(peak)
            chunk_times.append(i * CHUNK_SIZE / sample_rate)

            if peak > max_peak_val:
                max_peak_val = peak
                max_peak_idx = i
                print(f"New max peak found: {peak:.2f} at time {chunk_times[-1]:.2f}s")

        plt.subplot(212)
        plt.plot(chunk_times, chunk_peaks)
        plt.axvline(
            x=max_peak_idx * CHUNK_SIZE / sample_rate,
            color="r",
            linestyle="--",
            label="Detected Peak",
        )
        plt.title("Chunk Peak Values")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Peak Amplitude")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

        # FFT analysis of detected loudest chunk
        frequencies, magnitudes, time_info = fft_of_loudest_chunk(file, CHUNK_SIZE)
        print(f"\nFinal loudest chunk found at: {time_info:.3f} seconds")

        plt.figure(figsize=(10, 6))
        magnitudes_db = 20 * np.log10(magnitudes + 1e-12)
        plt.plot(frequencies, magnitudes_db, color="blue", linewidth=2)
        plt.xscale("log")
        plt.xlim(20, 20000)
        plt.grid(which="both", linestyle="--", linewidth=0.5, color="gray")
        plt.title(f"FFT at {time_info:.3f}s")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Magnitude (dB)")
        plt.show()


def fft_of_loudest_chunk(file: str, chunk_size: int):
    sample_rate, data = wavfile.read(file)

    if len(data.shape) > 1:
        data = np.mean(data, axis=1)

    data = data.astype(np.float32)

    num_chunks = len(data) // chunk_size
    loudest_chunk = None
    max_peak = float("-inf")
    loudest_chunk_index = 0

    for i in range(num_chunks):
        start = i * chunk_size
        chunk = data[start : start + chunk_size]
        peak = np.max(np.abs(chunk))

        if peak > max_peak:
            max_peak = peak
            loudest_chunk = chunk
            loudest_chunk_index = i

    time_in_seconds = (loudest_chunk_index * chunk_size) / sample_rate

    fft_result = np.fft.fft(loudest_chunk)
    magnitudes = np.abs(fft_result[: chunk_size // 2])
    frequencies = np.fft.fftfreq(chunk_size, d=1 / sample_rate)[: chunk_size // 2]

    return frequencies, magnitudes, time_in_seconds


if __name__ == "__main__":
    main()

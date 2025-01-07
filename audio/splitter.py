"""Slices given wav file into chunks"""

import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from typing import Any, Tuple, List

CHUNK_LEN_SEC = 10


def loudest_audio_chunk(
    file: str, graph: bool, fft_graph: bool = False
) -> Tuple[float, List[Any]]:
    """Returns loudest average magnitude in audio chunk and list containing
    data from loudest chunk in given file as float value."""
    data, sample_rate = sf.read(file, dtype="float32")
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)  # convert to mono

    chunk_size = sample_rate * CHUNK_LEN_SEC
    num_chunks = len(data) // chunk_size

    chunked_audio = split_audio(
        num_chunks=num_chunks, chunk_size=chunk_size, audio_data=data
    )

    loudest_chunk_avg = -np.inf
    loudest_chunk_start = 0

    for i, chunk in enumerate(chunked_audio):
        chunk_avg = chunk_avg_val(chunk)
        if chunk_avg > loudest_chunk_avg:
            loudest_chunk_avg = chunk_avg
            loudest_chunk_start = i * chunk_size

    loudest_chunk_end = loudest_chunk_start + chunk_size
    loudest_chunk_list = data[loudest_chunk_start:loudest_chunk_end]

    if graph:
        plot_waveform_with_loudest(data, sample_rate, loudest_chunk_start, chunk_size)

    if fft_graph:
        pass

    return loudest_chunk_avg, loudest_chunk_list


def split_audio(chunk_size: int, num_chunks: int, audio_data: np.ndarray):
    """Splits audio into chunks."""
    chunked_audio = []
    total_samples = len(audio_data)

    for i in range(num_chunks):
        start_index = i * chunk_size
        end_index = start_index + chunk_size

        if end_index > total_samples:
            end_index = total_samples

        chunked_audio.append(audio_data[start_index:end_index])

    return chunked_audio


def chunk_avg_val(chunk: np.ndarray) -> np.floating[Any]:
    """Calculates the average amplitude of a chunk."""
    return np.mean(np.abs(chunk))


# this is for me, just to see if this works
def plot_waveform_with_loudest(
    data: np.ndarray, sample_rate: int, loudest_start: int, chunk_size: int
):
    """Plots the entire waveform and highlights the loudest chunk."""
    time = np.linspace(0, len(data) / sample_rate, len(data))

    plt.figure(figsize=(12, 6))
    plt.plot(time, data, color="blue", linewidth=0.8, label="waveform")

    loudest_end = loudest_start + chunk_size
    plt.plot(
        time[loudest_start:loudest_end],
        data[loudest_start:loudest_end],
        color="pink",
        linewidth=1.5,
        label="loudest part",
    )

    plt.title("waveform + loudest part marked")
    plt.xlabel("time in seconds")
    plt.ylabel("amplitude")
    plt.axvline(
        x=time[loudest_start],
        color="green",
        linestyle="--",
        label=f"loudest part starts at({time[loudest_start]:.2f} sec)",
    )
    plt.axvline(
        x=time[loudest_end - 1],
        color="green",
        linestyle="--",
        label=f"loudest part ends at({time[loudest_end - 1]:.2f} sec)",
    )
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

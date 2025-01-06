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


if __name__ == "__main__":
    main()

import numpy as np
from scipy.io import wavfile
import audio_converter as converter


def main():
    files: list[str] = converter.open("beats_db")

    for file in files:
        rate, data = wavfile.read(file)
        for d in data:
            print(d)

    print(files)


def calc_rms()

if __name__ == "__main__":
    main()

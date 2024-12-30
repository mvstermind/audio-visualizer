from errors import InvalidFileFormatError
import numpy as np
from scipy.io import wavfile
import os
from pathlib import Path


def main():
    files: list[str] = read_audio_db("beats_db")

    print(files)

    # for file in files:
    #     rate, _data = wavfile.read(file)
    #     print(f"{file} has {rate} sample rate")


# reads all fiels, looks for .mp3 and .wav
# converts all .mp3 to .wav with ffmpeg
# return a list of all wav files
def read_audio_db(path_name: str) -> list[str]:
    wav_files: list[str] = []
    pathlist = Path(path_name).rglob("*")
    for path in pathlist:
        if str(path).endswith(".mp3") or str(path).endswith(".wav"):
            convert_to_wav(str(path))
            wav_files.append(str(path))

    return wav_files


# dunno what's better way to make it work
def convert_to_wav(filename: str) -> None:
    if filename.endswith(".wav"):
        return

    elif filename.endswith("mp3"):
        os.system(f"ffmpeg -i {filename} {filename.strip(".mp3")}.wav")
        os.system("clear")
        remove_mp3(filename)
        return

    else:
        raise InvalidFileFormatError("use valid file format")


def remove_mp3(filename: str) -> None:
    os.system(f"rm -f {filename}")


if __name__ == "__main__":
    main()

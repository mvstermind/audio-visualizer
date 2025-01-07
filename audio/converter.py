"""turns all mp3's into wav files"""

import os
from pathlib import Path


# reads all fiels, looks for .mp3 and .wav
# converts all .mp3 to .wav with ffmpeg
# return a list of all wav files
def open(path_name: str) -> list[str]:
    """
    Reads all files in given path
    converts all mp3's into wav files using ffmpeg
    returns list of strings that are paths of ALL wav files only
    """
    wav_files: list[str] = []

    # first turn all files into wav (if possible)
    pathlist = Path(path_name).rglob("*")
    for path in pathlist:
        # is it how i supposed to handle spaces in filenames??
        if " " in rf"{str(path)}":
            path_no_space: str = str(path).replace(" ", "\\ ")
            _convert_to_wav(path_no_space)
        else:
            _convert_to_wav(str(path))

    new_path = Path(path_name).rglob("*")
    for path in new_path:
        if str(path).endswith(".wav"):
            wav_files.append(str(path))
        else:
            continue
    return wav_files


# dunno what's better way to make it work
def _convert_to_wav(filename: str) -> None:
    """
    Converts ONLY mp3 files to wav using ffmpeg
    """
    if filename.endswith(".wav"):
        return

    elif filename.endswith("mp3"):
        os.system(f"ffmpeg -i {filename} {filename.strip(".mp3")}.wav")
        os.system("clear")
        _remove_mp3(filename)
        return

    else:
        pass


def _remove_mp3(filename: str) -> None:
    os.system(f"rm -f {filename}")

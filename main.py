from audio import converter, splitter


def main():
    files: list[str] = converter.open("beats_db")

    for file in files:
        loudest_avg, loudest_chunk_list = splitter.loudest_audio_chunk(
            file, graph=True, fft_graph=True
        )


if __name__ == "__main__":
    main()


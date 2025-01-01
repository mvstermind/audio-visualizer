# audio-visualizer
Ffmpeg is required!

### To-Do

1. **Find Loudest Segment** (using **v²**)

    To identify the loudest part of the audio signal, calculate the **average squared** **v²** for different chunks of the waveform. The segment with the highest value of **v²** is considered the loudest.

    ![Average Squared Equation](https://latex.codecogs.com/gif.latex?%3Cv%5E2%3E%20%3D%20%5Cfrac%7B1%7D%7BN%7D%20%5Csum%7Bi%3D1%7D%5EN%20x%5Bi%5D%5E2)

2. **Extract Samples Needed**

    Once the loudest segment is found, extract the samples corresponding to that segment for further analysis.

3. **Perform FFT on Extracted Sample**

    Perform the **Fast Fourier Transform (FFT)** on the extracted sample to convert the time-domain signal into the frequency domain.

4. **Convert FFT Results into Magnitude**

    The magnitude of the FFT result can be computed using the formula:

    ![FFT Formula](https://latex.codecogs.com/gif.latex?f%20%3D%20%5Cfrac%7B%5Ctext%7Bbin%20index%7D%20%5Ctimes%20%5Ctext%7Bsampling%20rate%7D%7D%7B%5Ctext%7BFFT%20size%7D%7D)

    - **Where**:
        - `bin index` is the index of the frequency bin.
        - `sampling rate` is the sample rate of the original audio signal.
        - `FFT size` is the total number of FFT bins.

## **Why not RMS?**

### RMS Calculation
The Root Mean Square (RMS) measures the effective amplitude of a signal:

![RMS Equation](https://latex.codecogs.com/gif.latex?%5Ctext%7BRMS%7D%20%3D%20%5Csqrt%7B%5Cfrac%7B1%7D%7BN%7D%20%5Csum%7Bi%3D1%7D%5EN%20x%5Bi%5D%5E2%7D)

- Used to assess signal loudness in units matching the original amplitude.
- Computationally more expensive due to the square root.

### Average Squared **v²**
The Average Squared is a simpler alternative for measuring signal energy:

![Average Squared Equation](https://latex.codecogs.com/gif.latex?%3Cv%5E2%3E%20%3D%20%5Cfrac%7B1%7D%7BN%7D%20%5Csum%7Bi%3D1%7D%5EN%20x%5Bi%5D%5E2)

- Provides the same relative loudness ranking as RMS.
- Faster to compute, making it ideal for larger datasets.

### Why **v²** Was Used
In this project, **v²**  was chosen over RMS to efficiently identify the loudest part of the audio signal,
as it avoids unnecessary computation without sacrificing accuracy in ranking loudness.

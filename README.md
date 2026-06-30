# Guitar Tuner App

This is a very basic, bare bones guitar tuner application designed for assisting an indivdual with tuning their guitar. The application requires the machine to have a micripohne, which the application will automatically recognize. When the user strums the string, the microphone automatically detects the acoustic signal which is then processed through a YIN algorithm. This algorithm provides the application signal accuracyly while limiting background noise interference, thus allowing it to isolate only the intended audio signal. After audip processing, the frequency is converted to it's corresponding pitch notation. The intended frequency and pitch notation are displayed in the gui as well as the real time frequency of the audio signal from the guitar. this give the user a point of refrence to allow them to determine wither the string is to tight to loose to produce the intended note. 


### Project Structure
* gui.py: The application frontend. Contains the Tkinter canvas, calculates the geometric transformations for the needle, and updates the display at 20 FPS (50ms). Run this file to start the app.

* main.py: Initializes the audio stream and runs the background audio processing loop on a daemon thread.

* audio_engine.py: Handles the hardware interface, safely querying input devices and populating the asynchronous audio queue.

* dsp_processor.py: The mathematical core of the tuner. Handles the low-pass filtering and the full YIN algorithm pipeline (Difference Function, Cumulative Mean Normalized Difference, and Peak/Valley Detection).

* config.py: Centralized configuration file for sample rates, buffer sizes, RMS volume thresholds, and ideal note frequencies.


### Usage

To start the tuner, execute the gui.py file from your terminal:
Bash

python gui.py

Ensure your microphone is active. The application will automatically detect the best input device, establish a stream, and begin analyzing the audio buffer. Play a note, and the UI will display the detected Hz, the closest musical note, and how many cents sharp or flat you are.

### Technical Notes: The YIN Implementation
This tuner utilizes a Time-Domain Autocorrelation approach. Standard FFT (Fast Fourier Transform) tuners often struggle with low-frequency resolution at small buffer sizes. The YIN algorithm solves this by operating entirely in the time domain.

To maintain accuracy on low-frequency notes without mathematically skewing the results, the difference function avoids standard array zero-padding. Instead, it slides a fixed half-window across the incoming audio buffer, guaranteeing an exact 1:1 sample comparison for every shift. This maintains a flat mathematical baseline and ensures the absolute minima represent the true fundamental frequency of the audio signal.
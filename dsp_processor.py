import scipy.signal as signal
import numpy as np
b, a = None, None

# Create filter kernel once at module level (not recreated each frame for efficiency)\
def configure(rate):
    global b, a
    b, a = signal.butter(4, 2000 / (rate / 2), 'low')

def preprocess_buffer(data):
    filtered_data = signal.filtfilt(b, a, data)
    window_data = filtered_data * np.hanning(len(filtered_data))
    return window_data

def  calculate_difference_function(data):
    energy = np.sum(data ** 2)
    result = 2 * energy - 2 * np.correlate(data, data, mode='full')[len(data)-1:]
    return result

def calculate_cumulative_mean_normalized_difference_function(df):
    cmnd = df.copy()
    for tau in range(1, len(df)):
        cmnd[tau] = df[tau] / (np.sum(df[1:tau + 1])/tau)
    return cmnd

def peak_valley_detection(cmnd):
    first_threshold = 0.15
    index = None
    for i in range(1, len(cmnd)-1):
        if cmnd[i] < first_threshold:
            index = i
            break
    if index is None:
        return None

    min_index = index
    for i in range(index, len(cmnd)-1):
        if cmnd[i] < cmnd[min_index]:
            min_index = i
    return min_index

def frequency_to_note_cent(freq):
    A4 = 440.0
    if freq <= 0:
        return None, None
    semitones_from_A4 = 12 * np.log2(freq / A4)
    note_index = int(round(semitones_from_A4)) % 12
    cents_off = (semitones_from_A4 - round(semitones_from_A4)) * 100
    note_names = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    note_name = note_names[note_index]
    return note_name, cents_off
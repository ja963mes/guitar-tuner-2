import scipy.signal as signal
import numpy as np
b, a = None, None

# Create filter kernel once at module level (not recreated each frame for efficiency)\
def configure(rate):
    global b, a
    b, a = signal.butter(4, 2000 / (rate / 2), 'low')

def preprocess_buffer(data):
    filtered_data = signal.filtfilt(b, a, data)
    return filtered_data

def calculate_difference_function(data):
    W = len(data) // 2
    df = np.zeros(W)
    
    for tau in range(W):

        df[tau] = np.sum((data[:W] - data[tau:tau+W]) ** 2)
        
    return df

def calculate_cumulative_mean_normalized_difference_function(df):
    cmnd = df.copy()
    for tau in range(1, len(df)):
        cmnd[tau] = df[tau] / (np.sum(df[1:tau + 1])/tau)
    return cmnd

def peak_valley_detection(cmnd):
    first_threshold = 0.15
    for tau in range(1, len(cmnd) - 1):
        if cmnd[tau] < first_threshold:
            while tau + 1 < len(cmnd) and cmnd[tau + 1] < cmnd[tau]:
                tau += 1
            return tau
            
    return None

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
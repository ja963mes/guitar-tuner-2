import numpy as np
import sys
from audio_engine import start_stream, stop_stream, AUDIO_QUEUE, callback_count
import dsp_processor as  dsp
import threading

detected_data = {
    "frequency": 0.0,
    "cents_off": 0.0,
    "note": ""

}

print("Starting audio stream...", flush=True)
stream = start_stream()
print(stream.samplerate)
print("Audio stream started. Make noise near the microphone...", flush=True)

dsp.configure(stream.samplerate)

def audio_processing_loop():
    count = 0
    rate = stream.samplerate
    while True:
        if not AUDIO_QUEUE.empty():
            data = AUDIO_QUEUE.get()
            data = data.flatten()  # Convert (2048, 1) to (2048,)
            print(f"Data shape: {data.shape}, Data size: {data.size}")  # Debug line
            rms = np.sqrt(np.mean(data**2))
            count += 1
            window_data = dsp.preprocess_buffer(data)
            print(f"[{count}] RMS Level: {rms:.6f}", flush=True)

            result = dsp.calculate_difference_function(window_data)
            cmnd = dsp.calculate_cumulative_mean_normalized_difference_function(result)
            min_index = dsp.peak_valley_detection(cmnd)
            if min_index is None:
                print(f"[{count}] Pitch detection failed (no peak found)")
            elif min_index <= 0:
                print(f"[{count}] Invalid min_index: {min_index}")
            else:
                detected_data["frequency"] = rate / min_index
                print(f"[{count}] Detected frequency: {detected_data['frequency']:.2f} Hz")
                note, cents_off = dsp.frequency_to_note_cent(detected_data['frequency'])
                detected_data["note"] = note
                detected_data["cents_off"] = cents_off
                print(f"[{count}] Detected note: {note}, Cents off: {cents_off:.2f}", flush=True)




audio_thread = threading.Thread(target=audio_processing_loop, daemon=True)
audio_thread.start()




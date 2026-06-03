import numpy as np
import queue
import sounddevice
import sys
import time

AUDIO_QUEUE = queue.Queue(maxsize=1)
callback_count = 0

def audio_callback(indata, frames, time, status):
    global callback_count
    callback_count += 1
    
    if status:
        print(f"[Callback #{callback_count}] Status: {status}", file=sys.stderr, flush=True)

    try:
        AUDIO_QUEUE.put(indata.copy(), block=False)
    except queue.Full:
        AUDIO_QUEUE.get_nowait()  # Discard the oldest frame
        AUDIO_QUEUE.put(indata.copy(), block=False)


def start_stream():
    device_id = 22
    device_info = sounddevice.query_devices(device_id)
    print(f"[INFO] Device info for device {device_id}: {device_info}", flush=True)
    
    # Find a supported sample rate
    supported_rates = [44100, 48000, 22050, 16000, 8000]
    sample_rate = None
    
    for rate in supported_rates:
        try:
            # Test if this sample rate is supported
            sounddevice.check_input_device(device_id, channels=1, samplerate=rate)
            sample_rate = rate
            print(f"[INFO] Using sample rate: {sample_rate} Hz", flush=True)
            break
        except:
            continue
    
    if sample_rate is None:
        # Fallback: use device's default sample rate
        sample_rate = int(device_info['default_samplerate'])
        print(f"[INFO] Using device default sample rate: {sample_rate} Hz", flush=True)
    
    print(f"[INFO] Creating InputStream with device={device_id} (Stereo Mix), sample_rate={sample_rate}", flush=True)
    input_stream = sounddevice.InputStream(device=device_id, channels=1, samplerate=sample_rate, blocksize=2048, callback=audio_callback, dtype='float32')
    print(f"[INFO] Stream created, calling start()...", flush=True)
    input_stream.start()
    print(f"[INFO] Stream started. Waiting for callbacks...", flush=True)
    # Give the stream a moment to stabilize
    time.sleep(0.5)
    return input_stream

def stop_stream(input_stream):
    try:
        input_stream.stop()
        input_stream.close()
    except Exception as e:
        print(f"Error stopping stream: {e}")
    finally:
        while not AUDIO_QUEUE.empty():
            AUDIO_QUEUE.get()


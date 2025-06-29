import queue
import sounddevice as sd
import vosk
import json
from state_manager import is_awake
import threading

model = vosk.Model("vosk-model-small-en-us-0.15")
q = queue.Queue()
def audio_callback(indata, frames, time, status):
    q.put(bytes(indata))

# Define keywords and exit flag
wake_keywords = ["arise", "hi arise" , "wake up", "hello arise", "arise wake up", "arise hello","hey","hi", "arise hi","hello"]
exit_keywords = ["exit", "quit", "stop", "shutdown"]
exit_flag = threading.Event()

def listen_for_wake_word(trigger_callback, stop_callback=None):
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=audio_callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        print("🟡 ARISE is sleeping... Say 'Arise' or 'Hi Arise' to wake.")

        while not exit_flag.is_set():
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "").lower().strip()
                if text:
                    print("Heard:", text)

                if any(kw in text for kw in wake_keywords):
                    if not is_awake.is_set():
                        print("✅ Wake phrase detected!")
                        is_awake.set()  # Set awake state
                        trigger_callback()
                    else:
                        print("ℹ️ ARISE already awake, ignoring wake phrase.")

                elif any(kw in text for kw in exit_keywords):
                    print("⛔ Exit phrase detected.")
                    if stop_callback:
                        stop_callback()
                    exit_flag.set()
                    break

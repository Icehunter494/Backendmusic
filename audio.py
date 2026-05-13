import wave
import numpy as np

def load_wav(filename):
    with wave.open(filename, 'rb') as w:
        frames = w.readframes(w.getnframes())

        sr = w.getframerate()
        channels = w.getnchannels()

        # convert to int16 safely
        audio = np.frombuffer(frames, dtype=np.int16)

        # convert stereo → mono if needed
        if channels == 2:
            audio = audio.reshape(-1, 2).mean(axis=1).astype(np.int16)

        return audio, sr
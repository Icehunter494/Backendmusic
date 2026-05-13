import wave
import struct

def load_wav(filename):
    with wave.open(filename, 'rb') as w:
        frames = w.readframes(w.getnframes())

        sr = w.getframerate()
        channels = w.getnchannels()

        # correct format string
        fmt = "<" + str(w.getnframes() * channels) + "h"
        samples = struct.unpack(fmt, frames)

        # convert stereo → mono
        if channels == 2:
            samples = [
                (samples[i] + samples[i+1]) // 2
                for i in range(0, len(samples), 2)
            ]

        return samples, sr
import wave
import struct

def load_wav(filename):
    with wave.open(filename, 'rb') as w:
        frames = w.readframes(w.getnframes())

        samples = struct.unpack(
            "<" + str(w.getnframes()) + "h",
            frames
        )

        sr = w.getframerate()

        return samples, sr
import wave
import struct

def load_wav(filename):
    with wave.open(filename, 'rb') as w:
        frames = w.readframes(w.getnframes())

        samples = struct.unpack("<" + str(w.getnframes()) + "h", frames)

        return samples, w.getframerate
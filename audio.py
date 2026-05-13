import wave
import struct

def load_wav(filename):

    with wave.open(filename, 'rb') as w:
        n_frames = w.getnframes()
        sample_rate = w.getframerate()

        raw = w.readframes(n_frames)

        samples = struct.unpack("<" + str(n_frames) + "h", raw)

        return samples, sample_rate
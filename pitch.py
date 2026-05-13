import math


def autocorrelation(signal, max_lag=1000):

    result = []

    for lag in range(1, max_lag):
        total = 0

        for i in range(len(signal) - lag):
            total += signal[i] * signal[i + lag]

        result.append(total)
    
    return result

def detect_pitch(frame, sr):

    corr = autocorrelation(frame, 800)
    #ignore sub bass
    start = 30
    corr = corr[start:]

    if not corr: return 0

    peak = max(corr)

    if peak <= 0:
        return 0
    
    lag = corr.index(peak) + start

    if lag <= 0:
        return 0
    
    return sr / lag


#music theory conver
def freq_to_midi(freq):
    if freq <= 0:
        return None
    return 12 * math.log2(freq / 440) + 69


def midi_to_note_name(midi):
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    note = int(round(midi))
    name = notes[note % 12]
    octave = (note // 12) - 1

    return f"{name}{octave}"

#guitar map

OPEN_STRINGS = {
    6: 40, # E2
    5: 45, # A2
    4: 50, # D3
    3: 55, # G3
    2: 59, # B3
    1: 64 # E4
}


def midi_to_tab(midi):


    best = None
    
    for string, open_midi in OPEN_STRINGS.items():
        fret = round(midi - open_midi)

        if 0 <= fret <= 24:
            error = abs((open_midi + fret) - midi)

            if best is None or error < best["error"]:
                best = {
                    "string": string,
                    "fret": fret,
                    "error": error
                }
    
    if best is None:
        return None
    
    return {
        "string": best["string"],
        "fret": best["fret"]
    }

#frame proc

def analyze_audio(samples, sr):

    FRAME_SIZE = 2048
    HOP = 1024

    frames = []

    for i in range(0, len(samples) - FRAME_SIZE, HOP):
        frame = samples[i:i + FRAME_SIZE]

        freq = detect_pitch(frame, sr)
        midi = freq_to_midi(freq)

        if midi is None:
            continue

        tab = midi_to_tab(midi)

        if tab is None:
            continue

        frames.append({
            "start": i / sr,
            "end": (i + FRAME_SIZE) / sr,
            "freq": freq,
            "midi": midi,
            **tab
        })

#frame event grouping

def group_notes(frames):


    if not frames:
        return []
    
    events = []
    current = frames[0]

    for f in frames[1:]:
        same_note = (
            f["string"] == current["string"] and
            f["fret"] == current["fret"]
        )

        if same_note:
            current["end"] = f["end"]
        else:
            events.append(current)
            current = f
    
    events.append(current)

    return events
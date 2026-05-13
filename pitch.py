import math

def autocorrelation(signal, max_lag=1000):
    result = []
    
    for lag in range(1, max_lag):
        total = 0
        for i in range(len(signal)-lag):
            total += signal[i] * signal[i + lag]
        result.append(total)

    return result

def freq_to_note_number(freq):
    return 12 * math.log2(freq / 440) + 69

def note_to_tab(note_number):
    #estand
    open_strings = {
        6: 40, #E2
        5: 45, #A2
        4: 50, #D3
        3: 55, #G3
        2: 59, #B3
        1: 64 
    }

    best = None
    best_string = None
    best_fret = None

    for string, open_midi in open_strings.items():
        fret = round(note_number - open_midi)

        if 0 <= fret <= 24:
            if best is None or abs(fret) < abs(best):
                best = fret
                best_string = string
                best_fret = fret
    
    return {
        "string": best_string,
        "fret": best_fret
    }

def detect_pitch(frame, sr):
    corr = autocorrelation(frame)
    peak = max(corr)
    lag = corr.index(peak) + 1

    freq = sr / lag
    return freq

def analyze_audio(samples, sr):
    FRAME = 2048
    result = []

    for i in range(0, len(samples), FRAME):
        frame = samples[i:i+FRAME]

        if len(frame) < FRAME:
            continue

        freq = detect_pitch(frame, sr)

        note = 12 * math.log2(freq / 440) + 69

        tab = note_to_tab(note)

        result.append({
            "start": i / sr,
            "end": (i + FRAME) / sr,
            **tab
        })
    return result

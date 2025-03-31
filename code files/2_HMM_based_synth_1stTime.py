import numpy as np
import hmmlearn.hmm as hmm
from scipy.signal import chirp, sawtooth
import wave

# Define phoneme frequency patterns
phoneme_frequencies = {
    'c': [250, 300, 280],  # Consonant-like
    'a': [600, 700, 650],  # Vowel-like
    't': [400, 450, 420],  # Stop consonant
    'd': [220, 270, 260],  # Consonant-like
    'o': [500, 550, 520],  # Vowel-like
    'g': [350, 400, 370]   # Consonant-like
}

# Prepare training data
X_train = []
lengths = []
for phoneme, freqs in phoneme_frequencies.items():
    sequence = np.array(freqs).reshape(-1, 1)
    X_train.append(sequence)
    lengths.append(len(sequence))
X_train = np.vstack(X_train)

# Train HMM model
hmm_model = hmm.GaussianHMM(n_components=3, covariance_type="diag", n_iter=100)
hmm_model.fit(X_train, lengths)

def generate_speech(word_phonemes, filename):
    generated_sequence = []
    for phoneme in word_phonemes:
        _, states = hmm_model.decode(np.array(phoneme_frequencies[phoneme]).reshape(-1, 1))
        predicted_freqs = hmm_model.means_[states]
        generated_sequence.extend(predicted_freqs.flatten())
    
    # Convert frequencies to waveform
    waveform = generate_wave(generated_sequence)
    
    # Save waveform as WAV file
    with wave.open(filename, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(waveform.tobytes())
    print(f"Generated speech saved as {filename}")

def generate_wave(freqs, duration=0.1, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))
    waveform = np.sin(2 * np.pi * np.array(freqs)[:, None] * t).sum(axis=0)
    return np.int16(waveform / np.max(np.abs(waveform)) * 32767)

# Generate speech for "cat" and "dog"
generate_speech(['c', 'a', 't'], "hmm_cat.wav")
generate_speech(['d', 'o', 'g'], "hmm_dog.wav")

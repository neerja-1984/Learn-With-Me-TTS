import numpy as np
import hmmlearn.hmm as hmm
import librosa
import librosa.display
import soundfile as sf
import matplotlib.pyplot as plt
import os

def extract_mfcc(audio_path, n_mfcc=13):
    """Extract MFCC features from an audio file."""
    y, sr = librosa.load(audio_path, sr=16000)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    return mfcc.T  # Transpose to make it time-major

# Load training data for "dog"
training_files = ["wav_files/DOG waves/DOG.wav", "wav_files/DOG waves/dog2.wav" , "wav_files/DOG waves/The Quick Brown DOG.wav"]  # Replace with real phoneme files for "dog"
training_data = []

for file in training_files:
    mfcc_features = extract_mfcc(file)
    training_data.append(mfcc_features)

# Flatten all data for HMM training
X = np.vstack(training_data)
print("MFCC Features :",X)
lengths = [len(data) for data in training_data]

# Train HMM
hmm_model = hmm.GaussianHMM(n_components=5, covariance_type="diag", n_iter=1000)
hmm_model.fit(X, lengths)

def generate_speech_sequence(length=50):
    """Generate a phoneme sequence using the trained HMM."""
    generated_features, _ = hmm_model.sample(length)
    return generated_features

def synthesize_audio(mfcc_features, output_file="dog_output_2.wav", sr=16000):
    """Convert MFCC back to waveform using Griffin-Lim algorithm. -> this is a vocoder"""
    reconstructed_audio = librosa.feature.inverse.mfcc_to_audio(mfcc_features.T)
    sf.write(output_file, reconstructed_audio, sr)
    print(f"Generated speech for 'dog' saved to {output_file}")

# Generate new speech features and synthesize speech
new_features = generate_speech_sequence()
synthesize_audio(new_features)

# Visualize MFCCs
plt.figure(figsize=(10, 4))
librosa.display.specshow(new_features.T, x_axis='time', cmap='viridis')
plt.colorbar()
plt.title("Generated MFCCs for 'dog'")
plt.show()

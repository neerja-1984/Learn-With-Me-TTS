import librosa
import numpy as np
import librosa.display
import matplotlib.pyplot as plt
import os

def classify_sound(file_path):
    # remove the file name from path
    figure_name = file_path.split('/')[-1]

    # Load audio file
    y, sr = librosa.load(file_path, sr=None)
    
    # Compute Spectrogram
    S = np.abs(librosa.stft(y))
    spectral_centroid = librosa.feature.spectral_centroid(S=S, sr=sr)
    spectral_flatness = librosa.feature.spectral_flatness(S=S)
    
    # Mean values
    centroid_mean = np.mean(spectral_centroid)
    flatness_mean = np.mean(spectral_flatness)
    
    # Thresholds (approximate values, adjust as needed)
    vowel_threshold = 2000  # Hz
    flatness_threshold = 0.1
    
    if centroid_mean < vowel_threshold and flatness_mean < flatness_threshold:
        print(f'Detected: Vowel : {figure_name}')
    else:
        print(f'Detected: Consonant : {figure_name}')

    # Display Spectrogram
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title(f'Spectrogram of {figure_name}')
    plt.show()

for file in os.listdir('wav_files'):
    classify_sound(f'wav_files/{file}')

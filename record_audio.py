import os
import sounddevice as sd
from scipy.io.wavfile import write

# Set recording parameters
samplerate = 16000  # 16kHz sample rate
channels = 1        # Mono audio
duration = 5        # Duration in seconds

# Ensure the uploads folder exists
os.makedirs("backend/uploads", exist_ok=True)

# File path to save the recording
file_path = "backend/uploads/test_audio.wav"

# Start recording
print("Recording for 5 seconds. Please speak into the microphone...")
audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=channels, dtype='int16')
sd.wait()  # Wait until recording is finished

# Save the recording as a WAV file
write(file_path, samplerate, audio_data)

print(f"Recording complete. Audio saved to: {file_path}")
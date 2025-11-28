"""
This module handles audio transcription 
using Vosk and manages transcript storage in SQLite.
"""

import wave
import json
from vosk import Model, KaldiRecognizer

def transcribe_audio(file_path, model_path):
    """
    Transcribes an audio file using the Vosk model.

    Args:
        file_path (str): Path to the audio file (.wav format).
        model_path (str): Path to the Vosk model directory.

    Returns:
        str: Transcribed text from the audio.
    """
    # Load the Vosk model from the provided path
    model = Model(model_path)
    wf = wave.open(file_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())

    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            results.append(result.get("text", ""))

    final_result = json.loads(rec.FinalResult()).get("text", "")
    if final_result:
        results.append(final_result)

    return " ".join(results)

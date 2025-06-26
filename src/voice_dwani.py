import whisper
import pyaudio
import wave
import numpy as np
import time
import os
from difflib import SequenceMatcher  # For fuzzy matching

# Audio recording parameters
RATE = 16000  # Sample rate (Hz)
CHUNK = 1024  # Buffer size
WAKE_WORD = "dwani"
# Fallback words for fuzzy matching (common mis-transcriptions)
FALLBACK_WORDS = ["dwani", "dwayne", "duane", "dwanee", "dvani"]

def record_audio(filename, duration=3, wake_word_mode=True):
    """Record audio from the microphone and save to a WAV file."""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
    
    print("Recording..." if wake_word_mode else "Recording command...")
    frames = []
    
    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    return filename

def transcribe_audio(filename, model):
    """Transcribe audio using Whisper."""
    try:
        result = model.transcribe(filename, fp16=False)
        text = result["text"].strip().lower()
        print(f"Raw Transcription: '{text}'")
        return text
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

def is_wake_word_detected(text, wake_word=WAKE_WORD, threshold=0.8):
    """Check if wake word or similar is in the transcribed text."""
    if not text:
        return False
    
    # Exact match
    if wake_word.lower() in text:
        return True
    
    # Fuzzy match for similar words
    for word in text.split():
        for fallback in FALLBACK_WORDS:
            similarity = SequenceMatcher(None, word, fallback).ratio()
            if similarity >= threshold:
                print(f"Fuzzy match: '{word}' matches '{fallback}' (similarity: {similarity:.2f})")
                return True
    return False

def listen_for_wake_word(model, wake_word=WAKE_WORD):
    """Listen continuously for the wake word."""
    attempt = 1
    while True:
        print(f"Attempt {attempt}: Listening for wake word '{wake_word}'...")
        filename = f"temp_wake_{attempt}.wav"
        record_audio(filename, duration=3, wake_word_mode=True)
        
        text = transcribe_audio(filename, model)
        
        if os.path.exists(filename):
            os.remove(filename)
        
        if is_wake_word_detected(text, wake_word):
            print(f"Wake word detected in: '{text}'")
            return True
        
        attempt += 1
        time.sleep(0.1)  # Avoid CPU overload

def listen_and_transcribe(model):
    """Listen for a command after wake word detection."""
    filename = "temp_command.wav"
    record_audio(filename, duration=10, wake_word_mode=False)
    
    text = transcribe_audio(filename, model)
    
    if os.path.exists(filename):
        os.remove(filename)
    
    return text

def main():
    print("Loading Whisper 'small' model...")
    model = whisper.load_model("medium")  # Changed to small model
    print("Model loaded successfully.")
    
    while True:
        if listen_for_wake_word(model, wake_word=WAKE_WORD):
            command = listen_and_transcribe(model)
            if command:
                print(f"Transcribed Command: '{command}'")
                if "what do you see" in command.lower():
                    print("Command recognized: Triggering camera action...")
                    # Add camera logic here
                else:
                    print(f"Command '{command}' not recognized.")
                
                if "exit" in command.lower():
                    print("Exiting...")
                    break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped by user.")
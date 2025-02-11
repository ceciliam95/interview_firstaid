# import pyttsx3
# engine = pyttsx3.init()
# engine.say("Can you tell me a time when you have to deal with difficult stakeholders?")
# engine.runAndWait()

from gtts import gTTS
from playsound import playsound
import tempfile
import os

# # Generate speech
# tts = gTTS("Can you tell me a time when you have to deal with difficult stakeholders?", lang="en")
#
# # Save to a temporary file and play it
# with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
#     temp_filename = temp_audio.name  # Get the file path
#     tts.save(temp_filename)  # Save TTS output
#
# # Play the audio file
# playsound(temp_filename)
#
# # Delete the file after playback
# os.remove(temp_filename)

# from google.cloud import texttospeech
#
# client = texttospeech.TextToSpeechClient()
#
# synthesis_input = texttospeech.SynthesisInput(text="Hello, world!")
# voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
# audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
#
# response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
#
# # Save & Play
# with open("output.mp3", "wb") as out:
#     out.write(response.audio_content)

import openai
import tempfile
import os
import pygame
from backend.secret import  OPENAI_API_KEY

os.environ["OpenAI_API_KEY"] = OPENAI_API_KEY

# Generate the speech
response = openai.audio.speech.create(
    model="tts-1",  # Choose the TTS model (e.g., "alloy", "echo", "fable")
    voice="fable",  # Available voices: "alloy", "echo", "fable", etc.
    input="Can you tell me a time when you have to deal with difficult stakeholders?"
)

# Save the audio to a temporary file
with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
    temp_filename = temp_audio.name  # Get the temporary file path
    temp_audio.write(response.content)  # Write the speech audio to the file

# Initialize pygame mixer
pygame.mixer.init()

# Load the temporary audio file and play it
pygame.mixer.music.load(temp_filename)
pygame.mixer.music.play()

# Keep the script running until the audio is finished
while pygame.mixer.music.get_busy():
    pass

# Clean up: delete the temporary file after playback
os.remove(temp_filename)

# Here trying the google text to speech library.
from gtts import gTTS
import os

# German text
text = "Guten Tag! Wie geht es Ihnen? Ich hoffe, Sie haben einen schönen Tag."

# Convert text to speech
tts = gTTS(text=text, lang='de')

# Save the audio file
audio_file = "german_text.mp3"
tts.save(audio_file)

# Play the audio file (optional)
#os.system(f"start {audio_file}")  # For Windows
# os.system(f"afplay {audio_file}")  # For macOS
# os.system(f"xdg-open {audio_file}")  # For Linux

print(f"Audio saved as {audio_file}")


from gtts import gTTS

def narrate_story(text, filename="images/narration.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    print(f"Narration saved as {filename}")


narrate_story("Once upon a time, in a land far away, there lived a brave knight who fought dragons and saved kingdoms.")
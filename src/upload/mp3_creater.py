from gtts import gTTS

text = "Hello, how are you? I am fine, thanks! It's nice to meet you."
tts = gTTS(text)
tts.save("greetings.mp3")

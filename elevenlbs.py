import elevenlabs
import ffmpeg
elevenlabs.set_api_key("9fc50a629f7f996b04c9d73a8fe96ef3")
voice = elevenlabs.Voice(
    voice_id = "g5CIjZEefAph4nQFvHAz",
    settings = elevenlabs.VoiceSettings(
        stability = 1,
        similarity_boost = 0.75
    )
)
 
audio = elevenlabs.generate(
    text = "Hi, I'm from the future!",
    voice = voice
)
 
elevenlabs.play(audio)
elevenlabs.save(audio, "audio.mp3")
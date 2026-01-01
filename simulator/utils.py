import os
import uuid
import wave

import pyaudio
# import whisper
from django.conf import settings
from django.utils import timezone
from pydub import AudioSegment


def generate_id():
    """
    Generates a unique identifier for audio files

    Returns:
    str: Unique identifier
    """

    return str(uuid.uuid4().hex[:8])  # Shorten to 8 characters for simplicity


def upload_path(instance):
    return f"{instance.user.email}/"


# ========================
# Audio Recording Module
# ========================
def record_audio(user, duration: int = 5) -> None:

    chunk = 1024
    FORMAT = pyaudio.paInt16
    channels = 1
    rate = 16000  # Sample rate compatible with Whisper

    media_path = os.path.join(settings.MEDIA_ROOT, "user_audio", user.email)

    now = timezone.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")

    filename = os.path.join(media_path, f"{timestamp}.wav")

    os.makedirs(media_path, exist_ok=True)

    p = pyaudio.PyAudio()

    try:
        stream = p.open(
            format=FORMAT,
            channels=channels,
            rate=rate,
            input=True,
            frames_per_buffer=chunk,
        )

        frames = []
        print(f"Recording {duration} seconds...")

        # Capture audio in chunks to prevent buffer overflow
        for _ in range(0, int(rate / chunk * duration)):
            data = stream.read(chunk, exception_on_overflow=False)
            frames.append(data)

        # Save raw audio data
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(rate)
            wf.writeframes(b"".join(frames))

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

    print(f"Recording saved to {filename}")
    convert_audio(
        input_path=filename,
        output_format="mp3",
    )


def convert_audio(input_path, output_format="mp3", bitrate=None, mpeg_layer=None):
    output_path = str(input_path).replace("wav", output_format)
    # Load input file
    audio = AudioSegment.from_file(input_path)

    # Prepare export parameters
    params = {"format": output_format}

    if bitrate:
        params["bitrate"] = bitrate

    # Handle MPEG layer specification
    if output_format in {"mp1", "mp2", "mp3"} and mpeg_layer:
        params["codec"] = f"mp{mpeg_layer}"

    # Special handling for MPEG formats
    if output_format == "mpeg" or output_format == "mpg":
        params["format"] = "mp3"  # Default to MP3 for .mpeg/.mpg containers
        if not output_path.endswith((".mpeg", ".mpg")):
            output_path += ".mpeg"

    # Export the file
    audio.export(output_path, **params)
    return output_path


# ========================
# Speech Processing Module
# ========================


# def transcribe_audio(file_path: str) -> str:
#     """
#     Converts speech to text using OpenAI's Whisper

#     Args:
#     file_path (str): Path to audio file

#     Returns:
#     str: Transcribed text (lowercase, no punctuation)

#     Reference: Radford et al. (2022) Robust Speech Recognition
#     via Large-Scale Weak Supervision
#     """
#     model = whisper.load_model(name="small")
#     result = model.transcribe(audio=file_path, verbose=True, language="fr")
#     print(f"===> Detected Language: {result['language']} <====")
#     return str(result["text"]).strip()


def text_to_speech(text: str, output_path: str = ".", lang: str = "fr") -> str:
    """
    Converts text to speech audio file using Google Text-to-Speech

    Args:
        text (str): Text to convert to speech
        output_path (str): Path where audio file will be saved
        lang (str): Language code (default: "fr" for French)

    Returns:
        str: Path to the generated audio file

    Example:
        >>> text_to_speech("Bonjour, comment allez-vous?", "/path/to/output.mp3")
    """

    from gtts import gTTS

    # Create TTS object and save to file
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(output_path)

    return output_path

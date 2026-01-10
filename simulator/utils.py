import os
import random
import uuid

# import whisper
from django.conf import settings
from django.utils import timezone
from pydub import AudioSegment
from gtts import gTTS


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
# Audio Conversion Module
# ========================
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

    # Create TTS object and save to file
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(output_path)

    return output_path


def concatenate_dialogue_audio(dialogue):
    """
    Concatenates all line recordings for a dialogue into one audio file

    Args:
        dialogue: Dialogue model instance

    Returns:
        str: Path to concatenated audio file or None if no recordings
    """

    lines = dialogue.lines.filter(recording__isnull=False).order_by("order")

    if not lines.exists():
        return None

    combined = AudioSegment.empty()

    for line in lines:
        try:
            audio_path = line.recording.audio_file.path
            audio = AudioSegment.from_file(audio_path)
            combined += audio + AudioSegment.silent(duration=random.randint(500, 1000))
        except Exception:
            continue

    if len(combined) == 0:
        return None

    output_path = os.path.join(
        settings.MEDIA_ROOT,
        "dialogues",
        "complete",
        f"dialogue_{dialogue.id}_{dialogue.title}.mp3",
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    combined.export(output_path, format="mp3")
    return f"dialogues/complete/dialogue_{dialogue.id}_{dialogue.title}.mp3"


def generate_simulation_audio(simulation):
    """
    Generates complete simulation audio by concatenating all dialogue audios
    with TTS title transitions and 2-second pauses

    Args:
        simulation: Simulation model instance

    Returns:
        str: Path to simulation audio file or None if no dialogue audios
    """
    import tempfile

    dialogues = simulation.dialogues.filter(complete_audio__isnull=False).order_by(
        "order"
    )

    if not dialogues.exists():
        return None

    combined = AudioSegment.empty()

    for dialogue in dialogues:
        try:
            # Generate TTS for dialogue title
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                title_audio_path = tmp.name
            text_to_speech(dialogue.title, title_audio_path, lang="fr")
            title_audio = AudioSegment.from_file(title_audio_path)

            # Add title + 2s pause + dialogue audio + 2s pause
            combined += title_audio + AudioSegment.silent(duration=2000)
            dialogue_audio = AudioSegment.from_file(dialogue.complete_audio.path)
            combined += dialogue_audio + AudioSegment.silent(duration=2000)

            # Cleanup temp file
            os.unlink(title_audio_path)
        except Exception:
            continue

    if len(combined) == 0:
        return None

    output_path = os.path.join(
        settings.MEDIA_ROOT,
        "simulations",
        "final",
        f"simulation_{simulation.id}_{simulation.title}.mp3",
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    combined.export(output_path, format="mp3")
    return f"simulations/final/simulation_{simulation.id}_{simulation.title}.mp3"

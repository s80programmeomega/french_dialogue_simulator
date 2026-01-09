#!/usr/bin/env python
"""Test audio concatenation with generated TTS samples"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from simulator.models import Dialogue, DialogueLine, LineRecording
from simulator.utils import text_to_speech
from django.conf import settings

# Get first dialogue
dialogue = Dialogue.objects.first()

if not dialogue:
    print("No dialogues found in database")
    exit(1)

print(f"Testing with dialogue: {dialogue.title}")
print(f"Total lines: {dialogue.lines.count()}")

# Generate TTS for first 2 lines as test
lines = dialogue.lines.all()[:2]

for line in lines:
    print(f"\nGenerating audio for line {line.order}: {line.text[:50]}...")
    
    output_path = os.path.join(
        settings.MEDIA_ROOT, 
        "simulations", 
        "lines", 
        f"test_line_{line.id}.mp3"
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Generate TTS
    text_to_speech(line.text, output_path, lang="fr")
    
    # Create recording
    LineRecording.objects.update_or_create(
        dialogue_line=line,
        defaults={"audio_file": f"simulations/lines/test_line_{line.id}.mp3"}
    )
    print(f"  ✓ Audio generated and saved")

# Now test concatenation
print("\n" + "="*50)
print("Testing complete dialogue audio generation...")

result = dialogue.generate_complete_audio()

if result:
    print(f"✓ SUCCESS! Complete audio saved to: {dialogue.complete_audio}")
    print(f"  File path: {dialogue.complete_audio.path}")
    print(f"  File exists: {os.path.exists(dialogue.complete_audio.path)}")
else:
    print("✗ FAILED - Audio generation returned False")

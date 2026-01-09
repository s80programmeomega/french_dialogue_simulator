#!/usr/bin/env python
"""Test script for complete dialogue audio generation"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from simulator.models import Dialogue, LineRecording

# Find a dialogue with recordings
dialogues = Dialogue.objects.all()

print(f"Total dialogues: {dialogues.count()}")

for dialogue in dialogues:
    lines_with_recordings = dialogue.lines.filter(recording__isnull=False).count()
    total_lines = dialogue.lines.count()
    
    print(f"\nDialogue: {dialogue.title}")
    print(f"  Lines with recordings: {lines_with_recordings}/{total_lines}")
    
    if lines_with_recordings > 0:
        print(f"  Testing audio generation...")
        result = dialogue.generate_complete_audio()
        
        if result:
            print(f"  ✓ Success! Audio saved to: {dialogue.complete_audio}")
        else:
            print(f"  ✗ Failed - no recordings found")
    else:
        print(f"  Skipping - no recordings available")

print("\n" + "="*50)
print("Test complete!")

#!/usr/bin/env python
"""Test script for simulation overall audio generation"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from simulator.models import Simulation, Dialogue

print("=" * 60)
print("SIMULATION AUDIO GENERATION TEST")
print("=" * 60)

simulations = Simulation.objects.all()
print(f"\nTotal simulations: {simulations.count()}")

for simulation in simulations:
    print(f"\n{'=' * 60}")
    print(f"Simulation: {simulation.title}")
    print(f"Status: {simulation.status}")
    
    dialogues = simulation.dialogues.all()
    dialogues_with_audio = simulation.dialogues.filter(complete_audio__isnull=False).count()
    
    print(f"Dialogues: {dialogues.count()}")
    print(f"Dialogues with audio: {dialogues_with_audio}/{dialogues.count()}")
    
    if dialogues_with_audio > 0:
        print(f"\nGenerating simulation audio...")
        from simulator.utils import generate_simulation_audio
        
        audio_path = generate_simulation_audio(simulation)
        
        if audio_path:
            simulation.final_audio = audio_path
            simulation.save()
            print(f"✓ SUCCESS! Audio saved to: {simulation.final_audio}")
            print(f"  File path: {simulation.final_audio.path}")
            print(f"  File exists: {os.path.exists(simulation.final_audio.path)}")
        else:
            print(f"✗ FAILED - Audio generation returned None")
    else:
        print(f"\nSkipping - no dialogue audios available")
        print(f"Tip: Generate dialogue audios first using test_audio_generation.py")

print("\n" + "=" * 60)
print("TEST COMPLETE!")
print("=" * 60)

# Audio Generation System - Overview

## Introduction
The French Dialogue Simulator includes a comprehensive audio generation system that creates, processes, and manages audio files at multiple levels: individual lines, complete dialogues, and full simulations.

## Audio Generation Levels

### 1. Line-Level Audio
- **User Recordings**: Captured via browser microphone
- **System TTS**: Auto-generated using Google Text-to-Speech (gTTS)
- **Storage**: `media/simulations/lines/`

### 2. Dialogue-Level Audio
- **Complete Dialogue**: Concatenation of all line recordings
- **Auto-generated**: When all lines in a dialogue are recorded
- **Storage**: `media/dialogues/complete/`

### 3. Simulation-Level Audio
- **Final Audio**: Complete simulation with TTS titles and transitions
- **Auto-generated**: When simulation is terminated
- **Storage**: `media/simulations/final/`

## Key Features

### Automatic Generation
- Line audio generates on-demand (TTS for system participants)
- Dialogue audio generates when all lines are complete
- Simulation audio generates automatically on termination

### Download Capabilities
- Individual dialogue audio download
- Complete simulation audio download
- Proper filename formatting

### Audio Processing
- Concatenation with silence gaps (0.5-1s between lines, 2s between dialogues)
- MP3 format output
- French TTS for system participants and titles

## Technical Stack
- **TTS Engine**: Google Text-to-Speech (gTTS)
- **Audio Processing**: PyDub (AudioSegment)
- **Format**: MP3
- **Language**: French (fr)

## File Structure
```
media/
├── simulations/
│   ├── lines/          # Individual line recordings
│   └── final/          # Complete simulation audio
└── dialogues/
    └── complete/       # Complete dialogue audio
```

## Related Documentation
- [Technical Implementation](./TECHNICAL_IMPLEMENTATION.md)
- [User Guide](./USER_GUIDE.md)
- [API Reference](./API_REFERENCE.md)
- [Troubleshooting](./TROUBLESHOOTING.md)
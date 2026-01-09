# Audio Generation Documentation Index

## Overview
This directory contains comprehensive documentation for the French Dialogue Simulator's audio generation system.

## Documentation Files

### 📋 [AUDIO_GENERATION_OVERVIEW.md](./AUDIO_GENERATION_OVERVIEW.md)
**Purpose**: High-level overview of the audio generation system
**Contents**:
- System architecture overview
- Audio generation levels (line, dialogue, simulation)
- Key features and capabilities
- File structure and storage

### 🔧 [TECHNICAL_IMPLEMENTATION.md](./TECHNICAL_IMPLEMENTATION.md)
**Purpose**: Detailed technical documentation for developers
**Contents**:
- Core function implementations
- Database model structures
- API endpoint specifications
- Automatic trigger mechanisms
- Dependencies and requirements

### 👤 [USER_GUIDE.md](./USER_GUIDE.md)
**Purpose**: End-user instructions and best practices
**Contents**:
- Recording user audio
- System audio generation
- Download procedures
- Settings configuration
- Workflow optimization tips

### 🔌 [API_REFERENCE.md](./API_REFERENCE.md)
**Purpose**: Complete API documentation for integration
**Contents**:
- Endpoint specifications
- Request/response formats
- JavaScript integration examples
- Error handling
- Rate limiting information

### 🛠️ [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
**Purpose**: Common issues and solutions
**Contents**:
- Recording problems
- TTS generation issues
- Download problems
- Performance optimization
- Debugging tools and techniques

## Quick Reference

### Key Components
- **TTS Engine**: Google Text-to-Speech (gTTS)
- **Audio Processing**: PyDub AudioSegment
- **Storage Format**: MP3
- **Recording Format**: WebM (browser native)

### Main Features
- ✅ User audio recording via browser
- ✅ Automatic TTS for system participants
- ✅ Dialogue audio concatenation
- ✅ Complete simulation audio generation
- ✅ Automatic generation on simulation termination
- ✅ Download capabilities with proper filenames

### File Locations
```
media/
├── simulations/
│   ├── lines/          # Individual recordings
│   └── final/          # Complete simulation audio
└── dialogues/
    └── complete/       # Complete dialogue audio
```

## Getting Started

### For Users
1. Start with [USER_GUIDE.md](./USER_GUIDE.md)
2. Configure settings for optimal workflow
3. Refer to [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) if issues arise

### For Developers
1. Review [AUDIO_GENERATION_OVERVIEW.md](./AUDIO_GENERATION_OVERVIEW.md)
2. Study [TECHNICAL_IMPLEMENTATION.md](./TECHNICAL_IMPLEMENTATION.md)
3. Use [API_REFERENCE.md](./API_REFERENCE.md) for integration

### For System Administrators
1. Check [TECHNICAL_IMPLEMENTATION.md](./TECHNICAL_IMPLEMENTATION.md) for dependencies
2. Review [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for common issues
3. Monitor file storage and permissions

## Version Information
- **Created**: Current implementation
- **Last Updated**: Latest feature additions
- **Compatibility**: Modern browsers with MediaRecorder API support

## Related Documentation
- [Dialogue Settings Documentation](../dialogue_settings/)
- [Main Project Documentation](../../README.md)
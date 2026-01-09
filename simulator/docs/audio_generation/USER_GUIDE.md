# User Guide - Audio Generation Features

## Overview
The audio generation system allows you to create, manage, and download audio files for your French dialogue practice sessions.

## Recording User Audio

### Manual Recording
1. **Navigate** to simulation run page
2. **Click** the red "Enregistrer" button for your lines
3. **Speak** into your microphone
4. **Click** "Arrêter" to finish recording
5. **Audio** automatically saves and plays

### Auto-Record Mode
1. **Open** settings modal (gear icon)
2. **Enable** "Enregistrement automatique"
3. **Recording** starts automatically when line becomes active

## System Audio Generation

### Automatic TTS
- System participant lines generate French TTS automatically
- Click "Écouter" button to generate and play
- Audio saves for future playback

### Auto-Play Settings
- **Enabled** (default): Audio plays immediately after generation
- **Disabled**: Manual playback control

## Dialogue Audio

### Complete Dialogue Generation
- **Automatic**: Generated when all lines are recorded
- **Manual**: Click "Générer Audio Global" button
- **Download**: Available via download button
- **Format**: MP3 with silence gaps between lines

### Features
- Combines all line recordings in order
- Adds natural pauses (0.5-1 second) between lines
- Downloadable with descriptive filename

## Simulation Audio

### Final Audio Generation
- **Automatic**: Generated when simulation is terminated
- **Manual**: Available via "Générer Audio Global" button
- **Content**: All dialogues with TTS titles and transitions

### Download Options
- **Preview**: Built-in audio player
- **Download**: Click "Télécharger Audio Complet" button
- **Filename**: `{simulation_title}_audio_complet.mp3`

## Audio Management

### Playback Controls
- Standard HTML5 audio controls
- Play, pause, seek, volume control
- Progress indicator

### File Organization
- Individual recordings preserved
- Generated audio files cached
- Automatic cleanup of temporary files

## Settings Configuration

### Access Settings
1. **Click** gear icon in simulation run page
2. **Configure** preferences in modal
3. **Save** settings (persisted in browser)

### Available Settings
- **Auto-Record**: Automatic recording/generation trigger
- **Auto-Play**: Automatic playback after generation

## Best Practices

### Recording Quality
- Use quiet environment
- Speak clearly and at normal pace
- Position microphone appropriately
- Test audio levels before starting

### Workflow Optimization
- Enable auto-record for faster practice
- Use auto-play for continuous flow
- Download complete audio for offline review

## Troubleshooting

### Common Issues
- **No microphone access**: Check browser permissions
- **Audio not generating**: Verify internet connection for TTS
- **Download not working**: Check browser download settings

### Browser Compatibility
- Chrome: Full support
- Firefox: Full support
- Safari: Full support
- Edge: Full support

## File Formats
- **Recording**: WebM (browser native)
- **Storage**: MP3 (converted automatically)
- **Download**: MP3 format
# Troubleshooting - Audio Generation

## Common Issues and Solutions

### Recording Issues

#### Microphone Not Working
**Symptoms**: No audio recorded, permission denied errors

**Solutions**:
1. **Check browser permissions**:
   - Chrome: Click lock icon → Allow microphone
   - Firefox: Click shield icon → Allow microphone
   - Safari: Safari menu → Preferences → Websites → Microphone

2. **Verify microphone hardware**:
   - Test in other applications
   - Check system audio settings
   - Ensure microphone is not muted

3. **Browser compatibility**:
   - Use modern browser versions
   - Clear browser cache and cookies
   - Try incognito/private mode

#### Audio Quality Issues
**Symptoms**: Distorted, quiet, or noisy recordings

**Solutions**:
1. **Environment optimization**:
   - Use quiet room
   - Minimize background noise
   - Position microphone 6-12 inches from mouth

2. **System settings**:
   - Adjust microphone gain/volume
   - Disable audio enhancements
   - Check for conflicting applications

### TTS Generation Issues

#### System Audio Not Generating
**Symptoms**: "Écouter" button doesn't produce audio

**Solutions**:
1. **Check internet connection**:
   - TTS requires internet for Google services
   - Verify stable connection
   - Try refreshing the page

2. **Server-side issues**:
   - Check Django logs for errors
   - Verify gTTS library installation
   - Ensure media directory permissions

#### TTS Audio Quality
**Symptoms**: Robotic or unclear system audio

**Solutions**:
1. **Text optimization**:
   - Use proper French punctuation
   - Avoid special characters
   - Break long sentences

2. **Language settings**:
   - Verify `lang='fr'` parameter
   - Check for mixed language content

### Audio Concatenation Issues

#### Dialogue Audio Not Generating
**Symptoms**: Complete dialogue audio fails to create

**Solutions**:
1. **Check prerequisites**:
   - Ensure all lines have recordings
   - Verify file permissions in media directory
   - Check available disk space

2. **Debug steps**:
   ```python
   # In Django shell
   from simulator.models import Dialogue
   dialogue = Dialogue.objects.get(id=YOUR_ID)
   dialogue.generate_complete_audio()
   ```

#### Simulation Audio Issues
**Symptoms**: Final simulation audio not generating

**Solutions**:
1. **Verify dialogue completion**:
   - All dialogues must have complete_audio
   - Check dialogue order sequence
   - Ensure proper file paths

2. **Manual generation**:
   ```python
   # In Django shell
   from simulator.utils import generate_simulation_audio
   from simulator.models import Simulation
   simulation = Simulation.objects.get(id=YOUR_ID)
   generate_simulation_audio(simulation)
   ```

### Download Issues

#### Download Button Not Working
**Symptoms**: Click doesn't trigger download

**Solutions**:
1. **Browser settings**:
   - Check download permissions
   - Verify download location settings
   - Disable popup blockers

2. **File accessibility**:
   - Ensure audio file exists
   - Check media URL configuration
   - Verify Django MEDIA_URL settings

#### Corrupted Downloads
**Symptoms**: Downloaded files won't play

**Solutions**:
1. **File integrity**:
   - Re-generate audio
   - Check source file validity
   - Try different browser

2. **Format compatibility**:
   - Ensure MP3 codec support
   - Try different media player
   - Check file extension

### Performance Issues

#### Slow Audio Generation
**Symptoms**: Long delays in TTS or concatenation

**Solutions**:
1. **Server optimization**:
   - Check server resources (CPU, memory)
   - Optimize media file storage
   - Consider caching strategies

2. **Network optimization**:
   - Use CDN for media files
   - Compress audio files
   - Implement progressive loading

#### Browser Memory Issues
**Symptoms**: Page crashes during recording

**Solutions**:
1. **Memory management**:
   - Close unnecessary tabs
   - Restart browser
   - Clear browser cache

2. **Recording optimization**:
   - Limit recording duration
   - Process recordings immediately
   - Avoid multiple simultaneous recordings

## Debugging Tools

### Browser Developer Tools
1. **Console**: Check for JavaScript errors
2. **Network**: Monitor API requests/responses
3. **Application**: Inspect localStorage settings

### Django Debug
```python
# Enable debug logging in settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'audio_debug.log',
        },
    },
    'loggers': {
        'simulator.utils': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    },
}
```

### Audio File Validation
```python
# Check audio file integrity
from pydub import AudioSegment

def validate_audio_file(file_path):
    try:
        audio = AudioSegment.from_file(file_path)
        print(f"Duration: {len(audio)}ms")
        print(f"Channels: {audio.channels}")
        print(f"Sample Rate: {audio.frame_rate}")
        return True
    except Exception as e:
        print(f"Invalid audio file: {e}")
        return False
```

## Getting Help

### Log Files
- Check Django application logs
- Browser console errors
- Network request failures

### System Requirements
- Modern browser with MediaRecorder API support
- Stable internet connection for TTS
- Sufficient disk space for audio files

### Contact Information
- Check project documentation
- Review GitHub issues
- Contact system administrator
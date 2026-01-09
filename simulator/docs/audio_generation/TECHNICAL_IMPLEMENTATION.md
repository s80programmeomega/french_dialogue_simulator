# Technical Implementation - Audio Generation

## Core Functions

### Text-to-Speech Generation
```python
def text_to_speech(text: str, output_path: str = ".", lang: str = "fr") -> str
```
- **Purpose**: Converts text to speech using Google TTS
- **Parameters**: Text content, output file path, language code
- **Returns**: Path to generated audio file
- **Usage**: System participant audio generation

### Dialogue Audio Concatenation
```python
def concatenate_dialogue_audio(dialogue) -> str
```
- **Purpose**: Combines all line recordings into single dialogue audio
- **Process**: 
  1. Retrieves all recorded lines in order
  2. Adds random silence (500-1000ms) between lines
  3. Exports as MP3
- **Returns**: Relative path to dialogue audio file

### Simulation Audio Generation
```python
def generate_simulation_audio(simulation) -> str
```
- **Purpose**: Creates complete simulation audio with TTS titles
- **Process**:
  1. Generates TTS for each dialogue title
  2. Concatenates: Title + 2s pause + Dialogue + 2s pause
  3. Exports final MP3
- **Returns**: Relative path to simulation audio file

## Database Models

### LineRecording
```python
class LineRecording(models.Model):
    dialogue_line = models.OneToOneField(DialogueLine, primary_key=True)
    audio_file = models.FileField(upload_to="simulations/lines/")
    recorded_at = models.DateTimeField(auto_now_add=True)
```

### Dialogue Audio Field
```python
class Dialogue(models.Model):
    complete_audio = models.FileField(upload_to="dialogues/complete/", null=True, blank=True)
    
    def generate_complete_audio(self):
        audio_path = concatenate_dialogue_audio(self)
        if audio_path:
            self.complete_audio = audio_path
            self.save()
            return True
        return False
```

### Simulation Audio Field
```python
class Simulation(models.Model):
    final_audio = models.FileField(upload_to="simulations/final/", null=True, blank=True)
```

## API Endpoints

### Line Recording
- **URL**: `/api/line/<int:line_id>/record/`
- **Method**: POST
- **Purpose**: Save user audio recording
- **Response**: `{"success": true, "audio_url": "..."}`

### System Audio Generation
- **URL**: `/api/line/<int:line_id>/generate/`
- **Method**: GET
- **Purpose**: Generate TTS for system lines
- **Response**: `{"success": true, "audio_url": "..."}`

### Dialogue Audio Generation
- **URL**: `/api/dialogue/<int:dialogue_id>/generate-complete/`
- **Method**: GET
- **Purpose**: Generate complete dialogue audio
- **Response**: `{"success": true, "audio_url": "..."}`

### Simulation Audio Generation
- **URL**: `/api/simulation/<int:pk>/generate-audio/`
- **Method**: GET
- **Purpose**: Generate complete simulation audio
- **Response**: `{"success": true, "audio_url": "..."}`

## Automatic Triggers

### Dialogue Completion
```javascript
// Triggered when all lines in dialogue are recorded
if (recordedLines === totalLines && totalLines > 0) {
    generateCompleteAudio();
}
```

### Simulation Termination
```python
# In views.py - complete_simulation() and next_dialogue()
if not simulation.final_audio:
    audio_path = generate_simulation_audio(simulation)
    if audio_path:
        simulation.final_audio = audio_path
```

## File Management

### Storage Paths
- Line recordings: `media/simulations/lines/system_{line_id}.mp3`
- Dialogue audio: `media/dialogues/complete/dialogue_{dialogue_id}.mp3`
- Simulation audio: `media/simulations/final/simulation_{simulation_id}.mp3`

### Cleanup
- Temporary TTS files are automatically deleted
- Original recordings are preserved
- Generated audio files persist until manual deletion

## Dependencies
```python
# requirements.txt
gtts==2.3.2          # Google Text-to-Speech
pydub==0.25.1        # Audio processing
pyaudio==0.2.11      # Audio recording (optional)
```
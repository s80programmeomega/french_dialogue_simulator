# API Reference - Audio Generation

## Endpoints Overview

### Line Recording API
**POST** `/api/line/<int:line_id>/record/`

**Purpose**: Save user audio recording for a dialogue line

**Parameters**:
- `line_id` (int): ID of the dialogue line
- `audio_data` (string): Base64 encoded audio data

**Request Format**:
```javascript
const formData = new FormData();
formData.append('audio_data', base64Audio);

fetch(`/api/line/${lineId}/record/`, {
    method: 'POST',
    body: formData
});
```

**Response**:
```json
{
    "success": true,
    "audio_url": "/media/simulations/lines/line_123.webm"
}
```

**Error Response**:
```json
{
    "success": false,
    "error": "No audio data"
}
```

---

### System Audio Generation API
**GET** `/api/line/<int:line_id>/generate/`

**Purpose**: Generate TTS audio for system participant lines

**Parameters**:
- `line_id` (int): ID of the dialogue line

**Response**:
```json
{
    "success": true,
    "audio_url": "/media/simulations/lines/system_123.mp3"
}
```

**Error Response**:
```json
{
    "success": false,
    "error": "Not a system line"
}
```

---

### Complete Dialogue Audio API
**GET** `/api/dialogue/<int:dialogue_id>/generate-complete/`

**Purpose**: Generate complete dialogue audio by concatenating all line recordings

**Parameters**:
- `dialogue_id` (int): ID of the dialogue

**Response**:
```json
{
    "success": true,
    "audio_url": "/media/dialogues/complete/dialogue_123.mp3"
}
```

**Error Response**:
```json
{
    "success": false,
    "error": "No recordings found"
}
```

---

### Simulation Audio Generation API
**GET** `/api/simulation/<int:pk>/generate-audio/`

**Purpose**: Generate complete simulation audio with TTS titles and transitions

**Parameters**:
- `pk` (int): ID of the simulation

**Response**:
```json
{
    "success": true,
    "audio_url": "/media/simulations/final/simulation_123.mp3"
}
```

**Error Response**:
```json
{
    "success": false,
    "error": "No dialogue audios found"
}
```

## JavaScript Integration

### Recording Implementation
```javascript
// Start recording
const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
const mediaRecorder = new MediaRecorder(stream);
const audioChunks = [];

mediaRecorder.ondataavailable = (event) => {
    audioChunks.push(event.data);
};

mediaRecorder.onstop = async () => {
    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
    await saveRecording(lineId, audioBlob);
};

mediaRecorder.start();
```

### Save Recording Function
```javascript
async function saveRecording(lineId, audioBlob) {
    const reader = new FileReader();
    reader.readAsDataURL(audioBlob);
    reader.onloadend = async () => {
        const base64Audio = reader.result;
        const formData = new FormData();
        formData.append('audio_data', base64Audio);

        const response = await fetch(`/api/line/${lineId}/record/`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (data.success) {
            // Update UI with audio player
            updateAudioPlayer(lineId, data.audio_url);
        }
    };
}
```

### Generate System Audio
```javascript
async function generateSystemAudio(lineId) {
    const response = await fetch(`/api/line/${lineId}/generate/`);
    const data = await response.json();
    
    if (data.success) {
        updateAudioPlayer(lineId, data.audio_url);
        if (settings.autoPlay) {
            playAudio(lineId);
        }
    }
}
```

## Response Codes

### Success Responses
- `200 OK`: Request successful
- `201 Created`: Resource created successfully

### Error Responses
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Resource not found
- `405 Method Not Allowed`: Invalid HTTP method
- `500 Internal Server Error`: Server processing error

## Rate Limiting
- No explicit rate limiting implemented
- Browser-based recording limits apply
- TTS service limits may apply for high volume usage

## File Upload Limits
- Maximum audio file size: Determined by Django settings
- Supported formats: WebM (input), MP3 (output)
- Audio quality: Browser default settings

## CSRF Protection
- Line recording endpoint uses `@csrf_exempt` decorator
- Other endpoints follow Django CSRF protection
- Include CSRF token in forms when required
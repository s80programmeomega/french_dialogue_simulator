# 🎭 French Dialogue Simulator

> An interactive web application for practicing French conversations through simulated dialogues with real-time audio recording and text-to-speech capabilities.

[![Django](https://img.shields.io/badge/Django-5.2.9-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.2-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📖 Description

**French Dialogue Simulator** is an educational platform designed to help learners practice French conversations in a structured, interactive environment. The application simulates real-world dialogue scenarios where users can:

- **Practice speaking** by recording their voice for assigned dialogue lines
- **Listen to native pronunciation** through automated text-to-speech for system participants
- **Track progress** through multiple dialogue sequences within simulations
- **Create custom scenarios** with flexible participant roles and conversation flows

Perfect for language learners, teachers, and anyone looking to improve their French conversational skills through immersive practice.

---

## ✨ Key Features

### 🎯 Core Functionality

- **Multi-participant dialogues**: Support for 2+ speakers in conversations
- **Turn-based recording**: Sequential audio recording following dialogue order
- **Automated TTS**: System participants automatically generate French speech using Google Text-to-Speech
- **Real-time audio playback**: Instant playback of recorded and generated audio
- **Progress tracking**: Visual indicators showing completion status

### 🛠️ Management Tools

- **Simulation builder**: Create and organize multiple dialogues into learning sessions
- **Participant management**: Define reusable characters (user or system-controlled)
- **Dialogue editor**: Build conversations line-by-line with drag-and-drop simplicity
- **Inline creation**: Add participants directly while editing dialogues
- **Difficulty levels**: Categorize dialogues as beginner, intermediate, or advanced

### 🎨 User Interface

- **Modern Bootstrap 5 design**: Clean, responsive interface
- **Sidebar navigation**: Quick access to all features
- **Dashboard analytics**: Overview of simulations, dialogues, and progress
- **Font Awesome icons**: Intuitive visual indicators throughout

---

## 🏗️ Architecture

### Database Schema

```
User (CustomUser)
  ↓ (1:N)
Participant ←──────┐
  ↓ (M:N)          │
Dialogue           │
  ↓ (1:N)          │
DialogueLine ──────┘
  ↓ (1:1)
LineRecording

Simulation
  ↓ (1:N)
Dialogue
```

**Key Relationships:**

- One user can create many participants
- Dialogues can have multiple participants (many-to-many)
- Each dialogue line belongs to one participant
- Each line has one audio recording (user or system-generated)
- Simulations contain multiple dialogues in sequence

### Technology Stack

**Backend:**

- Django 5.2.9 - Web framework
- SQLite - Database (development)
- gTTS - Google Text-to-Speech for French audio generation
- PyAudio - Audio recording utilities
- Pydub - Audio file manipulation

**Frontend:**

- Bootstrap 5.3.2 - UI framework
- Font Awesome 5 - Icon library
- MediaRecorder API - Browser-based audio recording
- Vanilla JavaScript - Client-side interactivity

**Development Tools:**

- django-watchfiles - Auto-reload during development
- django-browser-reload - Live browser refresh
- django-cleanup - Automatic file cleanup
- django-extensions - Enhanced management commands and utilities

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Modern web browser with microphone access

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/french-dialogue-simulator.git
cd french-dialogue-simulator
```

1. **Create virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

1. **Configure database**

```bash
python manage.py makemigrations
python manage.py migrate
```

1. **Create superuser (optional)**

```bash
python manage.py createsuperuser
```

1. **Load sample data**

```bash
python manage.py create_sample_data
# Or
python manage.py seed_dialogues
```

1. **Run development server**

```bash
python manage.py runserver
```

1. **Access the application**

```
Open browser: http://localhost:8000
Admin panel: http://localhost:8000/admin
```

---

## 📚 Usage Guide

### Creating Your First Simulation

1. **Create Participants**
   - Navigate to "Participants" in sidebar
   - Click "Nouveau Participant"
   - Enter character name (e.g., "Marie", "Serveur")
   - Check "Système" for automated TTS voices
   - Save

2. **Create Simulation**
   - Go to "Simulations" → "Nouvelle Simulation"
   - Enter simulation title (e.g., "Au Restaurant")
   - Save

3. **Add Dialogue**
   - Open your simulation
   - Click "Ajouter" under Dialogues
   - Fill in title, description, and difficulty level
   - Save

4. **Build Conversation**
   - Click "Éditer" on your dialogue
   - Add participants (existing or create new)
   - Add dialogue lines one by one
   - Assign each line to a participant
   - Lines are automatically ordered

5. **Run Simulation**
   - Click "Démarrer" on simulation detail page
   - For system lines: Click "Écouter" to generate/play TTS
   - For user lines: Click "Enregistrer" to record your voice
   - Complete all lines to finish

### Recording Audio

**Browser Permissions:**

- First recording will prompt for microphone access
- Grant permission to enable recording features

**Recording Process:**

1. Click "Enregistrer" button (red microphone icon)
2. Speak your line clearly
3. Click "Arrêter" when finished
4. Audio automatically saves and displays player
5. Re-record anytime by clicking "Enregistrer" again

---

## 📁 Project Structure

```
french_dialogue_simulator/
├── core/                      # Django project settings
│   ├── settings.py           # Configuration
│   ├── urls.py               # Root URL routing
│   └── wsgi.py               # WSGI entry point
├── simulator/                 # Main application
│   ├── management/
│   │   └── commands/
│   │       └── create_sample_data.py  # Sample data generator
│   ├── migrations/           # Database migrations
│   ├── templates/
│   │   └── simulator/        # HTML templates
│   │       ├── base.html     # Base template with sidebar
│   │       ├── home.html     # Dashboard
│   │       ├── simulation_*.html
│   │       ├── dialogue_*.html
│   │       └── participant_*.html
│   ├── admin.py              # Django admin configuration
│   ├── models.py             # Database models
│   ├── urls.py               # App URL routing
│   ├── utils.py              # Audio utilities (TTS, recording)
│   └── views.py              # View controllers
├── users/                     # Custom user authentication
│   └── models.py             # CustomUser model
├── media/                     # User-uploaded files (audio)
├── db.sqlite3                # SQLite database
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## 🎓 Educational Concepts

### Language Learning Principles

**Immersive Practice:**
The simulator follows the **communicative approach** to language learning, emphasizing real-world conversation practice over rote memorization.

**Scaffolded Learning:**

- **Beginner**: Simple greetings, basic requests
- **Intermediate**: Longer exchanges, varied vocabulary
- **Advanced**: Complex scenarios, idiomatic expressions

**Immediate Feedback:**
Learners can compare their pronunciation with system-generated TTS, enabling self-correction and improvement.

### Technical Learning Concepts

**Django MVT Pattern:**

- **Models**: Data structure (Participant, Dialogue, etc.)
- **Views**: Business logic (recording, TTS generation)
- **Templates**: User interface (Bootstrap 5 components)

**RESTful API Design:**

- `/api/line/<id>/record/` - POST audio data
- `/api/line/<id>/generate/` - GET TTS audio

**Browser APIs:**

- **MediaRecorder**: Capture audio from microphone
- **Fetch API**: Asynchronous server communication
- **Audio Element**: Playback controls

---

## 🔧 Configuration

### Audio Settings

**Text-to-Speech (gTTS):**

```python
# simulator/utils.py
text_to_speech(text, output_path, lang='fr')
```

- Language: French (`fr`)
- Speed: Normal (not slow)
- Format: MP3

**Recording Format:**

- Browser: WebM (MediaRecorder default)
- Server storage: As uploaded
- Playback: Native HTML5 audio

### Media Files

```python
# core/settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

Audio files stored in:

- User recordings: `media/simulations/lines/line_<id>.webm`
- System TTS: `media/simulations/lines/system_<id>.mp3`
- Final merged: `media/simulations/final/` (future feature)

---

## 🛣️ Roadmap

### Planned Features

- [ ] **Audio merging**: Combine all line recordings into single dialogue audio
- [ ] **Speech recognition**: Automatic transcription and pronunciation scoring
- [ ] **Vocabulary hints**: Inline translations and definitions
- [ ] **Social features**: Share dialogues with other learners
- [ ] **Mobile app**: Native iOS/Android applications
- [ ] **Multiple languages**: Extend beyond French
- [ ] **AI-generated dialogues**: Use LLMs to create scenarios
- [ ] **Progress analytics**: Detailed learning statistics

### Known Limitations

- Browser compatibility: Requires modern browser with MediaRecorder API
- Audio format: WebM may not play on all devices
- Single user: No multi-user collaboration yet
- No authentication required: Add login system for production

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

**Code Style:**

- Follow PEP 8 for Python
- Use meaningful variable names
- Add docstrings to functions
- Comment complex logic

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Jonas Levis**

- GitHub: [@s80programmeomega](https://github.com/s80programmeomega)
- Email: <jonasinfo2016@gmail.com>

---

## 🙏 Acknowledgments

- **Django Community** - Excellent web framework
- **Bootstrap Team** - Beautiful UI components
- **Google TTS** - Free text-to-speech service
- **Font Awesome** - Comprehensive icon library
- **French Language Learners** - Inspiration for this project

---
#

**Made with ❤️ for French language learners worldwide**

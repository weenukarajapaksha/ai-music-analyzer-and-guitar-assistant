# 🎵 AI Music Analyzer & Guitar Assistant

An intelligent web-based music analysis and guitar assistant platform built with Flask and Python.  
This system allows users to upload songs, analyze musical features, detect chords, generate chord sheets, transpose songs, and compose their own guitar parts interactively.

---

# 🚀 Live Demo

Add your deployed Render link here:

https://ai-music-analyzer-and-guitar-assistant-1.onrender.com

---

# 📌 Project Overview

AI Music Analyzer & Guitar Assistant is designed to help musicians, guitar learners, and music enthusiasts understand songs more easily.

The system can analyze uploaded MP3/WAV audio files and extract useful musical information such as:

- BPM / tempo
- Key signature
- Time signature
- Chord progression
- Chord timeline
- Mood / energy level

It also provides guitar-focused features such as chord sheets, transposition, guitar chord diagrams, piano note visualization, and an interactive guitar part composer.

---

# ✨ Features

## 🎼 Audio Analysis

- Upload MP3 or WAV audio files
- Detect BPM / tempo
- Detect key signature with Major / Minor estimation
- Estimate time signature
- Detect chords from the song
- Display chord changes with timestamps
- Analyze mood / energy level

---

## 🎸 Guitar Assistant

- View detected chords
- Click chords to see piano notes
- View guitar chord shapes
- Display visual guitar chord diagrams
- Beginner-friendly chord suggestions
- Suggested strumming patterns
- Practice BPM recommendation

---

## 📄 Chord Sheet Generator

- Generate chord sheets automatically from detected chords
- Display chord sheet in bar format
- Format chords as 4 bars per line
- Show song name, key signature, time signature, and BPM
- Export chord sheet as a PDF

Example chord sheet format:

```text
| C   _   G   _   | E   _   F   _   | G   _   _   F   | C   _   C   _   |
| C   _   _   _   | E   _   _   _   | G   G   _   F   | C   _   C   _   |
```

---

## 🔁 Transpose Functionality

- Transpose chord sheet to any selected key
- Increase key by one semitone
- Decrease key by one semitone
- Download PDF chord sheet in the transposed key

---

## 🎹 Compose Your Own Guitar Part

Users can create their own guitar part by selecting:

- Key signature
- Time signature
- Tempo
- Number of bars

The composer allows users to:

- Generate empty beat slots
- Select notes from the chosen key
- Fill note slots interactively
- Automatically suggest chords
- Play the created guitar part

---

## 💾 Analysis History

- Save analyzed song information using SQLite
- Store filename, BPM, key, time signature, mood, and chords
- View previous song analyses

---

# 🛠️ Technologies Used

## Backend

- Python
- Flask
- SQLite

## Audio Processing

- Librosa
- NumPy
- SciPy
- SoundFile
- Audioread

## PDF Generation

- ReportLab

## Frontend

- HTML5
- CSS3
- JavaScript

## Deployment

- Render
- Gunicorn

---

# 📂 Project Structure

```text
AI-Music-Analyzer/
│
├── app.py
├── requirements.txt
├── Procfile
├── .gitignore
│
├── uploads/
│   └── .gitkeep
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── images/
│   │
│   ├── sounds/
│   │
│   └── waveforms/
│       └── .gitkeep
│
└── templates/
    ├── index.html
    ├── chords.html
    ├── chord_sheet.html
    ├── composer.html
    ├── guitar_assistant.html
    └── history.html
```

---

# ⚙️ Installation and Setup

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate virtual environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the Application

```bash
python app.py
```

Open in browser:

```text
http://127.0.0.1:5000
```

---

# ☁️ Deployment on Render

This project can be deployed on Render using Gunicorn.

## Procfile

```text
web: gunicorn app:app --timeout 180
```

## Build Command

```bash
pip install -r requirements.txt
```

## Start Command

```bash
gunicorn app:app --timeout 180
```

---

# 📦 Requirements

Example `requirements.txt`:

```text
Flask
gunicorn
librosa
numpy
matplotlib
soundfile
audioread
reportlab
scipy
```

---

# ⚠️ Deployment Notes

For cloud deployment, audio processing may require memory optimization.

Recommended `librosa.load()` setting for limited hosting environments:

```python
y, sr = librosa.load(file_path, sr=22050, duration=60, mono=True)
```

If using Render free tier, long audio files may take more time to process.

---

# 📸 Screenshots

Add screenshots of your project here.

Example:

```markdown
![Home Page](static/images/homepage.png)
![Chord Sheet](static/images/chord-sheet.png)
![Guitar Assistant](static/images/guitar-assistant.png)
```

---

# 🔮 Future Improvements

- Real guitar sample playback
- Drag-and-drop composer
- MIDI export
- Advanced chord recognition
- Better chord correction using key-family theory
- User accounts
- Cloud database storage
- Mobile-friendly version
- Real-time microphone input analysis
- AI-based practice recommendations

---

# 👨‍💻 Author

Developed by **Weenuka Rajapaksha**

Department of Computer Science and Engineering  
University of Moratuwa

---

# 🎯 Project Goal

The goal of this project is to combine:

- Audio signal processing
- Music information retrieval
- Guitar learning assistance
- Interactive music composition
- Web application development

into one intelligent music platform for learners and musicians.

---

# ⭐ If you like this project

Consider giving the repository a star on GitHub.

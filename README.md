🎵 AI Music Analyzer & Guitar Assistant

An intelligent web-based music analysis platform built with Flask and Python that allows users to upload songs, analyze musical properties, generate chord sheets, transpose keys, and compose their own guitar parts interactively.

🚀 Features
🎼 Music Analysis
Upload MP3/WAV audio files
Automatic BPM / tempo detection
Key signature detection (Major / Minor)
Time signature estimation
Chord progression detection
Chord timeline visualization
🎸 Guitar Assistant
Interactive chord viewer
Piano key visualization
Guitar chord diagrams
Chord popup interface
Guitar fingering suggestions
📄 Chord Sheet Generator
Automatically generate structured chord sheets
4-bars-per-line formatting
Song title, key signature, BPM, and time signature
Export chord sheets as professional PDF files
🔁 Transpose System
Transpose chord sheets to any key
/ - semitone transpose buttons
Real-time chord updates
🎹 Guitar Part Composer
Select:
Key signature
Tempo
Time signature
Number of bars
Create custom guitar melodies
Auto chord suggestions based on notes
Real-time playback
Interactive note placement system
💾 Analysis History
SQLite database storage
Save analyzed songs and metadata
View previous analysis history
🌐 Modern Web Interface
Professional dark music-tech UI
Responsive design
Navigation bar
Animated sections
Interactive popups and cards
🛠️ Technologies Used
Backend
Python
Flask
SQLite
Audio Processing
Librosa
NumPy
SciPy
SoundFile
PDF Generation
ReportLab
Frontend
HTML5
CSS3
JavaScript
📂 Project Structure
AI-Music-Analyzer/
│
├── app.py
├── requirements.txt
├── Procfile
├── .gitignore
│
├── uploads/
│
├── static/
│   ├── css/
│   ├── images/
│   ├── sounds/
│   └── waveforms/
│
├── templates/
│   ├── index.html
│   ├── chords.html
│   ├── chord_sheet.html
│   ├── composer.html
│   └── history.html
⚙️ Installation
Clone Repository
git clone YOUR_REPOSITORY_LINK
cd AI-Music-Analyzer
Install Dependencies
pip install -r requirements.txt
Run Application
python app.py

Open browser:

http://127.0.0.1:5000
☁️ Deployment

This project is deployment-ready for:

Render
Railway
PythonAnywhere

Production server:

gunicorn app:app
📸 Main Modules
🎵 Song Analyzer

Analyze uploaded songs for:

tempo
chords
key
time signature
🎸 Guitar Assistant

Visualize:

piano notes
guitar chord diagrams
📄 Chord Sheet Generator

Generate:

structured chord sheets
downloadable PDFs
🎹 Composer

Create custom guitar parts interactively.

🔮 Future Improvements
Real guitar sample playback
MIDI export
AI chord correction
Drag-and-drop composition
Waveform editor
User accounts & cloud storage
Real-time chord recognition
Mobile app version
👨‍💻 Author

Developed by Weenuka Rajapaksha
Department of Computer Science & Engineering
University of Moratuwa

⭐ Project Goal

This project aims to combine:

Music Information Retrieval (MIR)
Machine Learning
Audio Signal Processing
Interactive Music Education
Guitar Assistance Tools

into a single intelligent music platform.

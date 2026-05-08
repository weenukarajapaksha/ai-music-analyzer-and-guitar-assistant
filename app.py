from flask import Flask, render_template, request, send_from_directory
import os
from datetime import datetime
import librosa
import numpy as np
from flask import make_response
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO

latest_audio_info = None

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"mp3", "wav"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

latest_chords = []
latest_filename = None

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def create_chord_templates():
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F',
             'F#', 'G', 'G#', 'A', 'A#', 'B']

    templates = {}

    for i, note in enumerate(notes):
        # Major chord: root, major third, perfect fifth
        major = np.zeros(12)
        major[i] = 1
        major[(i + 4) % 12] = 1
        major[(i + 7) % 12] = 1
        templates[note] = major

        # Minor chord: root, minor third, perfect fifth
        minor = np.zeros(12)
        minor[i] = 1
        minor[(i + 3) % 12] = 1
        minor[(i + 7) % 12] = 1
        templates[note + "m"] = minor

    return templates

def generate_chord_sheet(chords, bpm, time_signature, total_seconds=None):
    if not chords or not bpm:
        return []

    if time_signature == "3/4":
        beats_per_bar = 3
    elif time_signature == "6/8":
        beats_per_bar = 6
    else:
        beats_per_bar = 4

    seconds_per_beat = 60 / bpm

    chord_positions = []

    for time, chord in chords:
        beat_position = int(round(time / seconds_per_beat))
        chord_positions.append((beat_position, chord))

    if total_seconds:
        total_beats = int(total_seconds / seconds_per_beat)
    else:
        total_beats = chord_positions[-1][0] + beats_per_bar * 4

    total_bars = int(total_beats / beats_per_bar) + 1

    bars = []
    chord_index = 0
    current_chord = chord_positions[0][1]

    for bar_number in range(total_bars):
        bar = []

        for beat in range(beats_per_bar):
            current_beat = bar_number * beats_per_bar + beat

            while (
                chord_index + 1 < len(chord_positions)
                and chord_positions[chord_index + 1][0] <= current_beat
            ):
                chord_index += 1
                current_chord = chord_positions[chord_index][1]

            exact_change = (
                chord_index < len(chord_positions)
                and chord_positions[chord_index][0] == current_beat
            )

            if beat == 0:
                bar.append(current_chord)
            elif exact_change:
                bar.append(current_chord)
            else:
                bar.append("_")

        bars.append(bar)

    return bars

def get_family_chords(key):
    major_keys = {
        "C Major":  ["C", "Dm", "Em", "F", "G", "Am", "Bdim"],
        "C# Major": ["C#", "D#m", "Fm", "F#", "G#", "A#m", "Cdim"],
        "D Major":  ["D", "Em", "F#m", "G", "A", "Bm", "C#dim"],
        "D# Major": ["D#", "Fm", "Gm", "G#", "A#", "Cm", "Ddim"],
        "E Major":  ["E", "F#m", "G#m", "A", "B", "C#m", "D#dim"],
        "F Major":  ["F", "Gm", "Am", "A#", "C", "Dm", "Edim"],
        "F# Major": ["F#", "G#m", "A#m", "B", "C#", "D#m", "Fdim"],
        "G Major":  ["G", "Am", "Bm", "C", "D", "Em", "F#dim"],
        "G# Major": ["G#", "A#m", "Cm", "C#", "D#", "Fm", "Gdim"],
        "A Major":  ["A", "Bm", "C#m", "D", "E", "F#m", "G#dim"],
        "A# Major": ["A#", "Cm", "Dm", "D#", "F", "Gm", "Adim"],
        "B Major":  ["B", "C#m", "D#m", "E", "F#", "G#m", "A#dim"],
    }

    minor_keys = {
        "A Minor":  ["Am", "Bdim", "C", "Dm", "Em", "F", "G"],
        "A# Minor": ["A#m", "Cdim", "C#", "D#m", "Fm", "F#", "G#"],
        "B Minor":  ["Bm", "C#dim", "D", "Em", "F#m", "G", "A"],
        "C Minor":  ["Cm", "Ddim", "D#", "Fm", "Gm", "G#", "A#"],
        "C# Minor": ["C#m", "D#dim", "E", "F#m", "G#m", "A", "B"],
        "D Minor":  ["Dm", "Edim", "F", "Gm", "Am", "A#", "C"],
        "D# Minor": ["D#m", "Fdim", "F#", "G#m", "A#m", "B", "C#"],
        "E Minor":  ["Em", "F#dim", "G", "Am", "Bm", "C", "D"],
        "F Minor":  ["Fm", "Gdim", "G#", "A#m", "Cm", "C#", "D#"],
        "F# Minor": ["F#m", "G#dim", "A", "Bm", "C#m", "D", "E"],
        "G Minor":  ["Gm", "Adim", "A#", "Cm", "Dm", "D#", "F"],
        "G# Minor": ["G#m", "A#dim", "B", "C#m", "D#m", "E", "F#"],
    }

    if key in major_keys:
        return major_keys[key]

    if key in minor_keys:
        return minor_keys[key]

    return []


def detect_chords(y, sr, key):
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)

    chord_templates = create_chord_templates()
    family_chords = get_family_chords(key)
    detected_chords = []

    hop_length = 512  # default

    for i in range(chroma.shape[1]):
        frame = chroma[:, i]

        best_chord = None
        best_score = -1

        for chord, template in chord_templates.items():
            score = np.dot(frame, template)

            # Boost family chords of the detected key
            if chord in family_chords:
                score *= 1.25
            else:
                score *= 0.85

            if score > best_score:
                best_score = score
                best_chord = chord

        # 🎯 Convert frame index → time (seconds)
        time = librosa.frames_to_time(i, sr=sr, hop_length=hop_length)

        detected_chords.append((round(time, 2), best_chord))

    # Remove duplicates (keep changes only)
    simplified = []
    last_chord = None

    for t, chord in detected_chords:
        if chord != last_chord:
            simplified.append((t, chord))
            last_chord = chord

    return simplified

def detect_key(y, sr):
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_avg = np.mean(chroma, axis=1)

    notes = ['C', 'C#', 'D', 'D#', 'E', 'F',
             'F#', 'G', 'G#', 'A', 'A#', 'B']

    # Krumhansl-Schmuckler key profiles
    major_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09,
                              2.52, 5.19, 2.39, 3.66, 2.29, 2.88])

    minor_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53,
                              2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

    best_key = None
    best_score = -1

    for i in range(12):
        major_score = np.corrcoef(chroma_avg, np.roll(major_profile, i))[0, 1]
        minor_score = np.corrcoef(chroma_avg, np.roll(minor_profile, i))[0, 1]

        if major_score > best_score:
            best_score = major_score
            best_key = notes[i] + " Major"

        if minor_score > best_score:
            best_score = minor_score
            best_key = notes[i] + " Minor"

    return best_key

def detect_time_signature(y, sr):
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    if len(beat_frames) < 8:
        return "Unknown"

    onset_env = librosa.onset.onset_strength(y=y, sr=sr)

    beat_strengths = onset_env[beat_frames]

    scores = {}

    for meter in [3, 4, 6]:
        grouped_scores = []

        for i in range(0, len(beat_strengths) - meter, meter):
            group = beat_strengths[i:i + meter]

            if len(group) == meter:
                downbeat_strength = group[0]
                other_strengths = np.mean(group[1:])
                score = downbeat_strength - other_strengths
                grouped_scores.append(score)

        if grouped_scores:
            scores[meter] = np.mean(grouped_scores)

    if not scores:
        return "Unknown"

    best_meter = max(scores, key=scores.get)

    if best_meter == 3:
        return "3/4"
    elif best_meter == 6:
        return "6/8"
    else:
        return "4/4"
    
def detect_energy_mood(y, sr):
    rms = librosa.feature.rms(y=y)[0]
    avg_energy = np.mean(rms)

    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    tempo = float(tempo)

    if avg_energy > 0.08 and tempo > 120:
        mood = "High Energy"
    elif avg_energy > 0.04 and tempo > 80:
        mood = "Medium Energy"
    else:
        mood = "Low Energy"

    return mood, round(float(avg_energy), 4)

def analyze_audio(file_path):
    y, sr = librosa.load(file_path, sr=None)

    duration = librosa.get_duration(y=y, sr=sr)

    # 🎯 BPM detection
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    time_signature = detect_time_signature(y, sr)

    # 🎯 Key detection using chroma features
    key = detect_key(y, sr)

    minutes = int(duration // 60)
    seconds = int(duration % 60)

    chords = detect_chords(y, sr, key)

    mood, energy = detect_energy_mood(y, sr)

    audio_info = {
        "sample_rate": sr,
        "duration": f"{minutes} min {seconds} sec",
        "total_seconds": round(duration, 2),
        "tempo": round(float(tempo), 2),
        "beats_detected": len(beat_frames),
        "key": key,
        "chords": chords,
        "time_signature": time_signature,
        "mood": mood,
        "energy": energy
    }

    return audio_info

def generate_guitar_assistant(audio_info, chords):
    if not audio_info:
        return None

    bpm = audio_info["tempo"]
    key = audio_info["key"]
    time_signature = audio_info["time_signature"]

    unique_chords = []
    for item in chords:
        chord = item[1] if isinstance(item, tuple) else item
        if chord not in unique_chords:
            unique_chords.append(chord)

    if time_signature == "3/4":
        strumming = "Down Down Up"
    elif time_signature == "6/8":
        strumming = "Down _ Down Up Down Up"
    else:
        strumming = "Down Down Up Up Down Up"

    practice_bpm = int(bpm * 0.7)

    easy_chords = {
        "F": "Try Fmaj7 or small F shape",
        "Bm": "Try Bm7 or use capo",
        "B": "Try B7",
        "F#m": "Try F#m7 or use capo",
        "C#m": "Try C#m7 or use capo",
        "G#m": "Try G#m7 or use capo",
        "A#m": "Try A#m7 or use capo",
        "D#m": "Try D#m7 or use capo"
    }

    suggestions = []

    for chord in unique_chords:
        if chord in easy_chords:
            suggestions.append(f"{chord}: {easy_chords[chord]}")

    if not suggestions:
        suggestions.append("Most detected chords are beginner-friendly.")

    return {
        "key": key,
        "bpm": bpm,
        "practice_bpm": practice_bpm,
        "time_signature": time_signature,
        "unique_chords": unique_chords,
        "strumming": strumming,
        "suggestions": suggestions
    }

def format_chord_sheet_text(chord_sheet):
    lines = []

    for i in range(0, len(chord_sheet), 4):
        row_bars = chord_sheet[i:i + 4]
        line = ""

        for bar in row_bars:
            line += "| " + " ".join(bar) + " "

        line += "|"
        lines.append(line)

    return lines


@app.route("/", methods=["GET", "POST"])
def index():
    global latest_chords, latest_filename, latest_audio_info
    message = None
    filename = None
    audio_info = None

    if request.method == "POST":
        if "audio_file" not in request.files:
            message = "No file selected."
            return render_template("index.html", message=message)

        file = request.files["audio_file"]

        if file.filename == "":
            message = "No file selected."
            return render_template("index.html", message=message)

        if file and allowed_file(file.filename):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{file.filename}"

            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            audio_info = analyze_audio(file_path)

            latest_chords = audio_info["chords"]
            latest_filename = filename
            latest_audio_info = audio_info

            message = "Audio file uploaded and analyzed successfully!"
        else:
            message = "Only MP3 and WAV files are allowed."

    return render_template(
        "index.html",
        message=message,
        filename=filename,
        audio_info=audio_info
    )


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/chords")
def chords_page():
    print("Latest chords:", latest_chords)  # debug line

    return render_template(
        "chords.html",
        chords=latest_chords,
        filename=latest_filename
    )

@app.route("/chord-sheet")
def chord_sheet_page():
    if not latest_audio_info:
        return render_template(
            "chord_sheet.html",
            chord_sheet=[],
            filename=None,
            time_signature=None
        )

    chord_sheet = generate_chord_sheet(
        latest_chords,
        latest_audio_info["tempo"],
        latest_audio_info["time_signature"],
        latest_audio_info["total_seconds"]
    )

    return render_template(
        "chord_sheet.html",
        chord_sheet=chord_sheet,
        filename=latest_filename,
        time_signature=latest_audio_info["time_signature"]
    )

@app.route("/guitar-assistant")
def guitar_assistant_page():
    assistant_data = generate_guitar_assistant(
        latest_audio_info,
        latest_chords
    )

    return render_template(
        "guitar_assistant.html",
        assistant_data=assistant_data,
        filename=latest_filename
    )

@app.route("/download-chord-sheet")
def download_chord_sheet():
    if not latest_audio_info:
        return "No chord sheet available."

    chord_sheet = generate_chord_sheet(
        latest_chords,
        latest_audio_info["tempo"],
        latest_audio_info["time_signature"],
        latest_audio_info["total_seconds"]
    )

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 60

    song_name = latest_filename if latest_filename else "Unknown Song"

    # Title
    pdf.setFont("Helvetica-Bold", 22)
    title = "Chord Sheet"
    title_width = pdf.stringWidth(title, "Helvetica-Bold", 22)
    pdf.drawString((width - title_width) / 2, y, title)
    y -= 35

    # Song details
    pdf.setFont("Helvetica-Bold", 13)
    song_width = pdf.stringWidth(song_name, "Helvetica-Bold", 13)
    pdf.drawString((width - song_width) / 2, y, song_name)
    y -= 25

    pdf.setFont("Helvetica", 11)
    details = f"Key: {latest_audio_info['key']}    |    Time Signature: {latest_audio_info['time_signature']}    |    BPM: {latest_audio_info['tempo']}"
    details_width = pdf.stringWidth(details, "Helvetica", 11)
    pdf.drawString((width - details_width) / 2, y, details)
    y -= 40

    # Chord sheet settings
    pdf.setFont("Courier-Bold", 13)

    bars_per_line = 4
    lines_per_section = 2
    section_names = ["Verse", "Chorus", "Verse 2", "Bridge", "Final Chorus"]

    line_count = 0
    section_index = 0

    for i in range(0, len(chord_sheet), bars_per_line):
        # New page check
        if y < 80:
            pdf.showPage()
            y = height - 60
            pdf.setFont("Courier-Bold", 13)

        # Section heading every 8 bars
        if line_count % lines_per_section == 0:
            pdf.setFont("Helvetica-Bold", 12)

            if section_index < len(section_names):
                section_title = section_names[section_index]
            else:
                section_title = f"Section {section_index + 1}"

            pdf.drawString(50, y, section_title)
            y -= 22
            section_index += 1

            pdf.setFont("Courier-Bold", 13)

        row = chord_sheet[i:i + bars_per_line]

        line = ""
        for bar in row:
            formatted_bar = "| " + " ".join(f"{c:<3}" for c in bar) + " "
            line += formatted_bar
        line += "|"

        line_width = pdf.stringWidth(line, "Courier-Bold", 13)
        pdf.drawString((width - line_width) / 2, y, line)

        y -= 24
        line_count += 1

        # Extra space after section
        if line_count % lines_per_section == 0:
            y -= 18

    # Footer
    pdf.setFont("Helvetica-Oblique", 9)
    footer = "Generated by AI Music Analyzer"
    footer_width = pdf.stringWidth(footer, "Helvetica-Oblique", 9)
    pdf.drawString((width - footer_width) / 2, 35, footer)

    pdf.save()

    buffer.seek(0)

    response = make_response(buffer.getvalue())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=chord_sheet.pdf"

    return response


if __name__ == "__main__":
    app.run(debug=True)
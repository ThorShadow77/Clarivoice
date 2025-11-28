"""
This module handles audio transcription using Vosk and manages transcript storage in SQLite.
"""
import os
from flask import Flask, request, jsonify, render_template
from transcriber import transcribe_audio
from database import init_db, save_transcript, get_transcripts_from_db

# --- Setup paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
MODEL_PATH = os.path.join(BASE_DIR, "vosk-model-en-us-0.22-lgraph")
DB_PATH = os.path.join(BASE_DIR, "..", "clarivoice.db")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# --- Ensure upload folder exists ---
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Initialise Flask app ---
# Add explicit template and static folders here
app = Flask(
    __name__,
    template_folder=TEMPLATES_DIR,
    static_folder=STATIC_DIR
)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Initialise database ---
init_db(DB_PATH)

# Homepage route
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# Upload route with error handling
@app.route("/upload", methods=["POST"])
def upload_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
    audio_file.save(file_path)
    print(f" Saved file: {file_path}")

    try:
        transcript = transcribe_audio(file_path, MODEL_PATH)
        print(f" Transcript output: {transcript}")

        # Fallback if empty or failed
        if not transcript or not transcript.strip():
            return jsonify({
                "transcript": "Transcription failed, please try again with a clear audio file."
            }), 200

        save_transcript(transcript, DB_PATH)
        return jsonify({"transcript": transcript})

    except Exception as e:
        print(f" Error during transcription: {e}")
        return jsonify({
            "transcript": "Transcription failed, please try again.",
            "error": str(e)
        }), 500

@app.route('/my_meetings')
def my_meetings():
    return render_template('my_meetings.html')

@app.route('/shared')
def shared():
    return render_template('shared.html')

@app.route('/tasks')
def tasks():
    return render_template('tasks.html')

@app.route('/bookmarks')
def bookmarks():
    return render_template('bookmarks.html')

@app.route('/automations')
def automations():
    return render_template('automations.html')

@app.route('/user_oriented')
def user_oriented():
    """Renders the User Oriented workspace page."""
    return render_template('user_oriented.html')


@app.route('/print')
def print_page():
    """Renders the Print workspace page."""
    return render_template('print.html')


@app.route('/view')
def view_page():
    """Renders the View workspace page showing stored transcripts."""
    transcripts = get_transcripts_from_db(DB_PATH)
    return render_template('view.html', transcripts=transcripts)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

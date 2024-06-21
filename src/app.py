from datetime import timedelta
import os
import subprocess
import json
import shutil
from flask import Flask, request, redirect, url_for, render_template, flash, send_from_directory, session, jsonify
from flask_jwt_extended import JWTManager, jwt_required
from dotenv import load_dotenv
from auth.auth import auth_bp
from const import script_description
from evaluation.util.api import gpt_consumption, tts_consumption
from util.utils import limpiar_carpetas, combine_model_results, procesar_resultados

load_dotenv()

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = '../video'
app.config['AUDIO_FOLDER'] = '../audio'
app.config['FRAMES_FOLDER'] = '../frames'
app.secret_key = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)

# Register the auth blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/', methods=['GET'])
def root():
    return redirect(url_for('auth.login'))

@app.route('/index', methods=['GET'])
@jwt_required()
def index():
    video_url = session.get('video_url', None)
    results = session.get('results', [])
    audio_url = session.get('audio_url', None)
    return render_template('index.html', video_url=video_url, results=results, audio_url=audio_url)

@app.route('/audio/<filename>')
@jwt_required()
def uploaded_audio(filename):
    return send_from_directory(os.path.join('../audio'), filename)

@app.route('/video/<filename>')
@jwt_required()
def uploaded_file(filename):
    return send_from_directory(os.path.join('../video'), filename)

@app.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    carpetas = ['video', 'audio', 'frames']
    limpiar_carpetas(carpetas)

    example_file = request.form.get('example_file')
    if example_file:
        source_path = os.path.join('./example_videos', example_file)
        if not os.path.exists(source_path):
            flash('El archivo de ejemplo no existe.')
            return redirect(url_for('index'))
        filepath = os.path.join('video', example_file)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        shutil.copy2(source_path, filepath)
    else:
        if 'file' not in request.files:
            flash('No se encontró el archivo')
            return redirect(url_for('index'))
        file = request.files['file']
        if file.filename == '':
            flash('No se seleccionó ningún archivo')
            return redirect(url_for('index'))
        if not file.filename.lower().endswith('.mp4'):
            flash('Solo se permiten archivos .mp4')
            return redirect(url_for('index'))

        filepath = os.path.join('video', file.filename)
        file.save(filepath)

    progress_file = 'progress.txt'
    with open(progress_file, 'w') as f:
        f.write('0')

    commands = [
        ['pipenv', 'run', 'python', 'src/features/frames_as_jpg_soccernet.py'],
        ['pipenv', 'run', 'python', 'src/features/parse_soccernet.py'],
        ['pipenv', 'run', 'python', 'src/evaluation/test.py', 'src/evaluation/models/model1'],
        ['pipenv', 'run', 'python', 'src/evaluation/test.py', 'src/evaluation/models/model2'],
        ['pipenv', 'run', 'python', 'src/evaluation/test.py', 'src/evaluation/models/model3']
    ]

    try:
        for i, command in enumerate(commands):
            subprocess.run(command, check=True)
            progress = 0
            if i == 0:
                progress = 15
            elif i == 1:
                progress = 25
            elif i == 2:
                progress = 45
            elif i == 3:
                progress = 65
            elif i == 4:
                progress = 85
            with open(progress_file, 'w') as f:
                f.write(str(progress))

        results = []
        json_paths = {
            'model1': 'src/evaluation/models/model1/pred-test.88.json',
            'model2': 'src/evaluation/models/model2/pred-test.140.json',
            'model3': 'src/evaluation/models/model3/pred-test.149.json'
        }
        json_data = []
        for json_path in json_paths.values():
            with open(json_path, 'r') as results_models:
                json_data.append(json.load(results_models))

        combined_results = combine_model_results(json_data[0], json_data[1], json_data[2])

        for result in combined_results:
            video, event_details = procesar_resultados([result])
            results.append(("Resultado combinado", video, event_details))

        text_response = gpt_consumption(progress_file, json_data, script_description)

        tts_consumption(text_response, 'audio', progress_file)

        video_url = url_for('uploaded_file', filename=os.path.basename(filepath))
        audio_url = url_for('uploaded_audio', filename="script.mp3")
        session['video_url'] = video_url
        session['results'] = results
        session['audio_url'] = audio_url

    except subprocess.CalledProcessError as e:
        flash(f'Ocurrió un error: {e}')
    return redirect(url_for('index'))

@app.route('/progress', methods=['GET'])
@jwt_required()
def progress():
    def generate():
        progress_file = 'progress.txt'
        if not os.path.exists(progress_file):
            with open(progress_file, 'w') as f:
                f.write('0')
        
        while True:
            with open(progress_file, 'r') as f:
                progress = f.read().strip()
            yield f"data:{progress}\n\n"
            if progress == '100':
                break

    return app.response_class(generate(), mimetype='text/event-stream')

@app.route('/reset_progress', methods=['POST'])
@jwt_required()
def reset_progress():
    progress_file = 'progress.txt'
    with open(progress_file, 'w') as f:
        f.write('0')
        f.truncate()
    return jsonify({"message": "Progress reset to 0"}), 200

@app.route('/about-us', methods=['GET'])
@jwt_required()
def about_us():
    return render_template('about-us.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

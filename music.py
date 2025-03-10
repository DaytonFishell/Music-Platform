from flask import Flask, request, jsonify, send_from_directory
import os
import uuid

app = Flask(__name__, static_folder='.')

UPLOADS_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}

# Create uploads folder if it doesn't exist
os.makedirs(UPLOADS_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
        file.save(os.path.join(UPLOADS_FOLDER, filename))
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 201
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@app.route('/songs', methods=['GET'])
def list_songs():
    songs = []
    for filename in os.listdir(UPLOADS_FOLDER):
        if allowed_file(filename):
            songs.append({'name': filename.rsplit('.', 1)[0], 'filename': filename})
    return jsonify(songs)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOADS_FOLDER, filename)
@app.route('/style.css')
def style():
    return send_from_directory('.', 'style.css')
@app.route('/')
def index():
    return app.send_static_file('index.html')
@app.route('/script.js')
def script():
    return send_from_directory('.', 'script.js')

if __name__ == '__main__':
    app.run(debug=True)  # remove debug=True for production
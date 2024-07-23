import os
import mimetypes
import docx2txt
from PyPDF2 import PdfReader
from PIL import Image
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

def get_file_info(file_path, search_words):
    size = os.path.getsize(file_path)
    file_type = mimetypes.guess_type(file_path)[0]
    word_count = 0
    char_count = 0
    found_words = []

    try:
        content = ""
        if file_type == 'text/plain':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        elif file_type == 'application/pdf':
            reader = PdfReader(file_path)
            for page in reader.pages:
                content += page.extract_text()
        elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            content = docx2txt.process(file_path)
        elif file_type and file_type.startswith('image/'):
            with Image.open(file_path) as img:
                width, height = img.size
            char_count = width * height  # Total pixels
        
        if content:
            word_count = len(content.split())
            char_count = len(content)
            content_lower = content.lower()
            for word in search_words:
                if word.lower() in content_lower:
                    found_words.append(word)

    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

    return size, file_type, word_count, char_count, found_words

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        root_folder = request.form['root_folder']
        file_names = [name.strip() for name in request.form['file_names'].split(',')] if request.form['file_names'] else []
        search_words = [word.strip() for word in request.form['search_words'].split(',')] if request.form['search_words'] else []

        results = []
        files = request.files.getlist('files')
        for file in files:
            relative_path = file.filename
            if not file_names or any(name in relative_path for name in file_names):
                filename = secure_filename(os.path.basename(relative_path))
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                size, file_type, word_count, char_count, found_words = get_file_info(file_path, search_words)
                results.append({
                    'filename': filename,
                    'file_path': os.path.join(root_folder, relative_path),
                    'size': size,
                    'file_type': file_type,
                    'word_count': word_count,
                    'char_count': char_count,
                    'found_words': ', '.join(found_words)
                })
                
                os.remove(file_path)

        return jsonify(results)
    
    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
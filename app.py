from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from sat_core import generate_collage

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'results'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('images')
        sat_model = request.form.get('sat_model')
        orbit = request.form.get('orbit')

        if len(files) != 4:
            return "Musisz przesłać dokładnie 4 zdjęcia.", 400

        image_paths = []
        for f in files:
            filename = secure_filename(f.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            f.save(path)
            image_paths.append(path)

        output_path = os.path.join(app.config['RESULT_FOLDER'], 'kolaz.jpg')

        try:
            generate_collage(image_paths, sat_model, orbit, output_path)
        except Exception as e:
            return f"Błąd przetwarzania: {e}", 500

        return redirect(url_for('result'))

    return render_template('upload.html')

@app.route('/result')
def result():
    return render_template('result.html', collage_path='results/kolaz.jpg')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)
    app.run(debug=True)

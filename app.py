from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from utils import extract_text_from_pdf, call_llm_model, process_cv_with_all_models, AVAILABLE_MODELS

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', models=AVAILABLE_MODELS)

@app.route('/extract', methods=['POST'])
def extract():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    model = request.form.get('model', 'llama3')
    process_all = request.form.get('process_all', 'false') == 'true'
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)

        # Extract text from PDF
        text = extract_text_from_pdf(filepath)
        
        # Save the extracted text for reference
        text_path = os.path.join(app.config['RESULTS_FOLDER'], f"{unique_filename}_text.txt")
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        if process_all:
            # Process with all models
            results = process_cv_with_all_models(text)
        else:
            # Process with selected model
            results = {model: call_llm_model(text, model)}
        
        # Save results to JSON file
        result_path = os.path.join(app.config['RESULTS_FOLDER'], f"{unique_filename}_results.json")
        with open(result_path, 'w') as f:
            json.dump(results, f, indent=4)
        
        return jsonify({
            'data': results,
            'filename': unique_filename,
            'text_path': f"/results/{unique_filename}_text.txt",
            'result_path': f"/results/{unique_filename}_results.json"
        }), 200

    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/results/<filename>')
def results(filename):
    return send_from_directory(app.config['RESULTS_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

import os
import io
import base64
from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image
from model import detect_sheep
from my_utils import add_record, load_history, generate_excel_report

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/history')
def history():
    records = load_history()
    return render_template('history.html', records=records)

@app.route('/process_image', methods=['POST'])
def process_image():
    data = request.get_json()
    img_data = data['image'].split(',')[1]  # Удаляем префикс
    img_bytes = base64.b64decode(img_data)
    img = Image.open(io.BytesIO(img_bytes)).convert('RGB')

    # Детекция овец
    img_result, count = detect_sheep(img)

    # Сохраняем изображение с результатом
    img_id = len(load_history()) + 1
    filename = f'sheep_{img_id}.png'
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    img_result.save(filepath)

    # Добавляем запись в историю
    record = add_record(filepath, count)

    return jsonify({
        'id': record['id'],
        'date': record['date'],
        'sheep_count': count,
        'image_url': '/' + filepath.replace('\\', '/')
    })

@app.route('/download_report')
def download_report():
    filename = generate_excel_report()
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

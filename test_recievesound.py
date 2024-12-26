from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # เปิดใช้งาน CORS สำหรับทุก endpoint

# กำหนดโฟลเดอร์ในการอัปโหลดไฟล์
UPLOAD_FOLDER = 'uploads'
API_KEY = '15e568ee86a24818b68fab30a3e4f1ce'  # คีย์สำหรับการ authentication
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# สร้างโฟลเดอร์สำหรับจัดเก็บไฟล์ หากยังไม่มี
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ตรวจสอบ API Key
def check_api_key(key):
    return key == API_KEY

# ฟังก์ชันสำหรับอัปโหลดไฟล์
@app.route('/upload', methods=['POST'])
def upload_file():
    api_key = request.headers.get('API-Key')
    if not check_api_key(api_key):
        return jsonify({'error': 'Unauthorized'}), 401

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # จัดการชื่อไฟล์ให้ไม่ซ้ำ
    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return jsonify({'message': 'File uploaded successfully'}), 200

# ฟังก์ชันสำหรับแสดงรายการไฟล์ทั้งหมด
@app.route('/files', methods=['GET'])
def list_files():
    api_key = request.headers.get('API-Key')
    if not check_api_key(api_key):
        return jsonify({'error': 'Unauthorized'}), 401

    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files)

# ฟังก์ชันสำหรับดึงไฟล์ที่ระบุ
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    api_key = request.headers.get('API-Key')
    if not check_api_key(api_key):
        return jsonify({'error': 'Unauthorized'}), 401

    # ตรวจสอบว่าไฟล์ที่ร้องขอมีอยู่ในโฟลเดอร์หรือไม่
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, render_template, request, send_file, jsonify
import os
import tempfile
import re
import qrcode
from io import BytesIO
import base64
from PIL import Image
import io
import PyPDF2
from docx import Document
import zipfile

app = Flask(__name__)

# ============================================================
# HOME PAGE
# ============================================================
@app.route('/')
def index():
    return render_template('index.html')

# ============================================================
# QR CODE GENERATOR
# ============================================================
@app.route('/qr-generator')
def qr_generator():
    return render_template('qr-generator.html')

@app.route('/generate-qr', methods=['POST'])
def generate_qr():
    data = request.form.get('data', '')
    if not data:
        return jsonify({'error': 'Please enter URL or text'}), 400
    
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({'success': True, 'image': img_str})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        # ============================================================
# PDF COMPRESSOR (Backend)
# ============================================================
@app.route('/compress-pdf', methods=['POST'])
def compress_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF uploaded'}), 400
    
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({'error': 'No PDF selected'}), 400
    
    try:
        from PyPDF2 import PdfReader, PdfWriter
        import io
        
        pdf_reader = PdfReader(file.stream)
        pdf_writer = PdfWriter()
        
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
        
        # Compress using PyPDF2's compression
        output = io.BytesIO()
        pdf_writer.write(output)
        output.seek(0)
        
        return send_file(
            output,
            as_attachment=True,
            download_name='compressed.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================
# IMAGE RESIZER
# ============================================================
@app.route('/image-resizer')
def image_resizer():
    return render_template('image-resizer.html')

# ============================================================
# IMAGE CONVERTER
# ============================================================
@app.route('/image-converter')
def image_converter():
    return render_template('image-converter.html')

@app.route('/convert-image', methods=['POST'])
def convert_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    format_type = request.form.get('format', 'PNG')
    
    try:
        img = Image.open(file.stream)
        
        # Convert to RGB if necessary
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        
        buffered = BytesIO()
        img.save(buffered, format=format_type)
        buffered.seek(0)
        
        # Convert to base64 for display
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'image': img_base64,
            'format': format_type
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================
# UNIT CONVERTER
# ============================================================
@app.route('/unit-converter')
def unit_converter():
    return render_template('unit-converter.html')
    # ============================================================
# CURRENCY CONVERTER
# ============================================================
@app.route('/currency-converter')
def currency_converter():
    return render_template('currency-converter.html')

# ============================================================
# AGE CALCULATOR
# ============================================================
@app.route('/age-calculator')
def age_calculator():
    return render_template('age-calculator.html')

# ============================================================
# CASE CONVERTER
# ============================================================
@app.route('/case-converter')
def case_converter():
    return render_template('case-converter.html')

# ============================================================
# PASSWORD GENERATOR
# ============================================================
@app.route('/password-generator')
def password_generator():
    return render_template('password-generator.html')

# ============================================================
# WORD COUNTER
# ============================================================
@app.route('/word-counter')
def word_counter():
    return render_template('word-counter.html')

# ============================================================
# PDF TO WORD
# ============================================================
@app.route('/pdf-to-word')
def pdf_to_word():
    return render_template('pdf-to-word.html')

@app.route('/convert-pdf-to-word', methods=['POST'])
def convert_pdf_to_word():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF uploaded'}), 400
    
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({'error': 'No PDF selected'}), 400
    
    try:
        pdf_reader = PyPDF2.PdfReader(file.stream)
        doc = Document()
        
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                doc.add_paragraph(text)
        
        # Save to temp file
        temp_dir = tempfile.mkdtemp()
        output_path = os.path.join(temp_dir, 'output.docx')
        doc.save(output_path)
        
        return send_file(
            output_path,
            as_attachment=True,
            download_name='converted.docx'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================
# PDF COMPRESSOR
# ============================================================
@app.route('/pdf-compressor')
def pdf_compressor():
    return render_template('pdf-compressor.html')

    # ============================================================
# TEXT TO SPEECH
# ============================================================
@app.route('/text-to-speech')
def text_to_speech():
    return render_template('text-to-speech.html')

    # ============================================================
# NOTES / TODO LIST
# ============================================================
@app.route('/notes')
def notes():
    return render_template('notes.html')

    # ============================================================
# RANDOM NUMBER GENERATOR
# ============================================================
@app.route('/random-number')
def random_number():
    return render_template('random-number.html')
    
    # ============================================================
# BMI CALCULATOR
# ============================================================
@app.route('/bmi-calculator')
def bmi_calculator():
    return render_template('bmi-calculator.html')

# ============================================================
# RUN SERVER
# ============================================================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
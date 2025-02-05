import os
from flask import current_app

def save_uploaded_file(file):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)
    return file_path

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {
        'pdf', 'jpg', 'jpeg', 'png', 'jfif',
        'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'odt', 'rtf', 'txt'
    }
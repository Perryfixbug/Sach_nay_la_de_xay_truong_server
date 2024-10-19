from werkzeug.utils import secure_filename
import os
from flask import current_app

# Thư mục lưu ảnh
def image_path(endpoint = None):
    return f'static/image/{endpoint}'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file = None, endpoint = None):
    if file and allowed_file(file.filename):
        image_filename = secure_filename(file.filename)
        current_app.config['UPLOAD_FOLDER'] = image_path(endpoint)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename))
        return True,image_filename,200
    else: return False,"Định dạng ảnh không chính xác!", 401
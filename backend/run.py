from app import create_app
from flask import send_from_directory
import os

app = create_app()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print("Serving file:", full_path)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
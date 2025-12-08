from app import create_app
import os
from flask import send_from_directory

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)

    UPLOAD_FOLDER = os.path.join(os.patch.firname(os.path.abspath(__file__)), 'uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                     build_only=False,
                     view_func=lambda filename: send_from_directory(app.config['UPLOAD_FOLDER'], filename))

from pathlib import Path
from werkzeug.utils import secure_filename

def save_upload(file, upload_dir):
    Path(upload_dir).mkdir(parents=True, exist_ok=True)
    filename = secure_filename(file.filename)
    path = Path(upload_dir) / filename
    file.save(path)
    return filename

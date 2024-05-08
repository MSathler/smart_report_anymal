from flask import Flask, render_template, send_from_directory, abort
from werkzeug.utils import safe_join
import os

app = Flask(__name__)
#BASE_DIRS = ['/root/reports'] # Producao
BASE_DIRS = ['/Users/mauriciosathler/Desktop/itabira/ANYmal/'] # Teste

@app.template_filter('dirname')
def dirname_filter(path):
    # Strip trailing slashes to prevent '//'
    if path in ['', '/']:
        return None
    parent_path = os.path.dirname(path)
    if parent_path in ['', '/']:
        return ''  # Return an empty string for root
    return parent_path

@app.route('/')
@app.route('/<path:path>')
def files(path=''):
    for base_dir in BASE_DIRS:
        abs_path = safe_join(base_dir, path)
        
        if os.path.isfile(abs_path):
            if abs_path.endswith(('.html', '.png', '.jpeg', '.jpg', '.wav', '.mp4')):
                return send_from_directory(os.path.dirname(abs_path), os.path.basename(abs_path))
            continue

        elif os.path.isdir(abs_path):
            entries = os.listdir(abs_path)
            filtered_entries = []
            for entry in entries:
                full_path = os.path.join(abs_path, entry)
                entry_data = {
                    'name': entry,
                    'path': os.path.join(path, entry),
                    'is_folder': os.path.isdir(full_path)
                }
                if os.path.isdir(full_path) or entry.endswith(('.html', '.png', '.jpeg', '.jpg', '.wav', '.mp4')):
                    filtered_entries.append(entry_data)

            return render_template('Tfiles.html', files=filtered_entries, path=path)

    abort(404)  # If no path exists in any base directories

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8000)

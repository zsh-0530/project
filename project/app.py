from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 最大16MB

def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS records
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  image TEXT,
                  text TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM records ORDER BY id DESC")
    records = c.fetchall()
    conn.close()
    return render_template('index.html', records=records)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        text = request.form['text']
        file = request.files['image']

        if file:
            filename = secure_filename(file.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute("INSERT INTO records (image, text) VALUES (?, ?)",
                      (filename, text))
            conn.commit()
            conn.close()

        return redirect(url_for('index'))

    return render_template('upload.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)

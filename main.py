from flask import Flask, request, jsonify
import os
import base64
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# SQLite database setup
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn




# Регистрация
@app.route('/asd', methods=['POST'])
def setup_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            image_path TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.close()
    print("Database and tables created!")
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400
    finally:
        conn.close()

# Логин
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cur.fetchone()
    conn.close()
    
    if user:
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 400

# Добавление entry с изображением
@app.route('/add_entry', methods=['POST'])
def add_entry():
    data = request.get_json()
    user_id = data.get('user_id')
    base64_image = data.get('image')

    if not user_id or not base64_image:
        return jsonify({"error": "User ID and image are required"}), 400

    image_data = base64.b64decode(base64_image)
    filename = f'{secure_filename(str(user_id))}.png'
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    with open(image_path, 'wb') as img_file:
        img_file.write(image_data)

    conn = get_db_connection()
    conn.execute("INSERT INTO entries (user_id, image_path) VALUES (?, ?)", (user_id, image_path))
    conn.commit()
    conn.close()

    return jsonify({"message": "Entry added successfully!", "image_path": image_path}), 201

# Получение всех entry пользователя с изображениями
@app.route('/get_entries/<int:user_id>', methods=['GET'])
def get_entries(user_id):
    conn = get_db_connection()
    entries = conn.execute("SELECT * FROM entries WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()

    results = []
    for entry in entries:
        results.append({
            "id": entry['id'],
            "image_path": entry['image_path']
        })
    
    return jsonify({"entries": results}), 200

if __name__ == '__main__':
    
    app.run(debug=True)

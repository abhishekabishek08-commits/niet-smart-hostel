from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('hostel.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            room_number TEXT,
            description TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'POST':
        student_name = request.form['student_name']
        room_number = request.form['room_number']
        description = request.form['description']
        
        conn = sqlite3.connect('hostel.db')
        c = conn.cursor()
        c.execute('INSERT INTO complaints (student_name, room_number, description, status) VALUES (?, ?, ?, ?)', 
                  (student_name, room_number, description, 'Pending'))
        conn.commit()
        conn.close()
        return redirect(url_for('student'))
        
    conn = sqlite3.connect('hostel.db')
    c = conn.cursor()
    c.execute('SELECT * FROM complaints ORDER BY id DESC')
    complaints = c.fetchall()
    conn.close()
    
    return render_template('student.html', complaints=complaints)

@app.route('/warden', methods=['GET', 'POST'])
def warden():
    if request.method == 'POST':
        complaint_id = request.form['complaint_id']
        conn = sqlite3.connect('hostel.db')
        c = conn.cursor()
        c.execute("UPDATE complaints SET status = 'In Progress' WHERE id = ?", (complaint_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('warden'))

    conn = sqlite3.connect('hostel.db')
    c = conn.cursor()
    c.execute('SELECT * FROM complaints')
    complaints = c.fetchall()
    conn.close()
    
    return render_template('warden.html', complaints=complaints)

@app.route('/staff', methods=['GET', 'POST'])
def staff():
    if request.method == 'POST':
        complaint_id = request.form['complaint_id']
        conn = sqlite3.connect('hostel.db')
        c = conn.cursor()
        c.execute("UPDATE complaints SET status = 'Resolved' WHERE id = ?", (complaint_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('staff'))

    conn = sqlite3.connect('hostel.db')
    c = conn.cursor()
    c.execute("SELECT * FROM complaints WHERE status = 'In Progress' OR status = 'Resolved'")
    complaints = c.fetchall()
    conn.close()
    
    return render_template('staff.html', complaints=complaints)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

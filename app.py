from flask import Flask, render_template, request
import sqlite3
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Load XML controls configuration
tree = ET.parse('controls.xml')
root = tree.getroot()

@app.route('/')
def index():
    return render_template('index.html', controls=root)

@app.route('/submit', methods=['POST'])
def submit():
    # Access submitted form data
    form_data = {control.attrib['id']: request.form.get(control.attrib['id']) for control in root}

    # Store data in SQLite database
    store_in_database(form_data)

    return 'Data submitted successfully!'

def store_in_database(data):
    # Connect to SQLite database
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS userdata
                       (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        control_id TEXT, 
                        value TEXT)''')

    # Insert data into the table
    for control_id, value in data.items():
        cursor.execute('INSERT INTO userdata (control_id, value) VALUES (?, ?)', (control_id, value))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)

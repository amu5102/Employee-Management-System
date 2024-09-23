from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect('employees.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            position TEXT NOT NULL,
                            salary REAL NOT NULL)''')
        conn.commit()

init_db()

# Home page to view all employees
@app.route('/')
def index():
    with sqlite3.connect('employees.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()
    return render_template('index.html', employees=employees)

# Add employee
@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        salary = request.form['salary']
        with sqlite3.connect('employees.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO employees (name, position, salary) VALUES (?, ?, ?)", 
                           (name, position, salary))
            conn.commit()
        return redirect(url_for('index'))
    return render_template('add_employee.html')

# Edit employee
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    with sqlite3.connect('employees.db') as conn:
        cursor = conn.cursor()
        if request.method == 'POST':
            name = request.form['name']
            position = request.form['position']
            salary = request.form['salary']
            cursor.execute("UPDATE employees SET name=?, position=?, salary=? WHERE id=?", 
                           (name, position, salary, id))
            conn.commit()
            return redirect(url_for('index'))
        cursor.execute("SELECT * FROM employees WHERE id=?", (id,))
        employee = cursor.fetchone()
    return render_template('edit_employee.html', employee=employee)

# Delete employee
@app.route('/delete/<int:id>')
def delete_employee(id):
    with sqlite3.connect('employees.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id=?", (id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

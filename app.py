from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "flash message"

app.config ['MYSQL_HOST'] = 'localhost'
app.config ['MYSQL_USER'] = 'root'
app.config ['MYSQL_PASSWORD'] = '123456'
app.config ['MYSQL_DB'] = 'crudapplicatioin'

mysql = MySQL(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
@app.route('/')
def Index():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()

    cur.close()


    return render_template('index.html', students = data)

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        flash("Data Inserted Successfully")

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/update', methods = ['POST','GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE students
        SET name=%s, email=%s, phone=%s
        where id=%s
        """, (name, email, phone, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()

        return redirect(url_for('Index'))


@app.route('/delete/<id_data>', methods=['POST', 'GET'])
def delete(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", [id_data])
    mysql.connection.commit()

    return redirect(url_for('Index'))

@app.route('/get')
def get():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()

    cur.close()
    return jsonify({"Students":data})


if __name__ == '__main__':
    app.run(debug=True)
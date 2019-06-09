import cv2
import numpy as np
import pymysql
from flask import render_template, request
from src.main.application.app import app
from src.main.application.config.db_config import mysql
from src.main.application.web_components.tables import Results
from PIL import Image
import base64




@app.route('/')
def start():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/log',methods=["GET","POST"])
def log():
    if request.method == 'POST':
        data_url = request.data
        content = data_url.split(b';')[1]
        image_encoded = content.split(b',')[1]
        data = base64.decodebytes(image_encoded)
        nparr = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # verify if image is received correctly
        # cv2.imshow('Image',img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    return render_template('log.html')

@app.route('/table')
def table():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT *"                        
                        "FROM person AS p "
                        "JOIN log AS l "
                        "    on p.person_id = l.log_person "
                        "JOIN attendance AS a "
                        "    on l.log_attendance = a.attendance_id ")
        rows = cursor.fetchall()
        table = Results(rows)
        table.border = True
        return render_template('table.html', table=table)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/home',methods=['GET'])
def home():
    return render_template('home.html')



@app.route('/login', methods=['POST'])
def login():
    _name = request.form['inputName']
    _password = request.form['inputPassword']
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT user_id FROM user WHERE user_name=%s AND user_password=%s", [_name,_password])
        row = cursor.fetchone()
        if row:
            return render_template('home.html')
        else:
            return 'Error loading #{_name}'.format(name=_name)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()



if __name__ == "__main__":
    app.run()
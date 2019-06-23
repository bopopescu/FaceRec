from random import randint

import cv2
import numpy as np
import pymysql
from flask import render_template, request
from src.main.application.app import app
from src.main.application.config.db_config import mysql
from src.main.application.web_components.tables import Results
import base64
import json
from src.main.FaceRec.FaceRec import FaceRec



imagesToRegister = [];

newImagesToRegister = [];

@app.route('/')
def start():
    return render_template('login.html')


@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':

        if( len(imagesToRegister)==0 ):

            data_url = request.json

            for image in data_url:
                content = image.split(';')[1]
                data = content.split(',')[1]
                image_encoded = base64.standard_b64decode(data)
                nparr = np.frombuffer(image_encoded, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                imagesToRegister.append(img);

        else:

            _username = request.form['inputUsername']
            _password = request.form['inputPass']
            _password2 = request.form['inputPass2']

            _name = request.form['inputName']
            _email = request.form['inputEmail']
            _age = request.form['inputAge']
            _sex = request.form['inputSex']

            try:
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)

                cursor.execute("SELECT user_id FROM user ORDER BY user_id DESC LIMIT 1")
                result = cursor.fetchone()
                user_id = result['user_id']
                user_id = user_id + 1

                data_user = (user_id, _username, _password)
                insert_stmt_user = (
                    "INSERT INTO user (user_id,user_name,user_password) "
                    "VALUES (%s, %s, %s)"
                )
                cursor.execute(insert_stmt_user, data_user)
                # conn.commit()

                cursor.execute("SELECT person_id FROM person ORDER BY person_id DESC LIMIT 1")
                result = cursor.fetchone()
                person_id = result['person_id']
                person_id = person_id + 1

                data_person = (person_id, _name, _email, _age, _sex, "")
                insert_stmt_person = (
                    "INSERT INTO person (person_id,person_name,person_email,person_age,person_sex,person_picture_data) "
                    "VALUES (%s, %s, %s, %s, %s, %s)"
                )
                cursor.execute(insert_stmt_person, data_person)
                # conn.commit()

                data_user_person = (user_id, person_id)
                insert_stmt_user_person = (
                    "INSERT INTO user_person (user_id,person_id) "
                    "VALUES (%s, %s)"
                )
                cursor.execute(insert_stmt_user_person, data_user_person)
                conn.commit()

            except Exception as e:
                print(e)
            finally:
                cursor.close()
                conn.close()


            #creates the new user face alignament data
            facerec.create_manual_data(imagesToRegister,_name);

            #clears the image list
            imagesToRegister.clear()

        return render_template('login.html')

    # if request.method == 'GET':
    return render_template('register.html')


@app.route('/profile', methods=['POST','GET'])
def profile():
    if request.method == 'POST':

        if( len(newImagesToRegister)==0 ):

            data_url = request.json

            for image in data_url:
                content = image.split(';')[1]
                data = content.split(',')[1]
                image_encoded = base64.standard_b64decode(data)
                nparr = np.frombuffer(image_encoded, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                newImagesToRegister.append(img);

        else:

            _name = request.form['inputName']

            #creates the new user face alignament data
            facerec.create_manual_data(newImagesToRegister,_name);

            #clears the image list
            newImagesToRegister.clear();

    # if request.method == 'GET':
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

        #recog_data[0][0] - name of the recognized person
        #recog_data[0][1] - precision
        recog_data = facerec.camera_recog(img)

        try:
            from datetime import date,datetime

            today = date.today()
            # dd/mm/YY
            d1 = today.strftime("%d/%m/%Y")

            now = datetime.now()
            current_time = now.strftime("%H:%M")

            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            cursor.execute("SELECT a.attendance_id FROM attendance AS a ORDER BY a.attendance_id DESC LIMIT 1")
            result = cursor.fetchone()
            attendance_id = result['attendance_id']
            attendance_id  = attendance_id+1

            data_attendance = (attendance_id, d1, current_time, current_time, 0)
            insert_stmt_attendance = (
                "INSERT INTO attendance (attendance_id, attendance_date, attendance_in, attendance_out, attendance_duration) "
                "VALUES (%s, %s, %s, %s, %s)"
            )
            cursor.execute(insert_stmt_attendance, data_attendance)
            conn.commit()

            select_person_id_data = recog_data[0][0]
            select_person_id_stmt = (
                "SELECT p.person_id "
                "FROM person AS p "
                "WHERE p.person_name LIKE %s"
            )
            cursor.execute(select_person_id_stmt,select_person_id_data)
            result = cursor.fetchone()
            person_id = result['person_id']

            data_log = (person_id, attendance_id)
            insert_stmt_log = (
                "INSERT INTO log (log_person, log_attendance) "
                "VALUES (%s, %s)"
            )
            cursor.execute(insert_stmt_log, data_log)
            conn.commit()

        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    return render_template('log.html')

@app.route('/table')
def table():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute( "SELECT * "                        
                        "FROM person AS p "
                        "JOIN log AS l "
                        "    on p.person_id = l.log_person "
                        "JOIN attendance AS a "
                        "    on l.log_attendance = a.attendance_id "
                        "ORDER BY STR_TO_DATE(a.attendance_date,'%d/%m/%Y') DESC, a.attendance_in DESC")
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
    facerec = FaceRec()
    app.run()
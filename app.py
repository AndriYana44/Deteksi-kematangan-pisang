#!/usr/bin/python
import os
import cv2
import numpy as np
import mysql.connector
from flask import Flask, render_template, request, redirect, jsonify, json
from werkzeug.utils import secure_filename

mydb = mysql.connector.connect(
  host="localhost",
  user="user",
  password="user",
  database="flask-dev",
  # auth_plugin="mysql_native_password"
)

mycursor = mydb.cursor()

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getPercentage(objLow, objHigh, imgHsv):
    low = np.array(objLow, np.uint8)
    high = np.array(objHigh, np.uint8)
    mask = cv2.inRange(imgHsv, low, high)
    percentage = np.round((cv2.countNonZero(mask) / (imgHsv.size/3)) * 100, 2)

    return percentage

def getResult(img_hsv):
    res = {}
    # sangat matang
    res['sangat matang'] = getPercentage([20, 60, 60], [26, 150, 255], img_hsv)
    # matang
    res['matang'] = getPercentage([27, 60, 60], [36, 150, 255], img_hsv)
    # mentah
    res['mentah'] = getPercentage([37, 60, 60], [60, 150, 255], img_hsv)
    return res

def getData(query):
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data

# membuat persentase final
def percentageFIX():
    data_percentage = getData("SELECT * FROM percentage")
    for percentage in data_percentage:
        total = float(percentage[1]) + float(percentage[2]) + float(percentage[3])
    percentage_mentah = (float(percentage[1]) / round(total)) * 100
    percentage_matang = (float(percentage[2]) / round(total)) * 100
    percentage_sangat_matang = (float(percentage[3]) / round(total)) * 100
    res = {1:round(percentage_mentah, 2), 2:round(percentage_matang, 2), 3:round(percentage_sangat_matang, 2)}
    return res

@app.route('/api/suhu')
def getSuhu():
    try:
        suhu = getData("SELECT * FROM suhu")
        for val in suhu:
            jsonStr = json.dumps(val[1])
    except Exception:
        print(Exception)
    return jsonify(Employees=jsonStr)

@app.route('/')
def upload():
    data_max = getData("SELECT * FROM max_result")
    res = percentageFIX()
    return render_template('index.html', data_max=data_max, res=res)

@app.route('/testing')
def testing():
    data_max = getData("SELECT * FROM max_result")
    res = percentageFIX()
    return render_template('testing.html', res=res, data_max=data_max)

@app.route('/grafik')
def grafik():
    data_max = getData("SELECT * FROM max_result")
    res = percentageFIX()
    return render_template('grafik.html', res=res, data_max=data_max)

@app.route('/suhu', methods=['GET'])
def search():
    delete_suhu = "TRUNCATE TABLE suhu"   
    mycursor.execute(delete_suhu)

    args = request.args
    suhu = args.get('suhu')
    if suhu != 0 and suhu != '':
        sql_suhu = "INSERT INTO suhu (suhu) VALUES (%s)"
        mycursor.execute(sql_suhu, (suhu,))
        mydb.commit()
        return '', 200
    return '', 500

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['imageFile']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'data.jpg'))

        img = cv2.imread('./static/img/data.jpg')
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        percentage = getResult(img_hsv)
        hasil = max(percentage, key=percentage.get)
        if max(percentage.values()) < 1:
            hasil = 'Pisang Tidak Terdeteksi'

        if(max(percentage.values()) > 1):
            delete_sql_max = "TRUNCATE TABLE max_result"   
            delete_percentage = "TRUNCATE TABLE percentage"   
            mycursor.execute(delete_sql_max)
            mycursor.execute(delete_percentage)

            sql_max_result = "INSERT INTO max_result (data) VALUES (%s)"
            sql_percentage = "INSERT INTO percentage (mentah, matang, sangat_matang) VALUES (%s, %s, %s)"
            mycursor.execute(sql_max_result, (hasil,))
            mycursor.execute(sql_percentage, (float(percentage['mentah']), float(percentage['matang']), float(percentage['sangat matang'])))
            mydb.commit()

        return redirect('/')
		
if __name__ == '__main__':
   app.run(host='192.168.43.150', port=80, debug = True)

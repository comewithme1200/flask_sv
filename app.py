#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_mysqldb import MySQL
import uuid

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost:3306'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'truong_hoc'
jwt = JWTManager(app)
api = Api(app)
mysql = MySQL(app)

# APIs
@app.route('/sinh_vien', methods=['POST'])
def them_sinh_vien():
    ma_sinh_vien = str(uuid.uuid4())
    ho_ten = request.form['ho_ten']
    gioi_tinh = request.form['gioi_tinh']
    ngay_sinh = request.form['ngay_sinh']
    que_quan = request.form['que_quan']
    lop = request.form['lop']
    khoa = request.form['khoa']

      
    cur = mysql.connection.cursor()

    # data = sinh_vien(
    #     ma_sinh_vien,
    #     ho_ten,
    #     gioi_tinh,
    #     ngay_sinh,
    #     que_quan,
    #     lop,
    #     khoa
    #     )
    
    cur.execute("INSERT INTO sinh_vien (ma_sinh_vien, ho_ten, gioi_tinh, ngay_sinh, que_quan, lop, khoa) VALUES (%s, %s, %s, %s, %s, %s, %s)", (ma_sinh_vien, ho_ten, gioi_tinh, ngay_sinh, que_quan, lop, khoa))
    mysql.connection.commit()

    return 'Success'

@app.route('/sinh_vien/<string:ma_sinh_vien>', methods=['PUT'])
def sua_sinh_vien():
    ho_ten = request.form['ho_ten']
    gioi_tinh = request.form['gioi_tinh']
    ngay_sinh = request.form['ngay_sinh']
    que_quan = request.form['que_quan']
    lop = request.form['lop']
    khoa = request.form['khoa']  

    cur = mysql.connection.cursor()
    cur.execute("""
               UPDATE students
               SET ho_ten=%s, gioi_tinh=%s, ngay_sinh=%s, que_quan=%s, lop=%s, khoa=%s
               WHERE ma_sinh_vien=%s
            """, (ho_ten, gioi_tinh, ngay_sinh, que_quan, lop, khoa, ma_sinh_vien))
    mysql.connection.commit()
    return 'success'

@app.route('/sinh_vien', methods=['GET'])
def get_sinh_vien():  
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM sinh_vien")
    data = cur.fetchall()
    cur.close()

    return jsontify(data)

@app.route('/sinh_vien/<string:ma_sinh_vien>')
def xoa_sinh_vien():  
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM sinh_vien WHERE ma_sinh_vien=%s", (ma_sinh_vien))
    mysql.connection.commit()
    return 'success'


if __name__ == '__main__':
    app.run(debug=True)

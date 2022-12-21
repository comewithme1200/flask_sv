#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_mysqldb import MySQL
import uuid

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'truong_hoc'
jwt = JWTManager(app)
api = Api(app)
mysql = MySQL(app)

# APIs
@app.route('/sinh_vien', methods=['POST'])
def them_sinh_vien():
    jsonData = request.get_json()
    print(str(uuid.uuid4()))
    ma_sinh_vien = str(uuid.uuid4())
    print(ma_sinh_vien)
    ho_ten = jsonData['ho_ten']
    gioi_tinh = jsonData['gioi_tinh']
    ngay_sinh = jsonData['ngay_sinh']
    que_quan = jsonData['que_quan']
    lop = jsonData['lop']
    khoa = jsonData['khoa']

      
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

@app.route('/sinh_vien', methods=['PUT'])
def sua_sinh_vien():
    jsonData = request.get_json()
    ma_sinh_vien = jsonData['ma_sinh_vien']
    ho_ten = jsonData['ho_ten']
    gioi_tinh = jsonData['gioi_tinh']
    ngay_sinh = jsonData['ngay_sinh']
    que_quan = jsonData['que_quan']
    lop = jsonData['lop']
    khoa = jsonData['khoa']  

    cur = mysql.connection.cursor()
    cur.execute("""
               UPDATE sinh_vien
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

    return jsonify(data)
    # print(jsontify(data))


@app.route('/sinh_vien', methods=['DELETE'])
def xoa_sinh_vien():  
    jsonData = request.get_json()
    ma_sinh_vien = jsonData['ma_sinh_vien']
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM sinh_vien WHERE ma_sinh_vien=%s", (ma_sinh_vien))
    mysql.connection.commit()
    return 'success'


if __name__ == '__main__':
    app.run(debug=True)

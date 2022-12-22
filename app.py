#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

from flask import Flask, request, jsonify, make_response
from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_mysqldb import MySQL
import uuid
import jwt
import date_time
from functools import wraps
import jwt
import date_time
from functools import wraps

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'truong_hoc'
app.config['SECRET_KEY'] = 'secretkey'
app.config['SECRET_KEY'] = 'secretkey'
jwt = JWTManager(app)
api = Api(app)
mysql = MySQL(app)


# authentication
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')

        if not token:
            return jsonify({'message' : 'Token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return make_response('Forbidden', 403)

        return f(*arg, **kwargs)

@app.route('/login')
def login():
    jsonData = request.get_json()
    ten_dang_nhap = jsonData['ten_dang_nhap']
    mat_khau = jsonData['mat_khau']

    cur = mysql.connection.cursor()

    cur.execute("SELECT mat_khau FROM tai_khoan WHERE ten_dang_nhap=%s", (mat_khau, ten_dang_nhap))
    userPasswd = jsonify(cur.fetchone())
    cur.close()

    if userPasswd == '' or mat_khau != userPasswd:
        return make_response('Sai tài khoản hoặc mật khẩu', 401)
    else if userPasswd == mat_khau:
        token = jwt.encode({'ten_dang_nhap' : ten_dang_nhap, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)})
        return jsonify({'token' : token.decode('UTF-8')})

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

#giang vien
@app.route('/giang_vien', methods=['POST'])
def them_giang_vien():
    jsonData = request.get_json()
    ma_giang_vien = str(uuid.uuid4())
    ho_ten = jsonData['ho_ten']
    gioi_tinh = jsonData['gioi_tinh']
    ngay_sinh = jsonData['ngay_sinh']
    chuc_vu = jsonData['chuc_vu']
    khoa = jsonData['khoa']  

      
    cur = mysql.connection.cursor()

    cur.execute("INSERT INTO giang_vien (ma_giang_vien, ho_ten, gioi_tinh, ngay_sinh, khoa, chuc_vu) VALUES (%s, %s, %s, %s, %s, %s)", (ma_giang_vien, ho_ten, gioi_tinh, ngay_sinh, que_quan, lop, khoa))
    mysql.connection.commit()

    return 'Success'

@app.route('/giang_vien', methods=['PUT'])
def sua_giang_vien():
    jsonData = request.get_json()
    ma_giang_vien = jsonData['ma_giang_vien']
    ho_ten = jsonData['ho_ten']
    gioi_tinh = jsonData['gioi_tinh']
    ngay_sinh = jsonData['ngay_sinh']
    chuc_vu = jsonData['chuc_vu']
    khoa = jsonData['khoa']  

    cur = mysql.connection.cursor()
    cur.execute("""
               UPDATE giang_vien
               SET ho_ten=%s, gioi_tinh=%s, ngay_sinh=%s, lop=%s, khoa=%s, chuc_vu=%s
               WHERE ma_giang_vien=%s
            """, (ho_ten, gioi_tinh, ngay_sinh, que_quan, lop, khoa, chuc_vu, ma_giang_vien))
    mysql.connection.commit()
    return 'success'

@app.route('/giang_vien', methods=['GET'])
def get_giang_vien():  
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM giang_vien")
    data = cur.fetchall()
    cur.close()

    return jsonify(data)


@app.route('/giang_vien', methods=['DELETE'])
def xoa_giang_vien():  
    jsonData = request.get_json()
    ma_giang_vien = jsonData['ma_giang_vien']
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM giang_vien WHERE ma_giang_vien=%s", (ma_giang_vien))
    mysql.connection.commit()
    return 'success'

#hoc phan
@app.route('/hoc_phan', methods=['POST'])
def them_hoc_phan():
    jsonData = request.get_json()
    ma_hoc_phan = str(uuid.uuid4())
    ten_hoc_phan = jsonData['ten_hoc_phan']

      
    cur = mysql.connection.cursor()

    cur.execute("INSERT INTO hoc_phan (ma_hoc_phan, ten_hoc_phan) VALUES (%s, %s)", (ma_hoc_phan, ten_hoc_phan))
    mysql.connection.commit()

    return 'Success'

@app.route('/hoc_phan', methods=['PUT'])
def sua_hoc_phan():
    jsonData = request.get_json()
    ma_hoc_phan = jsonData['ma_hoc_phan']
    ten_hoc_phan = jsonData['ten_hoc_phan']

    cur = mysql.connection.cursor()
    cur.execute("""
               UPDATE hoc_phan
               SET ten_hoc_phan=%s
               WHERE ma_hoc_phan=%s
            """, (ten_hoc_phan, ma_hoc_phan))
    mysql.connection.commit()
    return 'success'

@app.route('/hoc_phan', methods=['GET'])
def get_hoc_phan():  
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM hoc_phan")
    data = cur.fetchall()
    cur.close()

    return jsonify(data)


@app.route('/hoc_phan', methods=['DELETE'])
def xoa_hoc_phan():  
    jsonData = request.get_json()
    ma_hoc_phan = jsonData['ma_hoc_phan']
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM hoc_phan WHERE ma_hoc_phan=%s", (ma_hoc_phan))
    mysql.connection.commit()
    return 'success'

#chi tiet hoc phan
@app.route('/chi_tiet_hoc_phan', methods=['POST'])
def them_chi_tiet_hoc_phan():
    jsonData = request.get_json()
    ma_chi_tiet = str(uuid.uuid4())
    ma_hoc_phan = jsonData['ma_hoc_phan']
    ma_sinh_vien = jsonData['ma_sinh_vien']
    ma_giang_vien = jsonData['ma_giang_vien']
    diem = jsonData['diem']

      
    cur = mysql.connection.cursor()

    cur.execute("INSERT INTO chi_tiet_hoc_phan (ma_chi_tiet, ma_hoc_phan, ma_sinh_vien, ma_giang_vien, diem) VALUES (%s, %s)", (ma_chi_tiet, ma_hoc_phan, ma_sinh_vien, ma_giang_vien, diem))
    mysql.connection.commit()

    return 'Success'

@app.route('/chi_tiet_hoc_phan', methods=['PUT'])
def sua_chi_tiet_hoc_phan():
    jsonData = request.get_json()
    ma_chi_tiet = jsonData['ma_chi_tiet']
    ma_hoc_phan = jsonData['ma_hoc_phan']
    ma_sinh_vien = jsonData['ma_sinh_vien']
    ma_giang_vien = jsonData['ma_giang_vien']
    diem = jsonData['diem']

    cur = mysql.connection.cursor()
    cur.execute("""
               UPDATE chi_tiet_hoc_phan
               SET ma_hoc_phan=%s, ma_sinh_vien=%s, ma_giang_vien=%s, diem=%s,
               WHERE ma_chi_tiet=%s
            """, (ma_hoc_phan, ma_sinh_vien, ma_giang_vien, diem, ma_chi_tiet))
    mysql.connection.commit()
    return 'success'

@app.route('/chi_tiet_hoc_phan', methods=['GET'])
def get_chi_tiet_hoc_phan():  
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM chi_tiet_hoc_phan")
    data = cur.fetchall()
    cur.close()

    return jsonify(data)


@app.route('/chi_tiet_hoc_phan', methods=['DELETE'])
def xoa_chi_tiet_hoc_phan():  
    jsonData = request.get_json()
    ma_chi_tiet = jsonData['ma_chi_tiet']
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM chi_tiet_hoc_phan WHERE ma_chi_tiet=%s", (ma_chi_tiet))
    mysql.connection.commit()
    return 'success'

if __name__ == '__main__':
    app.run(debug=True)

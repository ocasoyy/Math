# Test

# Setting
import sys
import os
sys.path.append(os.getcwd())
from config import *
from models import *
from keras.preprocessing.image import ImageDataGenerator

import pymysql

# MySQL Connection 연결
conn = pymysql.connect(host='ec2-52-34-245-98.us-west-2.compute.amazonaws.com',
                       user='pmauser', password='gongmo2018',
                       db='PhoneInfo', charset='utf8')

cursor = conn.cursor()

# SQL문 실행
sql = "select * from PhoneInfo"
cursor.execute(sql)
cursor.execute("SHOW TABLES")

# 데이타 Fetch
rows = cursor.fetchall()
print(rows)

# conn.commit()

# DB 연결 닫기
conn.close()






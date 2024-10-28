import pymysql
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_DB_IP = os.getenv('DB_HOST_IP')
SECRET_DB_PW = os.getenv('DB_PASSWORD')
conn = pymysql.connect(
    host=SECRET_DB_IP,
    port=3306,
    user='root',
    password=SECRET_DB_PW,
    db='PMS',
    #charset='utf8mb4'
)
cur = conn.cursor(pymysql.cursors.DictCursor)
# 테스트 로직 시작 (이 구간 안에 복사 및 붙여 넣기하여 테스트)


# 테스트 로직 끝

# cur.execute("select * from student;")
# result = cur.fetchall()
# print(result)

# cur.execute("select * from dept;")
# result = cur.fetchall()
# print(result)

# cur.execute("select * from project;")
# result = cur.fetchall()
# print(result)

conn.close()

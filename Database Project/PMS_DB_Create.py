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
    charset='utf8mb4'
)

cur = conn.cursor(pymysql.cursors.DictCursor)
cur.execute('CREATE DATABASE PMS DEFAULT CHARACTER SET utf8mb4')
conn.commit()
conn.close()

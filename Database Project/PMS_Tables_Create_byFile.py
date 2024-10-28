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
    charset='utf8mb4'
)

try:
    with conn.cursor() as cur:
        with open('PMS_Tables_Define.sql', 'r', encoding='utf-8') as f:
            sql_file = f.read()
        
        sql_commands = sql_file.split(';')

        for command in sql_commands:
            command = command.strip()

            if command:
                cur.execute(command)
		
        conn.commit()

finally:
    conn.close()

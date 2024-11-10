"""                                                          
   CodeCraft PMS Project                             
                                                                              
   파일명   : mysql_connection.py                                                          
   생성자   : 김창환                                
                                                                              
   생성일   : 2024/10/14
   업데이트 : 2024/11/10
                                                                             
   설명     : API와 DB를 연결하는 기능 정의
"""

import pymysql
from dotenv import load_dotenv
import os

# MySQL 서버에 로그인하고 PMS DB에 접속하는 함수
def db_connect():
    load_dotenv()
    password = os.getenv('DB_PASSWORD')

    connection = pymysql.connect(
        host='192.168.50.84',
        user='root',
        password=password,
        charset='utf8mb4',
        database='PMS'
    )
    return connection

# MySQL 서버에 로그인하여 접속하는 함수
# DML 작업을 수행할 DB 대상을 지정하지 않으며, 테이블이 아닌 DB 자체를 생성하거나 삭제하는 등의 경우에 사용한다
def db_root_connect():
    load_dotenv()
    password = os.getenv('DB_PASSWORD')

    connection = pymysql.connect(
        host='192.168.50.84',
        user='root',
        password=password,
        charset='utf8mb4'
    )
    return connection

# db_session = db_connect()

# try: # DB에 접속해 테이블 리스트 출력
#     with db_session.cursor() as cursor:
#         cursor.execute("SHOW DATABASES")
#         databases = cursor.fetchall()
#         print("Databases:")
#         for db in databases:
#             print(db[0])
# finally:
#     db_session.close()

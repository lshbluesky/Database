"""
    CodeCraft PMS Project
    파일명 : PMS_DB_Manage.py
    마지막 수정 날짜 : 2025/02/01
"""

import pymysql
from mysql_connection import *

# PMS DB를 생성하는 함수
def create_pms_db():
    connection = db_root_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute('CREATE DATABASE PMS DEFAULT CHARACTER SET utf8mb4')
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

# PMS DB를 삭제하는 함수
# PMS DB 안에 정의되어 있는 모든 테이블과 데이터가 삭제되므로 주의하여 사용
def drop_pms_db():
    connection = db_root_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute('DROP DATABASE PMS')
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

# PMS DB를 삭제하고 다시 생성하는 함수
def recreate_pms_db():
    connection = db_root_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute('DROP DATABASE PMS')
        connection.commit()
        cur.execute('CREATE DATABASE PMS DEFAULT CHARACTER SET utf8mb4')
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

# SQL 파일을 읽어서 PMS DB에 테이블을 생성하고 관계 및 제약조건 설정, 학과 정보를 입력하는 함수
# 주의사항 : PMS DB가 삭제된 상태에서 실행해야 한다 (SQL 파일 안에 PMS DB 생성문이 포함되어 있기 때문)
def create_pms_db_byFile():
    conn = db_root_connect()

    try:
        with conn.cursor() as cur:
            with open('PMS_Tables_Define.sql', 'r', encoding='utf-8') as f:
                sql_file = f.read()

            sql_commands = sql_file.split(';')

            for command in sql_commands:
                command = command.strip()

                if command:
                    cur.execute(command)

            with open('PMS_PLSQL_Define.sql', 'r', encoding='utf-8') as f:
                plsql_file = f.read()

            plsql_commands = plsql_file.split('$$')

            for command in plsql_commands:
                command = command.strip()

                if command:
                    cur.execute(command)

            conn.commit()
    except Exception as e:
        print(f"Error [create_pms_db_byFile] : {e}")
        cur.execute('DROP DATABASE PMS')
        conn.commit()
        return e
    finally:
        conn.close()

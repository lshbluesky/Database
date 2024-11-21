"""
    CodeCraft PMS Project
    파일명 : account_DB.py
    마지막 수정 날짜 : 2024/11/21
"""

import pymysql
from mysql_connection import db_connect
from account import *

# 사용자(학생) 생성 함수
def insert_user(payload, Token):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    try:
        add_student = """
        INSERT INTO student(s_no, s_id, s_pw, s_name, s_email, s_token, dno)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        # 매개변수 바인딩 방식으로 안전하게 값 전달
        cur.execute(add_student, (payload.univ_id, payload.id, payload.pw, payload.name, payload.email, Token, payload.department))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [insert_user] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 사용자(학생) 로그인 정보 확인 함수
def validate_user(id, pw):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        # 매개 변수로 받은 ID를 통하여 해당 ID, PW 조회
        cur.execute("SELECT s_id, s_pw FROM student WHERE s_id = %s", (id,))
        row = cur.fetchone()

        # 만약, 해당 ID 가 존재하고, 로그인 정보가 일치하다면 True 반환
        if row and id == row['s_id'] and pw == row['s_pw']:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error [validate_user] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 사용자(학생) 로그인 성공 후 토큰(세션)을 DB에 저장하는 함수
# 로그인 정보가 일치하여 로그인에 성공하면, 로그인한 학생의 ID와 생성된 토큰을 매개 변수로 받아서 해당 사용자의 현재 세션을 유지하기 위한 토큰을 저장한다
def save_signin_user_token(id, Token):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("UPDATE student SET s_token = %s WHERE s_id = %s", (Token, id))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [save_signin_user_token] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 사용자(학생) 로그아웃 함수
def signout_user(Token):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("UPDATE student SET s_token = NULL WHERE s_token = %s", (Token,))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [signout_user] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 사용자(학생) 삭제 함수
def delete_user(id):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("DELETE FROM student WHERE s_id = %s", (id,))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [delete_user] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 사용자(학생) 토큰 확인 함수
def validate_user_token(id, Token):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT s_token FROM student WHERE s_id = %s", (id,))
        stored_token = cur.fetchone()

        # 매개 변수로 받은 토큰과 DB에 저장된 해당 학생의 토큰 값이 일치하다면 True를 반환
        if Token == stored_token['s_token']:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error [validate_user_token] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

"""
    CodeCraft PMS Project
    파일명 : account_DB.py
    생성자 : 이상훈
    마지막 수정 날짜 : 2024/10/30
"""

import pymysql
import mysql_connection
import account

# 사용자(학생) 생성 함수
def insert_user(payload, Token):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        add_student = """
        INSERT INTO student(s_no, s_id, s_pw, s_name, s_email, s_token, dno)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(add_student, (payload.univ_id, payload.id, payload.pw, payload.name, payload.email, Token, payload.department))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

# 사용자(학생) 로그인 정보 확인 함수
def validate_user(id, pw):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        # 매개 변수로 받은 ID를 통하여 해당 ID, PW 조회
        cur.execute("SELECT s_id, s_pw FROM student WHERE id = %s", (id,))
        row = cur.fetchone()

        # 만약, 해당 ID 가 존재하고, 로그인 정보가 일치하다면 True 반환
        if row and id == row['s_id'] and pw == row['s_pw']:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error during user validation: {e}")
        return False
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
        return False
    finally:
        cur.close()
        connection.close()

# 사용자(학생) 토큰 확인 함수
def validate_user_token(id, Token):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT s_token FROM student WHERE id = %s", (id,))
        stored_token = cur.fetchone()

        # 매개 변수로 받은 토큰과 DB에 저장된 해당 학생의 토큰 값이 일치하다면 True를 반환
        if Token == stored_token['s_token']:
            return True
        else:
            return False
    except Exception as e:
        return False
    finally:
        cur.close()
        connection.close()

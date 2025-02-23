"""
    CodeCraft PMS Project
    파일명 : subject_DB.py
    마지막 수정 날짜 : 2025/02/17
"""

import pymysql
from mysql_connection import db_connect

# 모든 과목 목록을 조회하는 함수
# 매개 변수는 없으며, 모든 학과의 모든 과목을 조회한다
def fetch_subject_list():
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT /*+ INDEX(subject idx_subject_dno_subj_name) */ subj_no, subj_name FROM subject ORDER BY dno, subj_name")
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Error [fetch_subject_list] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 특정 학과의 모든 과목 목록을 조회하는 함수
# 학과 번호를 매개 변수로 받는다
def fetch_subject_list_of_dept(dno):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT subj_no, subj_name FROM subject WHERE dno = %s ORDER BY subj_name", dno)
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Error [fetch_subject_list] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 현재 사용자 소속 학과의 모든 과목 목록을 조회하는 함수
# 현재 사용자의 학번을 매개 변수로 받는다
def fetch_subject_list_of_student(univ_id):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT subj_no, subj_name FROM subject WHERE dno = (SELECT dno FROM student WHERE s_no = %s) ORDER BY subj_name", univ_id)
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Error [fetch_subject_list] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

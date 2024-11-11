"""
    CodeCraft PMS Project
    파일명 : grade_DB.py
    마지막 수정 날짜 : 2024/11/11
"""

import pymysql
from mysql_connection import db_connect

# 관리자(교수)가 학생의 프로젝트 평가 점수를 등록(부여)하거나 수정하는 함수
# 프로젝트 번호, 학번, 성적을 매개 변수로 받는다
# 주의사항 : 성적은 문자열('A+', 'A', 'B+', 'B', 'C+', 'C', 'D+', 'D', 'F')로 입력받아야 한다
def assign_grade(pid, univ_id, grade):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("UPDATE project_user SET grade = %s WHERE p_no = %s AND s_no = %s", (grade, pid, univ_id))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

# 관리자(교수)가 학생의 프로젝트 평가 점수를 삭제하는 함수
# 프로젝트 번호와 학번을 매개 변수로 받는다
def delete_grade(pid, univ_id):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("UPDATE project_user SET grade = NULL WHERE p_no = %s AND s_no = %s", (pid, univ_id))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

# 어떤 학생의 특정 프로젝트 평가 점수를 한 개 조회하여 반환하는 함수
# 프로젝트 번호와 학번을 매개 변수로 받는다
def fetch_one_grade(pid, univ_id):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT * FROM project_user WHERE p_no = %s AND s_no = %s", (pid, univ_id))
        row = cur.fetchone()
        return row['grade']
    except Exception as e:
        return False
    finally:
        cur.close()
        connection.close()

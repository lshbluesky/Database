"""
    CodeCraft PMS Project
    파일명 : grade_DB.py
    마지막 수정 날짜 : 2025/01/23
"""

import pymysql
from mysql_connection import db_connect

# 관리자(교수)가 학생의 프로젝트 평가(성적) 점수를 등록(부여)하거나 수정하는 함수
# 프로젝트 번호, 학번, 성적, 평가 코멘트를 매개 변수로 받는다
# 주의사항 : 성적은 문자열('A+', 'A', 'B+', 'B', 'C+', 'C', 'D+', 'D', 'F')로 입력받아야 한다
def assign_grade(pid, univ_id, grade, comment):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("UPDATE project_user SET grade = %s, comment = %s WHERE p_no = %s AND s_no = %s", (grade, comment, pid, univ_id))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [assign_grade] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 관리자(교수)가 학생의 프로젝트 평가(성적) 점수를 삭제하는 함수
# 프로젝트 번호와 학번을 매개 변수로 받는다
def delete_grade(pid, univ_id):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("UPDATE project_user SET grade = NULL, comment = NULL WHERE p_no = %s AND s_no = %s", (pid, univ_id))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [delete_grade] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 어떤 학생의 특정 프로젝트 평가(성적) 점수와 평가 코멘트를 조회하여 반환하는 함수
# 프로젝트 번호와 학번을 매개 변수로 받는다
def fetch_one_grade(pid, univ_id):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT grade, comment FROM project_user WHERE p_no = %s AND s_no = %s", (pid, univ_id))
        result = cur.fetchone()
        return result
    except Exception as e:
        print(f"Error [fetch_one_grade] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 어떤 학생이 참여하고 있는 모든 프로젝트의 평가(성적) 점수를 조회하는 함수
# 학번을 매개 변수로 받는다
def fetch_grade_by_student(univ_id):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        fetch_grade_by_student = """
        SELECT p.p_no, p.p_name, s.s_no, s.s_name, u.grade, u.comment
        FROM student s, project p, project_user u
        WHERE s.s_no = u.s_no AND p.p_no = u.p_no AND u.s_no = %s
        """
        cur.execute(fetch_grade_by_student, (univ_id,))
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Error [fetch_grade_by_student] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 특정 프로젝트에 속한 모든 팀원의 평가(성적) 점수를 조회하는 함수
# 프로젝트 번호를 매개 변수로 받는다
def fetch_grade_by_project(pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        fetch_grade_by_project = """
        SELECT p.p_no, p.p_name, s.s_no, s.s_name, u.grade, u.comment
        FROM student s, project p, project_user u
        WHERE s.s_no = u.s_no AND p.p_no = u.p_no AND u.p_no = %s
        """
        cur.execute(fetch_grade_by_project, (pid,))
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Error [fetch_grade_by_project] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

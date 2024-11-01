"""
    CodeCraft PMS Project
    파일명 : project_DB.py
    마지막 수정 날짜 : 2024/11/01
"""

import pymysql
from mysql_connection import db_connect
import project

# 프로젝트 생성 함수
def init_project(payload):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    # payload.pperiod의 값을 split() 메소드로 쪼개기
    total_period = payload.pperiod
    p_startD, p_endD = total_period.split('-')

    try:
        add_project = """
        INSERT INTO project(p_name, p_content, p_method, p_memcount, p_start, p_end, dno)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(add_project, (payload.pname, payload.pdetails, payload.pmm, payload.psize, p_startD, p_endD, 10))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

# 프로젝트 수정 함수
def edit_project(payload):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    # payload.pperiod의 값을 split() 메소드로 쪼개기
    total_period = payload.pperiod
    p_startD, p_endD = total_period.split('-')
    
    try:
        edit_project = """
        UPDATE project
        SET p_name = %s,
            p_content = %s,
            p_method = %s,
            p_memcount = %s,
            p_start = %s,
            p_end = %s,
            dno = %s
        WHERE p_no = %s
        """
        cur.execute(edit_project, (payload.pname, payload.pdetails, payload.pmm, payload.psize, p_startD, p_endD, 10, payload.pid))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

# 프로젝트 정보 조회 함수
def fetch_project_info(univ_id):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        fetch_project_info = """
        SELECT p.p_no, p.p_name, p.p_content, p.p_method, p.p_memcount, p.p_start, p.p_end
        FROM project p, project_user u
        WHERE p.p_no = u.p_no
        AND u.s_no = %s
        """
        cur.execute(fetch_project_info, (univ_id,))
        result = cur.fetchall()
        return result
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

# 프로젝트 삭제 함수
def delete_project(pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        # 프로젝트 테이블에서 매개 변수로 받은 프로젝트 삭제
        cur.execute("DELETE FROM project WHERE p_no = %s", (pid,))
        connection.commit()

        # 프로젝트가 삭제되었으므로, 해당 프로젝트에 참여하고 있었던 모든 학생은 자동으로 프로젝트 참여 해제
        cur.execute("DELETE FROM project_user WHERE p_no = %s", (pid,))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

# 프로젝트 사용자 추가(팀원 초대) 함수
# 주의사항 : 초대하려는 사용자(학생)는 회원가입이 이미 완료되어 있어야 한다
def add_project_user(pid, univ_id, role):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        add_project_user = """
        INSERT INTO project_user(p_no, s_no, permission, role, grade)
        VALUES (%s, %s, 0, %s, NULL)
        """
        cur.execute(add_project_user, (pid, univ_id, role))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

# 프로젝트 사용자 수정(팀원 정보 수정) 함수
def edit_project_user(id, name, email, univ_id, pid, role):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        # 학생 테이블에서 학번으로 수정할 학생을 선택하고 아이디, 이름, 이메일을 수정
        cur.execute("UPDATE student SET s_id = %s, s_name = %s, s_email = %s WHERE s_no = %s", (id, name, email, univ_id))
        connection.commit()

        # 프로젝트 참여 테이블에서 프로젝트 번호와 학번으로 수정할 팀원을 선택하고 역할을 수정
        cur.execute("UPDATE project_user SET role = %s WHERE p_no = %s AND s_no = %s", (role, pid, univ_id))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

# 프로젝트 사용자 삭제(팀원 퇴출) 함수
def delete_project_user(pid, univ_id):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("DELETE FROM project_user WHERE p_no = %s AND s_no = %s", (pid, univ_id))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

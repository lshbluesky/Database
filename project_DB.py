"""
    CodeCraft PMS Project
    파일명 : project_DB.py
    마지막 수정 날짜 : 2024/11/24
"""

import pymysql
from mysql_connection import db_connect
from project import *

# 프로젝트 생성 함수
# 생성하려는 프로젝트의 내용과 프로젝트 고유 번호를 매개 변수로 받는다
def init_project(payload, pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    # payload.pperiod의 값을 split() 메소드로 쪼개기
    total_period = payload.pperiod
    p_startD, p_endD = total_period.split('-')

    try:
        add_project = """
        INSERT INTO project(p_no, p_name, p_content, p_method, p_memcount, p_start, p_end, dno)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(add_project, (pid, payload.pname, payload.pdetails, payload.pmm, payload.psize, p_startD, p_endD, 10))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [init_project] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 프로젝트 수정 함수
# 수정하려는 프로젝트의 내용과 프로젝트 고유 번호를 매개 변수로 받는다 (pid는 payload에 포함되어 있음)
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
        print(f"Error [edit_project] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 프로젝트 정보 조회 함수
# 학생의 학번을 매개 변수로 받아서 해당 학생이 참여하고 있는 모든 프로젝트를 조회한다
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
        print(f"Error [fetch_project_info] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 프로젝트 삭제 함수
# 삭제하려는 프로젝트의 번호를 매개 변수로 받는다
def delete_project(pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        # 매개 변수로 받은 pid 값을 가진 프로젝트가 존재하는지 확인하기 위해 COUNT 함수를 사용
        cur.execute("SELECT COUNT(*) AS cnt FROM project WHERE p_no = %s", (pid,))
        result = cur.fetchone()

        # 매개 변수로 받은 pid 값을 가진 프로젝트가 존재하지 않으면 오류 메시지 출력 및 False 반환
        if result['cnt'] == 0:
            print(f"Error [delete_project] : Project UID {pid} does not exist.")
            return False
        
        # 프로젝트 테이블에서 매개 변수로 받은 프로젝트 삭제
        cur.execute("DELETE FROM project WHERE p_no = %s", (pid,))
        connection.commit()

        # 프로젝트가 삭제되었으므로, 해당 프로젝트에 참여하고 있었던 모든 학생은 자동으로 프로젝트 참여 해제
        cur.execute("DELETE FROM project_user WHERE p_no = %s", (pid,))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [delete_project] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 프로젝트 참여자 추가(팀원 초대) 함수
# 프로젝트 번호, 학번, PM 권한 여부(0/1), 역할을 매개 변수로 받는다
# 주의사항 : 초대하려는 사용자(학생)는 회원가입이 이미 완료되어 있어야 한다
def add_project_user(pid, univ_id, permission, role):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        add_project_user = """
        INSERT INTO project_user(p_no, s_no, permission, role, grade)
        VALUES (%s, %s, %s, %s, NULL)
        """
        cur.execute(add_project_user, (pid, univ_id, permission, role))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [add_project_user] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 프로젝트 참여자 수정(팀원 정보 수정) 함수
# 수정하려는 팀원의 학번, 프로젝트 번호, 역할을 매개 변수로 받는다
def edit_project_user(univ_id, pid, role):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        # 프로젝트 참여 테이블에서 프로젝트 번호와 학번으로 수정할 팀원을 선택하고 역할을 수정
        cur.execute("UPDATE project_user SET role = %s WHERE p_no = %s AND s_no = %s", (role, pid, univ_id))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [edit_project_user] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 프로젝트 참여자 삭제(팀원 퇴출) 함수
# 프로젝트 번호와 퇴출하려는 팀원의 학번을 매개 변수로 받는다
def delete_project_user(pid, univ_id):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("DELETE FROM project_user WHERE p_no = %s AND s_no = %s", (pid, univ_id))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [delete_project_user] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 프로젝트 참여자(팀원 조회) 조회 함수
# 조회하려는 팀원이 속한 프로젝트의 프로젝트 번호를 매개 변수로 받는다
def fetch_project_user(pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        # 프로젝트 참여 테이블에서 프로젝트 번호로 해당 프로젝트에 참여하고 있는 모든 팀원 조회
        cur.execute("SELECT * FROM project_user WHERE p_no = %s", (pid,))
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Error [fetch_project_user] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 프로젝트의 중요 정보를 수정할 때 사용자의 권한(PM 권한)을 확인하는 함수
# 프로젝트 번호와 학번을 매개 변수로 받는다
def validate_pm_permission(pid, univ_id):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT permission FROM project_user WHERE p_no = %s AND s_no = %s", (pid, univ_id))
        row = cur.fetchone()

        if row['permission'] == 1:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error [validate_pm_permission] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 프로젝트 고유 ID(PUID)가 데이터베이스에 존재하는지 확인
def is_uid_exists(uid):
    connection = db_connect()
    cur = connection.cursor()

    try:
        cur.execute("SELECT COUNT(*) AS count FROM project WHERE p_no = %s", (uid))
        result = cur.fetchone()
        return result[0] > 0
    except Exception as e:
        print(f"Error [is_uid_exists] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

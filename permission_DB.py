"""
    CodeCraft PMS Project
    파일명 : permission_DB.py
    마지막 수정 날짜 : 2025/01/14
"""

import pymysql
from mysql_connection import db_connect

# 팀장의 권한 정보를 추가하는 함수
# 프로젝트 번호와 학번을 매개 변수로 받는다
def add_leader_permission(pid, univ_id):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        add_leader_permission = """
        INSERT INTO permission(p_no, s_no, leader, ro, user, wbs, od, mm, ut, rs, rp, om, task, llm)
        VALUES (%s, %s, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        """
        cur.execute(add_leader_permission, (pid, univ_id))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [add_leader_permission] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 관전자 모드 사용자의 권한 정보를 추가하는 함수
# 프로젝트 번호와 학번을 매개 변수로 받는다
def add_ro_permission(pid, univ_id):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        add_ro_permission = """
        INSERT INTO permission(p_no, s_no, leader, ro, user, wbs, od, mm, ut, rs, rp, om, task, llm)
        VALUES (%s, %s, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        """
        cur.execute(add_ro_permission, (pid, univ_id))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [add_ro_permission] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 관전자 모드 사용자의 권한 정보를 추가하는 함수 Ver2 (ro 컬럼 대신에 다른 권한을 모두 읽기 전용으로 설정)
# 프로젝트 번호와 학번을 매개 변수로 받는다
def add_ro_permission2(pid, univ_id):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        add_ro_permission2 = """
        INSERT INTO permission(p_no, s_no, leader, ro, user, wbs, od, mm, ut, rs, rp, om, task, llm)
        VALUES (%s, %s, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0)
        """
        cur.execute(add_ro_permission2, (pid, univ_id))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [add_ro_permission2] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 일반적인 팀원의 기본값 권한 정보를 추가하는 함수
# 프로젝트 번호와 학번을 매개 변수로 받는다
def add_default_user_permission(pid, univ_id):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        add_default_user_permission = """
        INSERT INTO permission(p_no, s_no, leader, ro, user, wbs, od, mm, ut, rs, rp, om, task, llm)
        VALUES (%s, %s, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2)
        """
        cur.execute(add_default_user_permission, (pid, univ_id))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [add_default_user_permission] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 사용자의 권한 정보를 수동으로 추가하는 함수
# 프로젝트 번호, 학번, 12개의 권한 정보를 매개 변수로 받는다
def add_manual_permission(pid, univ_id, leader, ro, user, wbs, od, mm, ut, rs, rp, om, task, llm):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        add_manual_permission = """
        INSERT INTO permission(p_no, s_no, leader, ro, user, wbs, od, mm, ut, rs, rp, om, task, llm)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(add_manual_permission, (pid, univ_id, leader, ro, user, wbs, od, mm, ut, rs, rp, om, task, llm))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [add_manual_permission] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 사용자의 권한 정보를 수정하는 함수
# 프로젝트 번호, 학번, 12개의 권한 정보를 매개 변수로 받는다
def edit_permission(pid, univ_id, leader, ro, user, wbs, od, mm, ut, rs, rp, om, task, llm):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        edit_permission = """
        UPDATE permission
        SET leader = %s,
            ro = %s,
            user = %s,
            wbs = %s,
            od = %s,
            mm = %s,
            ut = %s,
            rs = %s,
            rp = %s,
            om = %s,
            task = %s,
            llm = %s
        WHERE p_no = %s AND s_no = %s
        """
        cur.execute(edit_permission, (leader, ro, user, wbs, od, mm, ut, rs, rp, om, task, llm, pid, univ_id))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [edit_permission] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 특정 프로젝트에서 모든 팀원의 모든 권한을 조회하는 함수
# 프로젝트 번호를 매개 변수로 받는다
def fetch_all_permissions_of_all_users(pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT * FROM permission WHERE p_no = %s", (pid,))
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Error [fetch_all_permissions_of_all_users] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 특정 프로젝트에서 특정 팀원의 모든 권한을 조회하는 함수
# 프로젝트 번호와 학번을 매개 변수로 받는다
def fetch_all_permissions_of_user(pid, univ_id):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT * FROM permission WHERE p_no = %s AND s_no = %s", (pid, univ_id))
        result = cur.fetchone()
        return result
    except Exception as e:
        print(f"Error [fetch_all_permissions_of_user] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 프로젝트의 중요 정보를 수정할 때 사용자가 팀장(리더) 권한을 보유하고 있는지 확인(검증)하는 함수
# 프로젝트 번호와 학번을 매개 변수로 받는다
def validate_leader_permission(pid, univ_id):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT leader FROM permission WHERE p_no = %s AND s_no = %s", (pid, univ_id))
        row = cur.fetchone()

        if row['leader'] == 1:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error [validate_leader_permission] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

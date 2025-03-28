"""
    CodeCraft PMS Project
    파일명 : task_DB.py
    마지막 수정 날짜 : 2025/02/21
"""

import pymysql
from mysql_connection import db_connect
from task import *

# 업무를 조회하는 함수
# 프로젝트 번호와 학번을 매개 변수로 받고, WHERE 절의 조건으로 필터링해야 한다
# 만약, 학번으로만 조회할 경우, 한 명의 사용자가 2개 이상의 프로젝트에 참여하고 있다면, 다른 프로젝트의 업무도 같이 조회될 수 있음
def fetch_task_info(pid, univ_id):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        load_work = "SELECT w_no, w_name, w_person, w_start, w_end, w_checked, s_no FROM work WHERE p_no = %s AND s_no = %s"
        cur.execute(load_work, (pid, univ_id))
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Error [fetch_task_info] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 특정 프로젝트의 모든 업무를 조회하는 함수
# 프로젝트 번호를 매개 변수로 받는다
def fetch_all_task_info(pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT * FROM work WHERE p_no = %s", (pid,))
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Error [fetch_all_task_info] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 업무를 추가하는 함수
# 추가하려는 업무의 내용, 프로젝트 번호, 학번을 매개 변수로 받는다
# 업무를 추가할 때 프로젝트 번호와 학번도 매개 변수로 받아야 한다 (work 테이블의 p_no, s_no 컬럼 모두 NOT NULL)
def add_task_info(tname, tperson, tstart, tend, pid, univ_id):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        add_work = """
        INSERT INTO work(w_name, w_person, w_start, w_end, w_checked, p_no, s_no)
        VALUES (%s, %s, %s, %s, 0, %s, %s)
        """
        cur.execute(add_work, (tname, tperson, tstart, tend, pid, univ_id))
        connection.commit()
        
        # ORDERY BY 절을 이용하여 업무 번호를 내림차순으로 조회하고,
        # 그 첫 번째 행만 가져온 후에 방금 추가한 업무의 업무 번호를 조회하여 반환
        cur.execute("SELECT /*+ INDEX(work idx_work_pno_sno_wno) */ * FROM work WHERE p_no = %s AND s_no = %s ORDER BY w_no DESC", (pid, univ_id))
        row = cur.fetchone()
        return row['w_no']
    except Exception as e:
        connection.rollback()
        print(f"Error [add_task_info] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 업무를 수정하는 함수
# 수정하려는 업무의 내용과 업무 번호를 매개 변수로 받는다
# 수정할 업무에 해당하는 업무 번호도 매개 변수로 같이 받아야 하며, 그렇지 않으면 모든 업무가 같은 내용으로 수정되는 문제가 발생
def update_task_info(tname, tperson, tstart, tend, tfinish, univ_id, w_no):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        edit_work = """
        UPDATE work
        SET w_name = %s,
            w_person = %s,
            w_start = %s,
            w_end = %s,
            w_checked = %s,
            s_no = %s
        WHERE w_no = %s
        """
        cur.execute(edit_work, (tname, tperson, tstart, tend, tfinish, univ_id, w_no))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [update_task_info]: {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 업무를 삭제하는 함수
# 삭제하려는 업무의 업무 번호를 매개 변수로 받는다
def delete_task_info(w_no):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT COUNT(*) AS cnt FROM work WHERE w_no = %s", (w_no,))
        result = cur.fetchone()

        if result['cnt'] == 0:
            print(f"Error [delete_task_info] : Work number {w_no} does not exist.")
            return False
        
        # 업무 번호로 해당 업무 삭제
        cur.execute("DELETE FROM work WHERE w_no = %s", (w_no,))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [delete_task_info] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

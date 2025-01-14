"""
    CodeCraft PMS Project
    파일명 : permission_DB.py
    마지막 수정 날짜 : 2025/01/14
"""

import pymysql
from mysql_connection import db_connect

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

"""
    CodeCraft PMS Project
    파일명 : wbs_DB.py
    마지막 수정 날짜 : 2025/01/04
"""

import pymysql
from mysql_connection import db_connect

# 진척도(WBS) 항목 여러 개 추가 및 기존 데이터 삭제 후 재삽입
def add_multiple_wbs(wbs_data, pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        # 새로운 데이터 추가
        wbs_data_with_pid = [item + [pid] for item in wbs_data]
        add_multiple_wbs_query = """
        INSERT INTO progress (group1, group2, group3, group4, work, output_file, manager, note, ratio, start_date, end_date, group1no, group2no, group3no, group4no, p_no)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.executemany(add_multiple_wbs_query, wbs_data_with_pid)
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [add_multiple_wbs] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 특정 프로젝트의 모든 WBS 항목 조회
def fetch_all_wbs(pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT * FROM progress WHERE p_no = %s ORDER BY group1no, group2no, group3no, group4no", (pid,))
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Error [fetch_all_wbs] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 특정 프로젝트의 모든 WBS 항목 삭제
def delete_all_wbs(pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("DELETE FROM progress WHERE p_no = %s", (pid,))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [delete_all_wbs] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

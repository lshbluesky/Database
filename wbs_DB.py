"""
    CodeCraft PMS Project
    파일명 : wbs_DB.py
    마지막 수정 날짜 : 2025/01/16
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
        cur.execute("SELECT COUNT(*) AS cnt FROM progress WHERE p_no = %s", (pid,))
        result = cur.fetchone()

        if result['cnt'] == 0:
            print(f"Error [delete_all_wbs] : Progress data does not exist in Project UID {pid}.")
            return False
        
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

# 특정 프로젝트의 WBS에서 대분류 항목별로 진척률의 평균을 조회하는 함수
# 프로젝트 번호를 매개 변수로 받는다
def fetch_wbs_ratio(pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        fetch_wbs_ratio = """
        SELECT group1no,
            CASE group1no
                WHEN 1 THEN '계획'
                WHEN 2 THEN '분석'
                WHEN 3 THEN '설계'
                WHEN 4 THEN '구현'
                WHEN 5 THEN '테스트'
                WHEN 6 THEN '유지보수' END AS group1,
            ROUND(AVG(ratio)) AS ratio
        FROM progress
        WHERE p_no = %s
        GROUP BY group1no
        """
        cur.execute(fetch_wbs_ratio, (pid,))
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Error [fetch_wbs_ratio] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

"""
    CodeCraft PMS Project
    파일명 : wbs_DB.py
    마지막 수정 날짜 : 2024/11/08
"""

import pymysql
from mysql_connection import db_connect

# 진척도(WBS) 항목 한 개를 추가하는 함수
# 추가하려는 진척도 항목 한 개의 내용과 프로젝트 번호를 매개 변수로 받는다
def add_one_wbs(group1, group2, group3, work, output_file, manager, note, ratio, start_date, end_date, group1no, group2no, group3no, pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        add_one_progress = """
        INSERT INTO progress (group1, group2, group3, work, output_file, manager, note, ratio, start_date, end_date, group1no, group2no, group3no, p_no)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(add_one_progress, (group1, group2, group3, work, output_file, manager, note, ratio, start_date, end_date, group1no, group2no, group3no, pid))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

# 진척도(WBS) 항목 한 개를 수정하는 함수
# 수정하려는 진척도 항목의 진척도 번호를 매개 변수로 받는다
def edit_one_wbs(group1, group2, group3, work, output_file, manager, note, ratio, start_date, end_date, group1no, group2no, group3no, progress_no):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        edit_one_progress = """
        UPDATE progress
        SET group1 = %s,
            group2 = %s,
            group3 = %s,
            work = %s,
            output_file = %s,
            manager = %s,
            note = %s,
            ratio = %s,
            start_date = %s,
            end_date = %s,
            group1no = %s,
            group2no = %s,
            group3no = %s
        WHERE progress_no = %s
        """
        cur.execute(edit_one_progress, (group1, group2, group3, work, output_file, manager, note, ratio, start_date, end_date, group1no, group2no, group3no, progress_no))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

# 진척도(WBS) 항목 한 개를 삭제하는 함수
# 삭제하려는 진척도 항목의 진척도 번호를 매개 변수로 받는다
def delete_one_wbs(progress_no):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("DELETE FROM progress WHERE progress_no = %s", (progress_no,))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

# 진척도(WBS)를 모두 조회하는 함수
def fetch_all_wbs(pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT * FROM progress WHERE p_no = %s ORDER BY group1no ASC, group2no ASC, group3no ASC", (pid,))
        result = cur.fetchall()
        return result
    except Exception as e:
        return False
    finally:
        cur.close()
        connection.close()

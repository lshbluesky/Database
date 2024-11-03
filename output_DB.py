"""
    CodeCraft PMS Project
    파일명 : output_DB.py
    마지막 수정 날짜 : 2024/11/03
"""

import pymysql
from mysql_connection import db_connect
from output import *

# ------------------------------ 프로젝트 개요서 ------------------------------ #
# 프로젝트 개요서 간단본을 추가하는 함수
# 프로젝트 개요서 상세본을 추가하는 함수

# ------------------------------ 회의록 ------------------------------ #
# 회의록을 추가하는 함수
# 추가하려는 회의록의 내용과 프로젝트 번호를 매개 변수로 받는다
def add_meeting_minutes(main_agenda, date_time, location, participants, responsible_person, meeting_content, meeting_outcome, pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        add_doc_meeting = """
        INSERT INTO doc_meeting(doc_m_title, doc_m_date, doc_m_loc, doc_m_member, doc_m_manager, doc_m_content, doc_m_result, p_no)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(add_doc_meeting, (main_agenda, date_time, location, participants, responsible_person, meeting_content, meeting_outcome, pid))
        connection.commit()

        cur.execute("SELECT * FROM doc_meeting WHERE p_no = %s ORDER BY doc_m_no DESC", (pid,))
        row = cur.fetchone()
        return row['doc_m_no']
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

# 회의록을 수정하는 함수
# 수정하려는 회의록의 내용과 산출물 번호를 매개 변수로 받는다
def edit_meeting_minutes(main_agenda, date_time, location, participants, responsible_person, meeting_content, meeting_outcome, doc_m_no):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        edit_doc_meeting = """
        UPDATE doc_meeting
        SET doc_m_title = %s,
            doc_m_date = %s,
            doc_m_loc = %s,
            doc_m_member = %s,
            doc_m_manager = %s,
            doc_m_content = %s,
            doc_m_result = %s
        WHERE doc_m_no = %s
        """
        cur.execute(edit_doc_meeting, (main_agenda, date_time, location, participants, responsible_person, meeting_content, meeting_outcome, doc_m_no))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

# 회의록을 삭제하는 함수
# 삭제하려는 회의록의 산출물 번호를 매개 변수로 받는다
def delete_meeting_minutes(doc_m_no):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("DELETE FROM doc_meeting WHERE doc_m_no = %s", (doc_m_no,))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

# 회의록을 모두 조회하는 함수
# 프로젝트 번호를 매개 변수로 받는다
def fetch_all_meeting_minutes(pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT * FROM doc_meeting WHERE p_no = %s", (pid,))
        result = cur.fetchall()
        return result
    except Exception as e:
        return False
    finally:
        cur.close()
        connection.close()

# 회의록을 하나만 조회하는 함수
# 조회하려는 회의록의 산출물 번호를 매개 변수로 받는다
def fetch_one_meeting_minutes(doc_m_no):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT * FROM doc_meeting WHERE doc_m_no = %s", (doc_m_no,))
        result = cur.fetchone()
        return result
    except Exception as e:
        return False
    finally:
        cur.close()
        connection.close()

# ------------------------------ 요구사항 명세서 ------------------------------ #
# 요구사항 명세서를 추가하는 함수
# 추가하려는 요구사항 명세서의 내용과 프로젝트 번호를 매개 변수로 받는다
def add_reqspec(feature_name, description, priority, non_functional_requirement_name, non_functional_description, non_functional_priority, system_item, system_description, pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        add_doc_require = """
        INSERT INTO doc_require(doc_r_f_name, doc_r_f_content, doc_r_nf_name, doc_r_nf_content, doc_r_s_name, doc_r_s_content, doc_r_date, p_no)
        VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)
        """
        cur.execute(add_doc_require, (feature_name, description, non_functional_requirement_name, non_functional_description, system_item, system_description, pid))
        connection.commit()

        cur.execute("SELECT * FROM doc_require WHERE p_no = %s ORDER BY doc_r_no DESC", (pid,))
        row = cur.fetchone()
        return row['doc_r_no']
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

# 요구사항 명세서를 수정하는 함수
# 수정하려는 요구사항 명세서의 내용과 산출물 번호를 매개 변수로 받는다
def edit_reqspec(feature_name, description, non_functional_requirement_name, non_functional_description, system_item, system_description, doc_r_no):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        edit_doc_require = """
        UPDATE doc_require
        SET doc_r_f_name = %s,
            doc_r_f_content = %s,
            doc_r_nf_name = %s,
            doc_r_nf_content = %s,
            doc_r_s_name = %s,
            doc_r_s_content = %s
        WHERE doc_r_no = %s
        """
        cur.execute(edit_doc_require, (feature_name, description, non_functional_requirement_name, non_functional_description, system_item, system_description, doc_r_no))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

# 요구사항 명세서를 삭제하는 함수
# 삭제하려는 요구사항 명세서의 산출물 번호를 매개 변수로 받는다
def delete_reqspec(doc_r_no):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("DELETE FROM doc_require WHERE doc_r_no = %s", (doc_r_no,))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

# 요구사항 명세서를 모두 조회하는 함수
# 프로젝트 번호를 매개 변수로 받는다
def fetch_all_reqspec(pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT * FROM doc_require WHERE p_no = %s", (pid,))
        result = cur.fetchall()
        return result
    except Exception as e:
        return False
    finally:
        cur.close()
        connection.close()

# 요구사항 명세서를 하나만 조회하는 함수
# 조회하려는 요구사항 명세서의 산출물 번호를 매개 변수로 받는다
def fetch_one_reqspec(doc_r_no):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT * FROM doc_require WHERE doc_r_no = %s", (doc_r_no,))
        result = cur.fetchone()
        return result
    except Exception as e:
        return False
    finally:
        cur.close()
        connection.close()

# ------------------------------ 테스트 케이스 ------------------------------ #
# 테스트 케이스를 추가하는 함수
# 테스트 케이스를 수정하는 함수
# 테스트 케이스를 삭제하는 함수
# 테스트 케이스를 모두 조회하는 함수
# 테스트 케이스를 하나만 조회하는 함수

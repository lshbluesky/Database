"""
    CodeCraft PMS Project
    파일명 : output_DB.py
    마지막 수정 날짜 : 2024/11/14
"""

import pymysql
from mysql_connection import db_connect
from output import *

# ------------------------------ 프로젝트 개요서 ------------------------------ #
# 프로젝트 개요서 간단본을 추가하는 함수
# 추가하려는 프로젝트 개요서 간단본의 내용과 프로젝트 번호를 매개 변수로 받는다
def add_summary_document(pname, pteam, psummary, pstart, pend, prange, poutcomes, pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        add_doc_summary = """
        INSERT INTO doc_summary(doc_s_name, doc_s_team, doc_s_overview, doc_s_start, doc_s_end, doc_s_range, doc_s_outcomes, doc_s_date, p_no)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), %s)
        """
        cur.execute(add_doc_summary, (pname, pteam, psummary, pstart, pend, prange, poutcomes, pid))
        connection.commit()

        cur.execute("SELECT * FROM doc_summary WHERE p_no = %s ORDER BY doc_s_no DESC", (pid,))
        row = cur.fetchone()
        return row['doc_s_no']
    except Exception as e:
        connection.rollback()
        print(f"Error [add_summary_document] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 프로젝트 개요서 간단본을 수정하는 함수
# 수정하려는 프로젝트 개요서 간단본의 내용과 산출물 번호를 매개 변수로 받는다
def edit_summary_document(pname, pteam, psummary, pstart, pend, prange, poutcomes, doc_s_no):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        edit_doc_summary = """
        UPDATE doc_summary
        SET doc_s_name = %s,
            doc_s_team = %s,
            doc_s_overview = %s,
            doc_s_start = %s,
            doc_s_end = %s,
            doc_s_range = %s,
            doc_s_outcomes = %s
        WHERE doc_s_no = %s
        """
        cur.execute(edit_doc_summary, (pname, pteam, psummary, pstart, pend, prange, poutcomes, doc_s_no))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [edit_summary_document] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 프로젝트 개요서 간단본을 모두 조회하는 함수
# 프로젝트 번호를 매개 변수로 받는다
def fetch_all_summary_documents(pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT * FROM doc_summary WHERE doc_s_outcomes IS NOT NULL AND p_no = %s", (pid,))
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Error [fetch_all_summary_documents] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 프로젝트 개요서 상세본을 추가하는 함수
# 추가하려는 프로젝트 개요서 상세본의 내용과 프로젝트 번호를 매개 변수로 받는다
def add_overview_document(poverview, pteam, pgoals, pstart, pend, prange, pstack, pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        add_doc_overview = """
        INSERT INTO doc_summary(doc_s_overview, doc_s_team, doc_s_goals, doc_s_start, doc_s_end, doc_s_range, doc_s_stack, doc_s_date, p_no)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), %s)
        """
        cur.execute(add_doc_overview, (poverview, pteam, pgoals, pstart, pend, prange, pstack, pid))
        connection.commit()

        cur.execute("SELECT * FROM doc_summary WHERE p_no = %s ORDER BY doc_s_no DESC", (pid,))
        row = cur.fetchone()
        return row['doc_s_no']
    except Exception as e:
        connection.rollback()
        print(f"Error [add_overview_document] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 프로젝트 개요서 상세본을 수정하는 함수
# 수정하려는 프로젝트 개요서 상세본의 내용과 산출물 번호를 매개 변수로 받는다
def edit_overview_document(poverview, pteam, pgoals, pstart, pend, prange, pstack, doc_s_no):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        edit_doc_overview = """
        UPDATE doc_summary
        SET doc_s_overview = %s,
            doc_s_team = %s,
            doc_s_goals = %s,
            doc_s_start = %s,
            doc_s_end = %s,
            doc_s_range = %s,
            doc_s_stack = %s
        WHERE doc_s_no = %s
        """
        cur.execute(edit_doc_overview, (poverview, pteam, pgoals, pstart, pend, prange, pstack, doc_s_no))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [edit_overview_document] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 프로젝트 개요서 상세본을 모두 조회하는 함수
# 프로젝트 번호를 매개 변수로 받는다
def fetch_all_overview_documents(pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT * FROM doc_summary WHERE doc_s_stack IS NOT NULL AND p_no = %s", (pid,))
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Error [fetch_all_overview_documents] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 프로젝트 개요서 간단본 또는 상세본 하나만 조회하는 함수
# 조회하려는 프로젝트 개요서 간단본 또는 상세본의 산출물 번호를 매개 변수로 받는다
def fetch_one_summary_document(doc_s_no):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT * FROM doc_summary WHERE doc_s_no = %s", (doc_s_no,))
        result = cur.fetchone()
        return result
    except Exception as e:
        print(f"Error [fetch_one_summary_document] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 프로젝트 개요서 간단본 또는 상세본을 삭제하는 함수
# 삭제하려는 프로젝트 개요서 간단본 또는 상세본의 산출물 번호를 매개 변수로 받는다
def delete_summary_document(doc_s_no):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("DELETE FROM doc_summary WHERE doc_s_no = %s", (doc_s_no,))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [delete_summary_document] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

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
        print(f"Error [add_meeting_minutes] : {e}")
        return e
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
        print(f"Error [edit_meeting_minutes] : {e}")
        return e
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
        print(f"Error [delete_meeting_minutes] : {e}")
        return e
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
        print(f"Error [fetch_all_meeting_minutes] : {e}")
        return e
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
        print(f"Error [fetch_one_meeting_minutes] : {e}")
        return e
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
        INSERT INTO doc_require(doc_r_f_name, doc_r_f_content, doc_r_f_priority, doc_r_nf_name, doc_r_nf_content, doc_r_nf_priority, doc_r_s_name, doc_r_s_content, doc_r_date, p_no)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s)
        """
        cur.execute(add_doc_require, (feature_name, description, priority, non_functional_requirement_name, non_functional_description, non_functional_priority, system_item, system_description, pid))
        connection.commit()

        cur.execute("SELECT * FROM doc_require WHERE p_no = %s ORDER BY doc_r_no DESC", (pid,))
        row = cur.fetchone()
        return row['doc_r_no']
    except Exception as e:
        connection.rollback()
        print(f"Error [add_reqspec] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 요구사항 명세서를 수정하는 함수
# 수정하려는 요구사항 명세서의 내용과 산출물 번호를 매개 변수로 받는다
def edit_reqspec(feature_name, description, priority, non_functional_requirement_name, non_functional_description, non_functional_priority, system_item, system_description, doc_r_no):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        edit_doc_require = """
        UPDATE doc_require
        SET doc_r_f_name = %s,
            doc_r_f_content = %s,
            doc_r_f_priority = %s,
            doc_r_nf_name = %s,
            doc_r_nf_content = %s,
            doc_r_nf_priority = %s,
            doc_r_s_name = %s,
            doc_r_s_content = %s
        WHERE doc_r_no = %s
        """
        cur.execute(edit_doc_require, (feature_name, description, priority, non_functional_requirement_name, non_functional_description, non_functional_priority, system_item, system_description, doc_r_no))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [edit_reqspec] : {e}")
        return e
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
        print(f"Error [delete_reqspec] : {e}")
        return e
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
        print(f"Error [fetch_all_reqspec] : {e}")
        return e
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
        print(f"Error [fetch_one_reqspec] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# ------------------------------ 테스트 케이스 ------------------------------ #
# 테스트 케이스를 추가하는 함수
def add_testcase(tcname, tcstart, tcend, tcpass, pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        add_doc_test = """
        INSERT INTO doc_test(doc_t_name, doc_t_start, doc_t_end, doc_t_pass, p_no)
        VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(add_doc_test, (tcname, tcstart, tcend, tcpass, pid))
        connection.commit()

        cur.execute("SELECT * FROM doc_test WHERE p_no = %s ORDER BY doc_t_no DESC", (pid,))
        row = cur.fetchone()
        return row['doc_t_no']
    except Exception as e:
        connection.rollback()
        print(f"Error [add_testcase] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 테스트 케이스를 수정하는 함수
# 수정하려는 테스트 케이스의 내용과 테스트 번호를 매개 변수로 받는다
def edit_testcase(tcname, tcstart, tcend, tcpass, doc_t_no):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        edit_doc_test = """
        UPDATE doc_test
        SET doc_t_name = %s,
            doc_t_start = %s,
            doc_t_end = %s,
            doc_t_pass = %s
        WHERE doc_t_no = %s
        """
        cur.execute(edit_doc_test, (tcname, tcstart, tcend, tcpass, doc_t_no))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [edit_testcase] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 테스트 케이스를 삭제하는 함수
# 삭제하려는 테스트 케이스의 테스트 번호를 매개 변수로 받는다
def delete_testcase(doc_t_no):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("DELETE FROM doc_test WHERE doc_t_no = %s", (doc_t_no,))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [delete_testcase] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 테스트 케이스를 조회하는 함수
# 프로젝트 번호를 매개 변수로 받는다
def fetch_all_testcase(pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT * FROM doc_test WHERE p_no = %s ORDER BY doc_t_no ASC", (pid,))
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Error [fetch_all_testcase] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# ------------------------------ 기타 산출물 ------------------------------ #
# 기타 산출물을 추가하는 함수
# 추가하려는 기타 산출물의 산출물 고유 번호, 파일 이름, 파일 경로, 프로젝트 번호를 매개 변수로 받는다
def add_other_document(file_unique_id, file_name, file_path, pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        add_doc_other = """
        INSERT INTO doc_other (file_no, file_name, file_path, file_date, p_no)
        VALUES (%s, %s, %s, NOW(), %s)
        """
        cur.execute(add_doc_other, (file_unique_id, file_name, file_path, pid))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [add_other_document] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 기타 산출물을 삭제하는 함수
# 삭제하려는 기타 산출물의 산출물 고유 번호를 매개 변수로 받는다
def delete_other_document(file_unique_id):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("DELETE FROM doc_other WHERE file_no = %s", (file_unique_id,))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [delete_other_document] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 기타 산출물의 목록을 조회하는 함수
# 프로젝트 번호를 매개 변수로 받는다
def fetch_all_other_documents(pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT * FROM doc_other WHERE p_no = %s", (pid,))
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Error [fetch_all_other_documents] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 기타 산출물의 첨부 파일 경로를 조회하여 반환하는 함수
# 산출물 고유 번호를 매개 변수로 받는다
def fetch_file_path(file_unique_id):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("SELECT file_path FROM doc_other WHERE file_no = %s", (file_unique_id,))
        result = cur.fetchone()
        if result:
            return result['file_path']
        else:
            return False
    except Exception as e:
        print(f"Error [fetch_file_path] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 기타 산출물의 첨부 파일 경로를 수정하는 함수
# 산출물 고유 번호와 새로 수정할 파일 경로를 매개 변수로 받는다
def edit_file_path(file_unique_id, new_file_path):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("UPDATE doc_other SET file_path = %s WHERE file_no = %s", (new_file_path, file_unique_id))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [edit_file_path] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# 기타 산출물의 첨부 파일 이름을 수정하는 함수
# 산출물 고유 번호와 새로 수정할 파일 이름을 매개 변수로 받는다
def edit_file_name(file_unique_id, new_file_name):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("UPDATE doc_other SET file_name = %s WHERE file_no = %s", (new_file_name, file_unique_id))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error [edit_file_name] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

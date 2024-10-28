import pymysql
import mysql_connection
import project

def init_project(payload):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        add_project = """
        INSERT INTO project(p_name, p_content, p_method, p_memcount, p_start, p_end, dno)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(add_project, (payload.pname, payload.pdetails, payload.pmm, payload.psize, payload.pperiod, payload.pperiod, 10))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

def edit_project(payload):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

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
        # payload.pperiod 에서 시작일과 종료일로 값을 어떻게 나눌지, 학과 번호를 어떻게 입력받을지 고려.
        cur.execute(edit_project, (payload.pname, payload.pdetails, payload.pmm, payload.psize, payload.pperiod, payload.pperiod, 10, payload.pid))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        return False
    finally:
        cur.close()
        connection.close()

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

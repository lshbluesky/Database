"""
    CodeCraft PMS Project
    파일명 : csv_DB.py
    마지막 수정 날짜 : 2025/01/03
"""

import pymysql
from datetime import datetime
from mysql_connection import db_connect

# 프로젝트 정보를 CSV 파일로 내보내는 함수
# 프로젝트 번호를 매개 변수로 받아서 해당 프로젝트의 정보, 업무, 진척도, 각 산출물 정보를 CSV 파일로 내보낸다
# 내보낸 CSV 파일은 /var/lib/mysql-files/ 경로에 저장된다
def export_csv(pid):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        csv_path = "/var/lib/mysql-files/"
        save_time = datetime.now().strftime("%y%m%d-%H%M%S")

        save_csv_project = f"SELECT * FROM project WHERE p_no = {pid} INTO OUTFILE '{csv_path}project_{pid}_{save_time}.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
        cur.execute(save_csv_project)

        save_csv_work = f"SELECT * FROM work WHERE p_no = {pid} INTO OUTFILE '{csv_path}work_{pid}_{save_time}.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
        cur.execute(save_csv_work)

        save_csv_progress = f"SELECT * FROM progress WHERE p_no = {pid} INTO OUTFILE '{csv_path}progress_{pid}_{save_time}.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
        cur.execute(save_csv_progress)

        save_csv_doc_s = f"SELECT * FROM doc_summary WHERE p_no = {pid} INTO OUTFILE '{csv_path}doc_s_{pid}_{save_time}.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
        cur.execute(save_csv_doc_s)

        save_csv_doc_r = f"SELECT * FROM doc_require WHERE p_no = {pid} INTO OUTFILE '{csv_path}doc_r_{pid}_{save_time}.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
        cur.execute(save_csv_doc_r)

        save_csv_doc_m = f"SELECT * FROM doc_meeting WHERE p_no = {pid} INTO OUTFILE '{csv_path}doc_m_{pid}_{save_time}.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
        cur.execute(save_csv_doc_m)

        save_csv_doc_t = f"SELECT * FROM doc_test WHERE p_no = {pid} INTO OUTFILE '{csv_path}doc_t_{pid}_{save_time}.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
        cur.execute(save_csv_doc_t)

        save_csv_doc_rep = f"SELECT * FROM doc_report WHERE p_no = {pid} INTO OUTFILE '{csv_path}doc_rep_{pid}_{save_time}.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
        cur.execute(save_csv_doc_rep)

        return True
    except Exception as e:
        print(f"Error [export_csv] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

# CSV 파일로부터 프로젝트 정보를 불러와서 DB에 저장하는 함수
def import_csv(file_paths):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    try:
        if "project" in file_paths:
            load_csv_project = f"LOAD DATA INFILE '{file_paths['project']}' INTO TABLE project FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
            cur.execute(load_csv_project)

        if "work" in file_paths:
            load_csv_work = f"LOAD DATA INFILE '{file_paths['work']}' INTO TABLE work FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
            cur.execute(load_csv_work)

        if "progress" in file_paths:
            load_csv_progress = f"LOAD DATA INFILE '{file_paths['progress']}' INTO TABLE progress FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
            cur.execute(load_csv_progress)

        if "doc_summary" in file_paths:
            load_csv_doc_s = f"LOAD DATA INFILE '{file_paths['doc_summary']}' INTO TABLE doc_summary FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
            cur.execute(load_csv_doc_s)

        if "doc_require" in file_paths:
            load_csv_doc_r = f"LOAD DATA INFILE '{file_paths['doc_require']}' INTO TABLE doc_require FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
            cur.execute(load_csv_doc_r)

        if "doc_meeting" in file_paths:
            load_csv_doc_m = f"LOAD DATA INFILE '{file_paths['doc_meeting']}' INTO TABLE doc_meeting FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
            cur.execute(load_csv_doc_m)

        if "doc_test" in file_paths:
            load_csv_doc_t = f"LOAD DATA INFILE '{file_paths['doc_test']}' INTO TABLE doc_test FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
            cur.execute(load_csv_doc_t)

        if "doc_report" in file_paths:
            load_csv_doc_rep = f"LOAD DATA INFILE '{file_paths['doc_report']}' INTO TABLE doc_report FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
            cur.execute(load_csv_doc_rep)

        connection.commit()
        print("Info : 모든 CSV 파일로부터 프로젝트 정보를 불러와서 DB에 저장하였습니다.")
        return True
    except Exception as e:
        print(f"Error [import_csv] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

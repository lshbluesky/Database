"""
    CodeCraft PMS Project
    파일명 : csv_DB.py
    마지막 수정 날짜 : 2025/01/04
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
# {산출물 종류(문자열) : CSV 파일 경로(문자열)} 형태의 딕셔너리를 매개 변수로 받아서 CSV 파일의 내용을 DB에 저장한다
def import_csv(file_paths):
    connection = db_connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    import_ok = []
    import_fail = []

    try:
        if "project" in file_paths:
            try:
                load_csv_project = f"LOAD DATA INFILE '{file_paths['project']}' INTO TABLE project FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
                cur.execute(load_csv_project)
                import_ok.append("project")
            except Exception as e:
                print(f"Error [import_csv :: project] : {e}")
                import_fail.append("project")

        if "work" in file_paths:
            try:
                load_csv_work = f"LOAD DATA INFILE '{file_paths['work']}' INTO TABLE work FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
                cur.execute(load_csv_work)
                import_ok.append("work")
            except Exception as e:
                print(f"Error [import_csv :: work] : {e}")
                import_fail.append("work")

        if "progress" in file_paths:
            try:
                load_csv_progress = f"LOAD DATA INFILE '{file_paths['progress']}' INTO TABLE progress FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
                cur.execute(load_csv_progress)
                import_ok.append("progress")
            except Exception as e:
                print(f"Error [import_csv :: progress] : {e}")
                import_fail.append("progress")

        if "doc_summary" in file_paths:
            try:
                load_csv_doc_s = f"LOAD DATA INFILE '{file_paths['doc_summary']}' INTO TABLE doc_summary FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
                cur.execute(load_csv_doc_s)
                import_ok.append("doc_summary")
            except Exception as e:
                print(f"Error [import_csv :: doc_summary] : {e}")
                import_fail.append("doc_summary")

        if "doc_require" in file_paths:
            try:
                load_csv_doc_r = f"LOAD DATA INFILE '{file_paths['doc_require']}' INTO TABLE doc_require FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
                cur.execute(load_csv_doc_r)
                import_ok.append("doc_require")
            except Exception as e:
                print(f"Error [import_csv :: doc_require] : {e}")
                import_fail.append("doc_require")

        if "doc_meeting" in file_paths:
            try:
                load_csv_doc_m = f"LOAD DATA INFILE '{file_paths['doc_meeting']}' INTO TABLE doc_meeting FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
                cur.execute(load_csv_doc_m)
                import_ok.append("doc_meeting")
            except Exception as e:
                print(f"Error [import_csv :: doc_meeting] : {e}")
                import_fail.append("doc_meeting")

        if "doc_test" in file_paths:
            try:
                load_csv_doc_t = f"LOAD DATA INFILE '{file_paths['doc_test']}' INTO TABLE doc_test FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
                cur.execute(load_csv_doc_t)
                import_ok.append("doc_test")
            except Exception as e:
                print(f"Error [import_csv :: doc_test] : {e}")
                import_fail.append("doc_test")

        if "doc_report" in file_paths:
            try:
                load_csv_doc_rep = f"LOAD DATA INFILE '{file_paths['doc_report']}' INTO TABLE doc_report FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
                cur.execute(load_csv_doc_rep)
                import_ok.append("doc_report")
            except Exception as e:
                print(f"Error [import_csv :: doc_report] : {e}")
                import_fail.append("doc_report")

        connection.commit()

        if not import_fail:
            print("Info : 모든 CSV 파일로부터 프로젝트 정보를 불러와서 DB에 저장하였습니다.")
        else:
            print(f"Info : {len(import_ok)}개의 테이블을 DB에 불러왔습니다.")
            print(f"Warning : 불러오지 못한 테이블은 [{', '.join(import_fail)}] 입니다.")
        return True
    except Exception as e:
        print(f"Error [import_csv] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

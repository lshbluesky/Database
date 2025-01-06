"""
    CodeCraft PMS Project
    파일명 : csv_DB.py
    마지막 수정 날짜 : 2025/01/06
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

        save_csv_work = f"SELECT w_name, w_person, w_start, w_end, w_checked, p_no, s_no FROM work WHERE p_no = {pid} INTO OUTFILE '{csv_path}work_{pid}_{save_time}.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
        cur.execute(save_csv_work)

        save_csv_progress = f"SELECT group1, group2, group3, group4, work, output_file, manager, note, ratio, start_date, end_date, group1no, group2no, group3no, group4no, p_no FROM progress WHERE p_no = {pid} INTO OUTFILE '{csv_path}progress_{pid}_{save_time}.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
        cur.execute(save_csv_progress)

        save_csv_doc_s = f"SELECT doc_s_name, doc_s_overview, doc_s_goals, doc_s_range, doc_s_outcomes, doc_s_team, doc_s_stack, doc_s_start, doc_s_end, doc_s_date, p_no FROM doc_summary WHERE p_no = {pid} INTO OUTFILE '{csv_path}doc_s_{pid}_{save_time}.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
        cur.execute(save_csv_doc_s)

        save_csv_doc_r = f"SELECT doc_r_f_name, doc_r_f_content, doc_r_f_priority, doc_r_nf_name, doc_r_nf_content, doc_r_nf_priority, doc_r_s_name, doc_r_s_content, doc_r_date, p_no FROM doc_require WHERE p_no = {pid} INTO OUTFILE '{csv_path}doc_r_{pid}_{save_time}.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
        cur.execute(save_csv_doc_r)

        save_csv_doc_m = f"SELECT doc_m_title, doc_m_date, doc_m_loc, doc_m_member, doc_m_manager, doc_m_content, doc_m_result, p_no FROM doc_meeting WHERE p_no = {pid} INTO OUTFILE '{csv_path}doc_m_{pid}_{save_time}.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
        cur.execute(save_csv_doc_m)

        save_csv_doc_t = f"SELECT doc_t_name, doc_t_start, doc_t_end, doc_t_pass, p_no FROM doc_test WHERE p_no = {pid} INTO OUTFILE '{csv_path}doc_t_{pid}_{save_time}.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
        cur.execute(save_csv_doc_t)

        save_csv_doc_rep = f"SELECT doc_rep_name, doc_rep_writer, doc_rep_date, doc_rep_pname, doc_rep_member, doc_rep_professor, doc_rep_research, doc_rep_design, doc_rep_arch, doc_rep_result, doc_rep_conclusion, p_no FROM doc_report WHERE p_no = {pid} INTO OUTFILE '{csv_path}doc_rep_{pid}_{save_time}.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n'"
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
# csv_dict = {
#     "project" : "/var/lib/mysql-files/project_10001_250105-153058.csv",
#     "work" : "/var/lib/mysql-files/work_10001_250105-153058.csv",
#     "progress" : "/var/lib/mysql-files/progress_10001_250105-153058.csv",
#     "doc_summary" : "/var/lib/mysql-files/doc_s_10001_250105-153058.csv",
#     "doc_require" : "/var/lib/mysql-files/doc_r_10001_250105-153058.csv",
#     "doc_meeting" : "/var/lib/mysql-files/doc_m_10001_250105-153058.csv",
#     "doc_test" : "/var/lib/mysql-files/doc_t_10001_250105-153058.csv",
#     "doc_report" : "/var/lib/mysql-files/doc_rep_10001_250105-153058.csv"
# }
# 위와 같이 딕셔너리를 만들고, import_csv(csv_dict) 와 같이 함수를 호출하여 사용한다
# 참고 : 딕셔너리의 키는 수정이 불가능하며, 값은 /var/lib/mysql-files 경로 대신에 실제 CSV 파일이 저장되어 있는 다른 경로로 변경할 수 있다
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
                load_csv_work = f"LOAD DATA INFILE '{file_paths['work']}' INTO TABLE work FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n' (w_name, w_person, w_start, w_end, w_checked, p_no, s_no)"
                cur.execute(load_csv_work)
                import_ok.append("work")
            except Exception as e:
                print(f"Error [import_csv :: work] : {e}")
                import_fail.append("work")

        if "progress" in file_paths:
            try:
                load_csv_progress = f"LOAD DATA INFILE '{file_paths['progress']}' INTO TABLE progress FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n' (group1, group2, group3, group4, work, output_file, manager, note, ratio, start_date, end_date, group1no, group2no, group3no, group4no, p_no)"
                cur.execute(load_csv_progress)
                import_ok.append("progress")
            except Exception as e:
                print(f"Error [import_csv :: progress] : {e}")
                import_fail.append("progress")

        if "doc_summary" in file_paths:
            try:
                load_csv_doc_s = f"LOAD DATA INFILE '{file_paths['doc_summary']}' INTO TABLE doc_summary FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n' (doc_s_name, doc_s_overview, doc_s_goals, doc_s_range, doc_s_outcomes, doc_s_team, doc_s_stack, doc_s_start, doc_s_end, doc_s_date, p_no)"
                cur.execute(load_csv_doc_s)
                import_ok.append("doc_summary")
            except Exception as e:
                print(f"Error [import_csv :: doc_summary] : {e}")
                import_fail.append("doc_summary")

        if "doc_require" in file_paths:
            try:
                load_csv_doc_r = f"LOAD DATA INFILE '{file_paths['doc_require']}' INTO TABLE doc_require FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n' (doc_r_f_name, doc_r_f_content, doc_r_f_priority, doc_r_nf_name, doc_r_nf_content, doc_r_nf_priority, doc_r_s_name, doc_r_s_content, doc_r_date, p_no)"
                cur.execute(load_csv_doc_r)
                import_ok.append("doc_require")
            except Exception as e:
                print(f"Error [import_csv :: doc_require] : {e}")
                import_fail.append("doc_require")

        if "doc_meeting" in file_paths:
            try:
                load_csv_doc_m = f"LOAD DATA INFILE '{file_paths['doc_meeting']}' INTO TABLE doc_meeting FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n' (doc_m_title, doc_m_date, doc_m_loc, doc_m_member, doc_m_manager, doc_m_content, doc_m_result, p_no)"
                cur.execute(load_csv_doc_m)
                import_ok.append("doc_meeting")
            except Exception as e:
                print(f"Error [import_csv :: doc_meeting] : {e}")
                import_fail.append("doc_meeting")

        if "doc_test" in file_paths:
            try:
                load_csv_doc_t = f"LOAD DATA INFILE '{file_paths['doc_test']}' INTO TABLE doc_test FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n' (doc_t_name, doc_t_start, doc_t_end, doc_t_pass, p_no)"
                cur.execute(load_csv_doc_t)
                import_ok.append("doc_test")
            except Exception as e:
                print(f"Error [import_csv :: doc_test] : {e}")
                import_fail.append("doc_test")

        if "doc_report" in file_paths:
            try:
                load_csv_doc_rep = f"LOAD DATA INFILE '{file_paths['doc_report']}' INTO TABLE doc_report FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '^' LINES TERMINATED BY '\\n' (doc_rep_name, doc_rep_writer, doc_rep_date, doc_rep_pname, doc_rep_member, doc_rep_professor, doc_rep_research, doc_rep_design, doc_rep_arch, doc_rep_result, doc_rep_conclusion, p_no)"
                cur.execute(load_csv_doc_rep)
                import_ok.append("doc_report")
            except Exception as e:
                print(f"Error [import_csv :: doc_report] : {e}")
                import_fail.append("doc_report")

        connection.commit()

        if not import_fail:
            print("Info : 모든 CSV 파일로부터 프로젝트 정보를 불러와서 DB에 저장하였습니다.")
            return True
        else:
            print(f"Info : {len(import_ok)}개의 테이블을 DB에 불러왔습니다.")
            print(f"Warning : 불러오지 못한 테이블은 [{', '.join(import_fail)}] 입니다.")
            return False
    except Exception as e:
        print(f"Error [import_csv] : {e}")
        return e
    finally:
        cur.close()
        connection.close()

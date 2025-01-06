CREATE DATABASE PMS DEFAULT CHARACTER SET utf8mb4;
USE PMS;

CREATE TABLE student (
 s_no INT NOT NULL PRIMARY KEY,
 s_id VARCHAR(20) NOT NULL UNIQUE,
 s_pw VARCHAR(255) NOT NULL,
 s_name VARCHAR(20) NOT NULL,
 s_email VARCHAR(255) NOT NULL,
 s_token VARCHAR(30) NULL UNIQUE,
 dno INT NOT NULL
);

CREATE TABLE admin (
 a_id VARCHAR(20) NOT NULL PRIMARY KEY,
 a_pw VARCHAR(255) NOT NULL,
 a_name VARCHAR(20) NOT NULL,
 a_email VARCHAR(255) NOT NULL,
 a_token VARCHAR(30) NULL UNIQUE
);

CREATE TABLE project_user (
 p_no INT NOT NULL,
 s_no INT NOT NULL,
 permission BOOLEAN NOT NULL,
 role VARCHAR(100) NULL,
 grade VARCHAR(2) NULL,
 PRIMARY KEY (p_no, s_no)
);

CREATE TABLE doc_other (
 file_no INT NOT NULL PRIMARY KEY,
 file_name VARCHAR(300) NOT NULL,
 file_path VARCHAR(1000) NOT NULL,
 file_date DATETIME NOT NULL,
 s_no INT NOT NULL,
 p_no INT NOT NULL
);

CREATE TABLE progress (
 progress_no INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 group1 VARCHAR(300) NULL,
 group2 VARCHAR(300) NULL,
 group3 VARCHAR(300) NULL,
 group4 VARCHAR(300) NULL,
 work VARCHAR(500) NULL,
 output_file VARCHAR(500) NULL,
 manager VARCHAR(20) NULL,
 note VARCHAR(1000) NULL,
 ratio DOUBLE NOT NULL,
 start_date DATE NOT NULL,
 end_date DATE NOT NULL,
 group1no INT NULL,
 group2no INT NULL,
 group3no INT NULL,
 group4no INT NULL,
 p_no INT NOT NULL
);

CREATE TABLE project (
 p_no INT NOT NULL PRIMARY KEY,
 p_name VARCHAR(300) NOT NULL,
 p_content TEXT NOT NULL,
 p_method VARCHAR(20) NOT NULL,
 p_memcount INT NOT NULL,
 p_start DATE NOT NULL,
 p_end DATE NOT NULL,
 dno INT NOT NULL
);

CREATE TABLE work (
 w_no INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 w_name VARCHAR(300) NOT NULL,
 w_person VARCHAR(20) NULL,
 w_start DATE NOT NULL,
 w_end DATE NOT NULL,
 w_checked BOOLEAN NOT NULL,
 p_no INT NOT NULL,
 s_no INT NULL
);

CREATE TABLE dept (
 dno INT NOT NULL PRIMARY KEY,
 dname VARCHAR(20) NOT NULL
);

CREATE TABLE doc_require (
 doc_r_no INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 doc_r_f_name TEXT NULL,
 doc_r_f_content TEXT NULL,
 doc_r_f_priority TEXT NULL,
 doc_r_nf_name TEXT NULL,
 doc_r_nf_content TEXT NULL,
 doc_r_nf_priority TEXT NULL,
 doc_r_s_name TEXT NULL,
 doc_r_s_content TEXT NULL,
 doc_r_date DATE NOT NULL,
 p_no INT NOT NULL
);

CREATE TABLE doc_meeting (
 doc_m_no INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 doc_m_title TEXT NOT NULL,
 doc_m_date DATE NOT NULL,
 doc_m_loc TEXT NOT NULL,
 doc_m_member TEXT NOT NULL,
 doc_m_manager TEXT NOT NULL,
 doc_m_content TEXT NOT NULL,
 doc_m_result TEXT NOT NULL,
 p_no INT NOT NULL
);

CREATE TABLE doc_summary (
 doc_s_no INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 doc_s_name VARCHAR(300) NULL,
 doc_s_overview TEXT NULL,
 doc_s_goals TEXT NULL,
 doc_s_range TEXT NULL,
 doc_s_outcomes TEXT NULL,
 doc_s_team TEXT NULL,
 doc_s_stack TEXT NULL,
 doc_s_start DATE NOT NULL,
 doc_s_end DATE NOT NULL,
 doc_s_date DATE NOT NULL,
 p_no INT NOT NULL
);

CREATE TABLE doc_test (
 doc_t_no INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 doc_t_name TEXT NOT NULL,
 doc_t_start DATE NOT NULL,
 doc_t_end DATE NOT NULL,
 doc_t_pass BOOLEAN NOT NULL,
 p_no INT NOT NULL
);

CREATE TABLE doc_report (
 doc_rep_no INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 doc_rep_name TEXT NOT NULL,
 doc_rep_writer TEXT NOT NULL,
 doc_rep_date DATE NOT NULL,
 doc_rep_pname TEXT NULL,
 doc_rep_member TEXT NULL,
 doc_rep_professor TEXT NULL,
 doc_rep_research TEXT NULL,
 doc_rep_design TEXT NULL,
 doc_rep_arch TEXT NULL,
 doc_rep_result TEXT NULL,
 doc_rep_conclusion TEXT NULL,
 p_no INT NOT NULL
);

ALTER TABLE student ADD CONSTRAINT FK_dept_TO_student_1 FOREIGN KEY (dno) REFERENCES dept (dno);
ALTER TABLE project_user ADD CONSTRAINT FK_project_TO_project_user_1 FOREIGN KEY (p_no) REFERENCES project (p_no) ON DELETE CASCADE;
ALTER TABLE project_user ADD CONSTRAINT FK_student_TO_project_user_1 FOREIGN KEY (s_no) REFERENCES student (s_no) ON DELETE CASCADE;
ALTER TABLE doc_other ADD CONSTRAINT FK_student_TO_doc_other_1 FOREIGN KEY (s_no) REFERENCES student (s_no);
ALTER TABLE doc_other ADD CONSTRAINT FK_project_TO_doc_other_1 FOREIGN KEY (p_no) REFERENCES project (p_no) ON DELETE CASCADE;
ALTER TABLE progress ADD CONSTRAINT FK_project_TO_progress_1 FOREIGN KEY (p_no) REFERENCES project (p_no) ON DELETE CASCADE;
ALTER TABLE project ADD CONSTRAINT FK_dept_TO_project_1 FOREIGN KEY (dno) REFERENCES dept (dno);
ALTER TABLE work ADD CONSTRAINT FK_project_user_TO_work FOREIGN KEY (p_no, s_no) REFERENCES project_user (p_no, s_no) ON DELETE CASCADE;
ALTER TABLE doc_require ADD CONSTRAINT FK_project_TO_doc_require_1 FOREIGN KEY (p_no) REFERENCES project (p_no) ON DELETE CASCADE;
ALTER TABLE doc_meeting ADD CONSTRAINT FK_project_TO_doc_meeting_1 FOREIGN KEY (p_no) REFERENCES project (p_no) ON DELETE CASCADE;
ALTER TABLE doc_summary ADD CONSTRAINT FK_project_TO_doc_summary_1 FOREIGN KEY (p_no) REFERENCES project (p_no) ON DELETE CASCADE;
ALTER TABLE doc_test ADD CONSTRAINT FK_project_TO_doc_test_1 FOREIGN KEY (p_no) REFERENCES project (p_no) ON DELETE CASCADE;
ALTER TABLE doc_report ADD CONSTRAINT FK_project_TO_doc_report_1 FOREIGN KEY (p_no) REFERENCES project (p_no) ON DELETE CASCADE;

ALTER TABLE project_user ADD CONSTRAINT CK_project_user_grade CHECK (grade IN ('A+', 'A', 'B+', 'B', 'C+', 'C', 'D+', 'D', 'F'));

INSERT INTO dept VALUES(10, '컴퓨터소프트웨어학과');
INSERT INTO dept VALUES(11, '가상현실학과');
INSERT INTO dept VALUES(12, '지능정보통신공학과');
INSERT INTO dept VALUES(13, '멀티미디어학과');
INSERT INTO dept VALUES(20, '드론공간정보공학과');
INSERT INTO dept VALUES(21, '빅데이터경영공학과');
INSERT INTO dept VALUES(22, '전자공학과');
SELECT * FROM dept;
COMMIT;

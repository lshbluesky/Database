CREATE TABLE `student` (
	`s_no`	INT	NOT NULL PRIMARY KEY,
	`s_id`	VARCHAR(20)	NOT NULL UNIQUE,
	`s_pw`	VARCHAR(255)	NOT NULL,
	`s_name`	VARCHAR(20)	NOT NULL,
	`s_email`	VARCHAR(255)	NOT NULL,
	`s_time_join`	DATETIME	NULL,
	`s_time_edit`	DATETIME	NULL,
	`s_time_delete`	DATETIME	NULL,
	`dno`	INT	NOT NULL
);

CREATE TABLE `professor` (
	`f_no`	INT	NOT NULL PRIMARY KEY,
	`f_id`	VARCHAR(20)	NOT NULL UNIQUE,
	`f_pw`	VARCHAR(255)	NOT NULL,
	`f_name`	VARCHAR(20)	NOT NULL,
	`f_email`	VARCHAR(255)	NOT NULL,
	`f_time_join`	DATETIME	NULL,
	`f_time_edit`	DATETIME	NULL,
	`f_time_delete`	DATETIME	NULL,
	`dno`	INT	NOT NULL
);

CREATE TABLE `project_user` (
	`p_no`	INT	NOT NULL,
	`s_no`	INT	NOT NULL,
	`permission`	BOOLEAN	NOT NULL,
	`role`	VARCHAR(100)	NULL,
	`grade`	VARCHAR(2)	NULL,
	`f_no`	INT	NULL,
	PRIMARY KEY (`p_no`, `s_no`)
);

CREATE TABLE `document` (
	`file_no`	INT	NOT NULL	PRIMARY KEY	AUTO_INCREMENT,
	`file_category`	VARCHAR(100)	NOT NULL,
	`file_name`	VARCHAR(300)	NOT NULL,
	`file_path`	VARCHAR(10000)	NOT NULL,
	`file_date`	DATETIME	NOT NULL,
	`p_no`	INT	NOT NULL
);

CREATE TABLE `progress` (
	`progress_no`	INT	NOT NULL	PRIMARY KEY	AUTO_INCREMENT,
	`group1`	VARCHAR(300)	NULL,
	`group2`	VARCHAR(300)	NULL,
	`group3`	VARCHAR(300)	NULL,
	`work`	VARCHAR(500)	NULL,
	`output_file`	VARCHAR(500)	NULL,
	`manager`	VARCHAR(20)	NULL,
	`note`	VARCHAR(1000)	NULL,
	`ratio`	DOUBLE	NOT NULL,
	`start_date`	DATE	NOT NULL,
	`end_date`	DATE	NOT NULL,
	`group1no`	INT	NULL,
	`group2no`	INT	NULL,
	`group3no`	INT	NULL,
	`p_no`	INT	NOT NULL
);

CREATE TABLE `project` (
	`p_no`	INT	NOT NULL	PRIMARY KEY	AUTO_INCREMENT,
	`p_name`	VARCHAR(300)	NOT NULL,
	`p_content`	VARCHAR(5000)	NOT NULL,
	`p_method`	VARCHAR(20)	NOT NULL,
	`p_memcount`	INT	NOT NULL,
	`p_start`	DATE	NOT NULL,
	`p_end`	DATE	NOT NULL,
	`dno`	INT	NOT NULL
);

CREATE TABLE `work` (
	`w_no`	INT	NOT NULL	PRIMARY KEY	AUTO_INCREMENT,
	`w_name`	VARCHAR(300)	NOT NULL,
	`w_content`	VARCHAR(5000)	NOT NULL,
	`w_start`	DATE	NOT NULL,
	`w_end`	DATE	NOT NULL,
	`w_checked`	BOOLEAN	NOT NULL,
	`p_no`	INT	NOT NULL,
	`s_no`	INT	NOT NULL
);

CREATE TABLE `dept` (
	`dno`	INT	NOT NULL	PRIMARY KEY,
	`dname`	VARCHAR(20)	NOT NULL
);

ALTER TABLE `student` ADD CONSTRAINT `FK_dept_TO_student_1` FOREIGN KEY (`dno`) REFERENCES `dept` (`dno`);
ALTER TABLE `professor` ADD CONSTRAINT `FK_dept_TO_professor_1` FOREIGN KEY (`dno`) REFERENCES `dept` (`dno`);
ALTER TABLE `project_user` ADD CONSTRAINT `FK_project_TO_project_user_1` FOREIGN KEY (`p_no`) REFERENCES `project` (`p_no`);
ALTER TABLE `project_user` ADD CONSTRAINT `FK_student_TO_project_user_1` FOREIGN KEY (`s_no`) REFERENCES `student` (`s_no`);
ALTER TABLE `project_user` ADD CONSTRAINT `FK_professor_TO_project_user_1` FOREIGN KEY (`f_no`) REFERENCES `professor` (`f_no`);
ALTER TABLE `document` ADD CONSTRAINT `FK_project_TO_document_1` FOREIGN KEY (`p_no`) REFERENCES `project` (`p_no`);
ALTER TABLE `progress` ADD CONSTRAINT `FK_project_TO_progress_1` FOREIGN KEY (`p_no`) REFERENCES `project` (`p_no`);
ALTER TABLE `project` ADD CONSTRAINT `FK_dept_TO_project_1` FOREIGN KEY (`dno`) REFERENCES `dept` (`dno`);
ALTER TABLE work ADD CONSTRAINT FK_project_user_TO_work FOREIGN KEY (p_no, s_no) REFERENCES project_user (p_no, s_no);

insert into dept values(10, '컴퓨터소프트웨어학과');
insert into dept values(11, '가상현실학과');
insert into dept values(12, '지능정보통신공학과');
insert into dept values(13, '멀티미디어학과');
insert into dept values(20, '드론공간정보공학과');
insert into dept values(21, '빅데이터경영공학과');
insert into dept values(22, '전자공학과');
select * from dept;
commit;

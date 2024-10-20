import pymysql
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_DB_IP = os.getenv('DB_HOST_IP')
SECRET_DB_PW = os.getenv('DB_PASSWORD')
conn = pymysql.connect(
    host=SECRET_DB_IP,
    port=3306,
    user='root',
    password=SECRET_DB_PW,
    db='PMS',
    charset='utf8mb4'
)
cur = conn.cursor(pymysql.cursors.DictCursor)

# 각 로직의 변수는 실제로는 프론트엔드에서 받아온 json 등의 파일에 있는 값으로 처리하지만, 지금은 임의의 값을 지정하였습니다.

# 학생 추가
s_no = 20101234
s_id = 'gildong123'
s_pw = 'abc123'
s_name = '홍길동'
s_email = 'gildong@naver.com'
dno = 10

add_student = """
INSERT INTO student (s_no, s_id, s_pw, s_name, s_email, s_time_join, s_time_edit, s_time_delete, dno)
VALUES (%s, %s, %s, %s, %s, NOW(), NULL, NULL, %s)
"""
cur.execute(add_student, (s_no, s_id, s_pw, s_name, s_email, dno))
conn.commit()

# 학생 수정
s_no = 20101234
s_id = 'gildong123'
s_pw = 'abc123'
s_name = '홍길동'
s_email = 'gildong@naver.com'
dno = 10

edit_student = "UPDATE student SET s_id=%s, s_pw=%s, s_name=%s, s_email=%s, s_time_edit=NOW(), dno=%s WHERE s_no=%s"
cur.execute(edit_student, (s_id, s_pw, s_name, s_email, dno, s_no))
conn.commit()

# 학생 삭제
s_no = 20101234

delete_student = "DELETE FROM student WHERE s_no=%s"
cur.execute(delete_student, (s_no))
conn.commit()

# 학번으로 학생 조회
s_no = 20101234

find_student = "SELECT * FROM student WHERE s_no=%s"
cur.execute(find_student, (s_no))

# 학생 전체 조회
cur.execute("select * from student;")
result = cur.fetchall()
print(result)

conn.close()
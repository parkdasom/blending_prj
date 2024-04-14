import sqlite3

# SQLite 데이터베이스 연결
conn = sqlite3.connect('welfare.db')
cursor = conn.cursor()

# 데이터 삽입을 위한 SQL 쿼리 작성
insert_query = """
    INSERT INTO benefit (name, description, requirements)
    VALUES (?, ?, ?)
"""

# 예시 데이터
applications_data = [
    ("Benefit 1", "베네핏 1", "1000만원 이상"),
    ("Benefit 2", "베네핏 2", "2000만원 이상"),
    # 다른 데이터 추가
]

# 데이터 삽입
for data in applications_data:
    cursor.execute(insert_query, data)

# 변경사항 저장
conn.commit()

# 연결 종료
conn.close()

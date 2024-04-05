import sqlite3

# SQLite 데이터베이스 연결
conn = sqlite3.connect('welfare.db')

# 커서 생성
cur = conn.cursor()

# 사용자 데이터 조회
cur.execute("SELECT * FROM user;")
rows = cur.fetchall()
for row in rows:
    print(row)

# 연결 종료
conn.close()

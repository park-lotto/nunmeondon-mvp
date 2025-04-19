import pandas as pd
import sqlite3

df = pd.read_csv("data/sample_data.csv", encoding="cp949")

conn = sqlite3.connect("data/data.db")
df.to_sql("support", conn, if_exists="replace", index=False)
conn.close()

print("✅ CSV → SQLite 변환 완료")

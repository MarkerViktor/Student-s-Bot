import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()
cursor.execute('SELECT name, surname FROM users WHERE vk_id=94138203')
print(cursor.fetchall())

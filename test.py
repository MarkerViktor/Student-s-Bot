import os
import psycopg2
DATABASE_URL = os.environ['DATABASE_URL']
def connect():
  conn = psycopg2.connect(config.DATABASE_URL, sslmode='require')
  return conn.cursor()
def search():
  cursor = connect()
  cursor.execute('SELECT name, surname FROM users WHERE id=94138203')
  print(cursor.fetchall())

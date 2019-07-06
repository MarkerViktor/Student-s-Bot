import os
import psycopg2
def connect():
  DATABASE_URL = os.environ['DATABASE_URL']
  conn = psycopg2.connect(config.DATABASE_URL, sslmode='require')
  return conn.cursor()
def search():
  cursor = connect()
  cursor.execute('SELECT name, surname FROM users WHERE id=94138203')
  print(cursor.fetchall())

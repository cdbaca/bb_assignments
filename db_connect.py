import psycopg2
import credentials

hostname = credentials.hostname
database = credentials.database
username = credentials.username
pwd = credentials.pwd
port_id = credentials.port_id
conn = None
cur = None

def connect():
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id
    )

    cur = conn.cursor()

    return(cur)

connect()

if conn is not None:
    conn.close()
if cur is not None:
    cur.close()

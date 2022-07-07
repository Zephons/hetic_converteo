import os
import psycopg
import pandas as pd
from sqlalchemy import create_engine

postgresql_uri = os.environ["DATABASE_URL"]
conn_dict =  psycopg.conninfo.conninfo_to_dict(postgresql_uri)

df_casto_sample = pd.read_excel("data/sample.xlsx", header=[1])

engine = create_engine(postgresql_uri.replace("postgres", "postgresql"))
df_casto_sample.to_sql(name="sample", con=engine, if_exists="replace")

# with psycopg.connect(**conn_dict) as conn:
#     with conn.cursor() as cur:
#         cur.execute("""
#             CREATE TABLE test (
#                 id serial PRIMARY KEY,
#                 num integer,
#                 data text)
#             """)
#         cur.execute(
#             "INSERT INTO test (num, data) VALUES (%s, %s)",
#             (100, "abc'def"))

#         cur.execute("SELECT * FROM test")
#         cur.fetchone()

#         for record in cur:
#             print(record)
#         conn.commit()

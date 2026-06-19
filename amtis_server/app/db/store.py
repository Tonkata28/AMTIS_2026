db = {
    "users": {},
    "session_id": None,
    "sessions": {},
    "regulations": list[dict]
}

from dotenv import load_dotenv

load_dotenv("credentials.env")

# import os
# import psycopg

# try:
#     with psycopg.connect(
#         host=os.environ["DB_HOST"],
#         port=int(os.environ["DB_PORT"]),
#         dbname=os.environ["DB_NAME"],
#         user=os.environ["DB_USER"],
#         password=os.environ["DB_PASSWORD"],
#         connect_timeout=5,
#     ) as conn:
#         with conn.cursor() as cur:
            
#             create_table = """CREATE TABLE IF NOT EXISTS test(
#                                 id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
#                                 name VARCHAR(50) NOT NULL,
#                                 email VARCHAR(50) NOT NULL
#             )"""

#             insert_into_table = """
#                 INSERT INTO test (name, email)
#                 VALUES (%s, %s)
#             """

#             select_from_table = "SELECT * FROM test"

#             cur.execute(create_table)
#             cur.execute(insert_into_table, ("Anton", "email"))
#             cur.execute(select_from_table)

#             print(cur.fetchone())

# except Exception as ex:
#     print(ex)

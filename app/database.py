from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# import psycopg2
# import time
# from psycopg2.extras import RealDictCursor

# default set up for the database url
# SQLALCHEMY_DATABSE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'


SQLALCHEMY_DATABSE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABSE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Not necessary anymore, since we are using SQLAlchemy to interact with our database.
# This would be used if we were using Raw SQL
# ===================================================================================

# We don't want our server to run if the connect to the database fails, so
# let's put this in a while
# while True:
#     try:
#         # conn = psycopg2.connect(host, database, user, password)
#         # To do: these values are hard coded. Bad Idea. We need to dynamically
#         # assign these.
#         conn = psycopg2.connect(
#             host='localhost', database='fastapi', user='postgres',
#             password='aagdgfb', cursor_factory=RealDictCursor)
#         # cursor is used to execute SQL statements
#         cursor = conn.cursor()
#         print("Database connection was succesfull")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print(f"Error: {error}")
#         time.sleep(2)

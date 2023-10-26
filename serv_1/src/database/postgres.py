import databases
import sqlalchemy
import psycopg2
import logging

logging.basicConfig(level=logging.INFO)

DB_URL = 'postgresql://root:ubfiQ3VV5IPiy1oaDYswWZXH@arthur.iran.liara.ir:33048/postgres'
database = databases.Database(DB_URL)
metadata = sqlalchemy.MetaData()
eng = sqlalchemy.create_engine(DB_URL)

user_table = sqlalchemy.Table(
    "user_table",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("lastname", sqlalchemy.String),
    sqlalchemy.Column("national_id", sqlalchemy.String),
    sqlalchemy.Column("IP", sqlalchemy.String),
    sqlalchemy.Column("image1", sqlalchemy.String),
    sqlalchemy.Column("image2", sqlalchemy.String),
    sqlalchemy.Column("state", sqlalchemy.String)
)
metadata.create_all(eng)
from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
    MetaData,
    create_engine
)

from databases import Database

DATABASE_URL = "sqlite:///./fastapidb.db"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

Article = Table(
    'articles',
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(200)),
    Column("description", String(500))
)

User = Table(
'users',
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50)),
    Column("password", String(500))
)

database = Database(DATABASE_URL)

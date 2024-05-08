from pydantic import BaseModel
from typing import Optional
from .database import Base
from sqlalchemy import Boolean, Integer, String, Column, ForeignKey
from sqlalchemy.sql.expression import Null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='social_media',
#                                 user='postgres', password='Systemmind1234', cursor_factory=RealDictCursor)
#         curs = conn.cursor()
#         print('Database connection established')
#         break
#     except Exception as error:
#         print('Database connection not established')
#         print('Error: ', error)
#         time.sleep(2)

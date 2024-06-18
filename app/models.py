from pydantic import BaseModel
from typing import Optional
from app.database import Base
from sqlalchemy import Boolean, Integer, String, Column, ForeignKey, orm
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
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    owner = orm.relationship("User")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))


class Votes(Base):
    __tablename__ = 'votes'
    post_id = Column(Integer, ForeignKey(
        "post.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)

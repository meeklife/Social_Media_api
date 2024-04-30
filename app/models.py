from pydantic import BaseModel
from typing import Optional
from datetime import date
import psycopg2
from psycopg2.extras import RealDictCursor
import time


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='social_media',
                                user='postgres', password='Systemmind1234', cursor_factory=RealDictCursor)
        curs = conn.cursor()
        print('Database connection established')
        break
    except Exception as error:
        print('Database connection not established')
        print('Error: ', error)
        time.sleep(2)

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

while True:
    """creates a connection to the database"""
    try:
        conn = psycopg2.connect(
            host="<host>",
            database="<database>",
            user="<user>",
            password="<password>",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("\033[1;32;40mdatabase connection was successful!")
        break
    except Exception as e:
        print(f"\033[1;31;40merror: {e}")
        time.sleep(2)

@app.get("/test")
def test_request(db: Session = Depends(get_db)):
    """This is a test function to execute a basic query, the database will return
    all the products and the api will send it all to the frontend"""
    products = db.query(models.Product).all()
    return {"products": products}

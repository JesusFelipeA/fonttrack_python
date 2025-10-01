# backend/services/db_connection.py

from pymongo import MongoClient
from config import env

def get_db():
    client = MongoClient(env.MONGO_URI)
    db = client[env.DB_NAME]
    return db

def get_collection(name):
    db = get_db()
    return db[name]

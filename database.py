from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


class Connect(object):
    @staticmethod
    def get_connection():
        print(DATABASE_URL)
        return MongoClient(DATABASE_URL)

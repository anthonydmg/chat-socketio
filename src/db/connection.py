from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def mongodb_conn():
    try:
        return MongoClient("mongodb://adminbot:aerito@localhost:27017/?authMechanism=DEFAULT&authSource=chatbot")
    except ConnectionFailure as e:
        print(f"Could not connect to server: {e}")

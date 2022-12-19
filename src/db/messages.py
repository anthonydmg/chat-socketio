from .connection import mongodb_conn
from datetime import datetime

conn = mongodb_conn()

chatbotDB = conn['chatbot']
message_collection = chatbotDB['messages']

def insert_message_user(message, intent_name , intent_score, entities, session_id):
    try:
        message_collection.insert_one({"message": message, "sender": "user", "session_id": session_id , 
                                        "intent_name": intent_name , "intent_score": intent_score, "entities": entities, "date": datetime.now()})
        return True
    except Exception as e:
        print("Insercion de nuevo mensaje fallo ::", e)
        return False

def insert_message_bot(message, utter_response, session_id):
    try:
        message_collection.insert_one({"message": message, "sender": "bot", "utter_response" : utter_response, "session_id": session_id , "date": datetime.now()})
        return True
    except Exception as e:
        print("Insercion de nuevo mensaje fallo ::", e)
        return False

def get_sorted_messages_by_session(session_id):
    messages = message_collection.find({"session_id": session_id}).sort("date")
    return list(messages)


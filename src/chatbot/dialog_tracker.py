from ..db import messages

class DialogTracker:
    def get_dialogue_history(session_id):
        return messages.get_sorted_messages_by_session(session_id)

    def get_last_user_message(session_id):
        dialogue_history = messages.get_sorted_messages_by_session(session_id)
        messages_user = [message for message in dialogue_history if message['sender'] == "user"]
        last_message_user = messages_user[-1] if len(messages_user) > 0 else None
        return last_message_user 

    def get_last_bot_message(session_id):
        dialogue_history = messages.get_sorted_messages_by_session(session_id)
        messages_bot = [message for message in dialogue_history if message['sender'] == "bot"]
        last_message_bot = messages_bot[-1] if len(messages_bot) > 0 else None
        return last_message_bot

    def register_message_user(message, intent_name , intent_score, entities, session_id):
        messages.insert_message_user(message, intent_name , intent_score, entities, session_id)
    
    def register_message_bot(message, utter_reponse, session_id):
        messages.insert_message_bot(message, utter_reponse, session_id)
    



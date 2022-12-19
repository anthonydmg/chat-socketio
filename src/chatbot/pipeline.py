from .nlu import NLU
from .dialog_manager import DialogManagement
from .dialog_tracker import DialogTracker
from .responses import get_template_response
import re

pattern = "\\\\\S+"

class Pipeline:
    def __init__(self) -> None:
        self.nlu = NLU()
        self.dm = DialogManagement()

    def preprocessing(self, text):
        text = text.lower()
        text = text.strip()
        return text

    def run(self, message, session_id):
        ## Prepocesing text
        print("Message Pipeline: ", message)

        if not re.match(pattern, message): 
            clean_message = self.preprocessing(message)
            ## Nlu Inference
            nlu_data = self.nlu.inference(clean_message)
            intent_name = nlu_data['intent']
            intent_score = nlu_data['intent_score']
            entities = nlu_data['entities']
        else: ## Command intent
            intent_name = message.replace("\\","")
            intent_score = 1.0
            entities = []

        ## Dialoque Managment
        responses = self.dm.next_responses(intent_name, intent_score, entities, session_id)
        
        DialogTracker.register_message_user(message, intent_name, intent_score, entities, session_id)
        
        template_responses = [{ "utter_template": response['response'], "message": get_template_response(response['response'])} for response in responses]
        
        for response in template_responses:
            DialogTracker.register_message_bot(response['message'], response['utter_template'], session_id)
        
        return template_responses

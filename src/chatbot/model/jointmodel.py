from .jointbert import JointBERT
from .utils import tokenize_spacy

import torch
import torch.nn.functional as F
import pickle
from transformers import BertTokenizerFast, BertConfig
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class JointModel:
    def __init__(self, model_type = "JointBERT"):
        self.model_type = model_type

    def load_checkpoint(self, model_checkpoint):

        with open(f"{model_checkpoint}/int2label.pkl", "rb") as f:
            self.int2label = pickle.load(f)
    
        with open(f"{model_checkpoint}/label2int.pkl", "rb") as f:
            self.label2int = pickle.load(f)
        
        with open(f"{model_checkpoint}/ent2label.pkl", "rb") as f:
            self.ent2label = pickle.load(f)

        with open(f"{model_checkpoint}/label2ent.pkl", "rb") as f:
            self.label2ent = pickle.load(f)


        if self.model_type == "JointBERT":
            self.tokenizer = BertTokenizerFast.from_pretrained(model_checkpoint)
            bert_config = BertConfig.from_pretrained(model_checkpoint)
            self.joint_model = JointBERT.from_pretrained(
            model_checkpoint,
            config = bert_config,
            num_intent_labels = len(self.int2label),
            num_slot_labels = len(self.ent2label),
            ).to(device)

    def pretokenize(self, message):
        return tokenize_spacy(message)

    def inference_joint_model(self, message):
        ## Preprocesing

        ## Pretokenizacion
        tokens = self.pretokenize(message)

        ## Tokenization Model
        tokenized_inputs = self.tokenizer(tokens, truncation = True, padding = True, is_split_into_words = True, return_tensors="pt")

        inputs = {k: v.to(device) for k, v in tokenized_inputs.items()}

        ## Inference Model
        with torch.no_grad():
            outputs = self.joint_model(**inputs)
            intent_logits = outputs['intent_logits']
            slot_logits = outputs['slot_logits']
            intent_logits = intent_logits.detach().cpu()
            intent_probs = F.softmax(intent_logits[0], dim = 0)
            intent_label = np.argmax(intent_logits.numpy(), axis = 1)
            intent_score = intent_probs[intent_label[0].item()].item()
            intent_name = self.label2int[intent_label[0]]
            entities_labels = np.argmax(slot_logits.detach().cpu().numpy(), axis = 2)
            entities_names = [ self.label2ent[id] for id in entities_labels[0]]
            
            output_nlu = {"intent": intent_name, "intent_score": intent_score , "entities": []}
            
            entity_words = []
            current_entity = None

            word_ids = tokenized_inputs.word_ids()
            pre_word_id = None
            for idx , word_idx in enumerate(word_ids):
                if word_idx is None or pre_word_id == word_idx:
                    continue
                entity_label = entities_names[idx]
                if current_entity != None:
                    if entity_label == 'O' or current_entity != entity_label[2:]:
                        output_nlu['entities'].append({"value": " ".join(entity_words), 
                                                    "entity":current_entity })
                        current_entity = None
                        entity_words = []
                    
                    if current_entity == entity_label.replace('I-',''):
                        entity_words.append(tokens[word_idx])

                elif current_entity == None and entity_label.startswith('B-'):
                    current_entity = entity_label.replace('B-','')
                    entity_words.append(tokens[word_idx])
                
                pre_word_id = word_idx
            
            if current_entity!= None:
                output_nlu['entities'].append({ "value": " ".join(entity_words), 
                                                "entity":current_entity
                                            })
            return output_nlu
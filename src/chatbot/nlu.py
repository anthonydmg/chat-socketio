from .model.jointmodel import JointModel

model_checkpoint = "src/chatbot/model/joint_bert"

class NLU:
    def __init__(self, model_type = "JointBERT" , with_joint_model = True):
        
        self.with_joint_model = True
        self.model_type = model_type

        if with_joint_model == True:
            self.load_join_model()
        else:
            pass
        
    def load_join_model(self):
        self.joint_model = JointModel(self.model_type)
        self.joint_model.load_checkpoint(model_checkpoint)

  
    def inference(self, message):
        return self.joint_model.inference_joint_model(message)


'''
1.create folder (save new model)
2. comparison new model with new model, accept as well as reject
'''
import os, sys
from typing import Optional
from src.exception import InsuranceException
from src.entity.config_entity import MODEL_FILE_NAME, TRANSFORM_OBJECT_FILE_NAME, TARGET_ENCODER_OBJECT_FILE_NAME

class ModelResolver:
    def __init__(self, model_registry: str = "saved_model",
                 transformer_dir_name = "transformer",
                 target_encoder_dir_name = "target_encoder",
                 model_dir_name = "model"
                 ):
        try:
            self.model_registry = model_registry
            os.makedirs(self.model_registry, exist_ok=True)
            self.transformer_dir_name = transformer_dir_name
            self.target_encoder_dir_name = target_encoder_dir_name
            self.model_dir_name = model_dir_name
            
        except Exception as e:
            raise InsuranceException(e, sys)
        
    def get_latest_dir_path(self)-> Optional[str]:
        try:
            dir_name = os.listdir(self.model_registry)
            if len(dir_name) == 0:
                return None
            dir_name = list(map(int, dir_name))
            latest_dir_name = max(dir_name)
            return os.path.join(self.model_registry, f"{latest_dir_name}")
        
        except Exception as e:
            raise InsuranceException(e, sys)
        
    def get_latest_model_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception("model is not available !!")
            return os.path.join(latest_dir, self.model_dir_name, MODEL_FILE_NAME)
        
        except Exception as e:
            raise InsuranceException(e, sys)
    
    def get_latest_transformer_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception("transform data is not available !!")
            return os.path.join(latest_dir, self.transformer_dir_name, TRANSFORM_OBJECT_FILE_NAME)
        
        except Exception as e:
            raise InsuranceException(e, sys)
    
    def get_latest_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception("Target encoder data is not available !!")
            return os.path.join(latest_dir, self.target_encoder_dir_name, TARGET_ENCODER_OBJECT_FILE_NAME)
        
        except Exception as e:
            raise InsuranceException(e, sys)
        
    def get_latest_save_dir_path(self)-> str:
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                return os.path.join(self.model_registry, f"{0}")
            
            latest_dir_num = int(os.path.basename(self.get_latest_dir_path()))
            return os.path.join(self.model_registry, f"{latest_dir_num + 1}")
        
        except Exception as e:
            raise InsuranceException(e, sys)
        
    def get_latest_save_model_path(self):
        try:
            latest_dir = self.get_latest_model_path
            return os.path.join(latest_dir, self.model_dir_name, MODEL_FILE_NAME)
            
        except Exception as e:
            raise InsuranceException(e, sys)
        
    def get_latest_save_transform_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir, self.transformer_dir_name, TRANSFORM_OBJECT_FILE_NAME)
            
        except Exception as e:
            raise InsuranceException(e, sys)
        
    def get_latest_save_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir, self.target_encoder_dir_name, TARGET_ENCODER_OBJECT_FILE_NAME)
            
        except Exception as e:
            raise InsuranceException(e, sys)




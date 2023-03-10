from src.entity import artifact_entity, config_entity
from src.exception import InsuranceException
import os, sys
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
import pandas as pd
import numpy as np
from src.config import TARGET_COLUMN
from sklearn.preprocessing import LabelEncoder
from src import utils
from src.logger import logging
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from src.predictor import ModelResolver

class ModelEvaluation:
    def __init__(self, model_evaluation_config : config_entity.ModelEvaluationConfig,
                data_ingestion_artifact: artifact_entity.DataIngestionArtifact,
                data_transformation_artifact: artifact_entity.DataTransformationArtifact,
                model_trainer_artifact: artifact_entity.ModelTrainingArtifact):
        try:
            self.model_evaluation_config = model_evaluation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver()
        
        except Exception as e:
            raise InsuranceException(e, sys)
        
    def iniatiate_model_evaluation(self)-> artifact_entity.ModelEvaluationArtifact:
        try:
            latest_dir_path = self.model_resolver.get_latest_dir_path() 
            
            if latest_dir_path == None:
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted = True, improved_accuracy = None)
                
            logging.info(f"model evaluation artifact: {model_eval_artifact}")
        
        except Exception as e:
            raise InsuranceException(e, sys)
'''
1. Model define and train model
2. save accuracy for model validation
3. set threshold for accuracy so that we accept or decline the new model.
4. Data is showing underfitting and underfitting.
'''
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


class ModelTrainer():
    def __init__(self, model_trainer_config: config_entity.ModelTrainingConfig,
                 data_transformation_artifact: artifact_entity.DataTransformationArtifact):
        try:
            logging.info(f"**********Model training start****************")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        
        except Exception as e:
            raise InsuranceException(e, sys)
        
    def train_model(self, x, y):
        try:
            logging.info(f"**********start linear regression model training ****************")
            lr = LinearRegression()
            lr.fit(x, y)
            
            return lr
        
        except Exception as e:
            raise InsuranceException(e, sys)
        
    def initiate_model_trainer(self)-> artifact_entity.ModelTrainingArtifact:
        try:
            train_array = utils.load_numpy_array_data(file_path= self.data_transformation_artifact.transform_train_path)
            test_array = utils.load_numpy_array_data(file_path= self.data_transformation_artifact.transform_test_path)
            
            x_train, y_train = train_array[:, : -1], train_array[:, -1]
            x_test, y_test = test_array[:, : -1], test_array[:, -1]
            
            model = self.train_model(x= x_train, y = y_train)
            
            y_prep_train = model.predict(x_train)
            r2_train_score = r2_score(y_true= y_train, y_pred=y_prep_train)
            
            y_prep_test = model.predict(x_test)
            r2_test_score = r2_score(y_true= y_test, y_pred=y_prep_test)
            
            if r2_test_score < self.model_trainer_config.expected_accuracy:
                raise Exception(f"model is not good and model is not able to give expected accuracy : {self.model_trainer_config.expected_accuracy} : model actual score : {r2_test_score}")
            
            diff = abs(r2_train_score - r2_test_score)
            
            if diff > self.model_trainer_config.overfitting_threshold:
                raise Exception(f"train model and test score difference: {diff} is more than threshold: {self.model_trainer_config.overfitting_threshold} and model is shows overfitting")
            
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)
            
            model_trainer_artifact = artifact_entity.ModelTrainingArtifact(
                model_path = self.model_trainer_config.model_path,
                r2_train_score = r2_train_score,
                r2_test_score = r2_test_score
            )
            
            return model_trainer_artifact
            
        except Exception as e:
            raise InsuranceException(e, sys)


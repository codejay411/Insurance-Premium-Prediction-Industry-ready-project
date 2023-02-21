'''1.  impute missing Values
2. outlier handling
3. imbalanced data handling
4. convert categorical data into numerical data. '''

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

class DataTransformation:
    def __init__(self, data_transformation_config: config_entity.DataTransformationConfig,
                 data_ingestion_artifact: artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"**********Data Transformation ****************")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        
        except Exception as e:
            raise InsuranceException(e, sys)
    
    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            simple_imputer = SimpleImputer(strategy='constant', fill_value=0)
            
            robust_scaler = RobustScaler()
            
            pipeline = Pipeline(steps=[
                ('Imputer', simple_imputer),
                ('RobustScaler', robust_scaler )
            ])
            
            return pipeline
        
        except Exception as e:
            raise InsuranceException(e, sys)
    
    def initiate_data_transformation(self)-> artifact_entity.DataTransformationArtifact:
        try:
            logging.info(f"**********Initiate data transformation****************")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            
            input_feature_train_df = train_df.drop(TARGET_COLUMN, axis=1)
            input_feature_test_df = test_df.drop(TARGET_COLUMN, axis=1)
            
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]
            
            logging.info(f"**********Start label encoding ****************")
            label_encoder = LabelEncoder()
            #fit data
            # print("fit data")
            
            target_feature_train_arr = target_feature_train_df.squeeze()
            target_feature_test_arr = target_feature_test_df.squeeze()
            
            for column in input_feature_train_df.columns:
                if input_feature_test_df[column].dtypes == 'O':
                    input_feature_train_df[column] = label_encoder.fit_transform(input_feature_train_df[column])
                    input_feature_test_df[column] = label_encoder.fit_transform(input_feature_test_df[column])
                else:
                    input_feature_train_df[column] = input_feature_train_df[column]
                    input_feature_test_df[column] = input_feature_test_df[column]
                    
            #handle imbalanced data
            # from imblearn.combine import SMOTE
            
            tranformation_pipeline = DataTransformation.get_data_transformer_object()
            tranformation_pipeline.fit(input_feature_train_df)
            
            input_feature_train_arr = tranformation_pipeline.transform(input_feature_train_df)
            input_feature_test_arr = tranformation_pipeline.transform(input_feature_test_df)
            
            logging.info(f"**********Data Transformation save artifact ****************")
            
            train_arr = np.c_[input_feature_train_arr, target_feature_train_arr]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_arr]
            
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transform_train_path, array=train_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transform_test_path, array=test_arr)
            
            utils.save_object(file_path=self.data_transformation_config.transform_object_path, obj=tranformation_pipeline)
            utils.save_object(file_path=self.data_transformation_config.target_encoder_path, obj=label_encoder)
            
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path = self.data_transformation_config.transform_object_path,
                transform_train_path = self.data_transformation_config.transform_train_path,
                transform_test_path = self.data_transformation_config.transform_test_path,
                target_encoder_path = self.data_transformation_config.target_encoder_path 
            )
            
            logging.info(f"**********Data Transformation artifact saved****************")
            
            return data_transformation_artifact
        
        except Exception as e:
            raise InsuranceException(e, sys)
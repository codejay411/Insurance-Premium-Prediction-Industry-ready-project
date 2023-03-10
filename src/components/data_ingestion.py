from email import header
import logging
from operator import index
import pandas as pd
import numpy as np
import os, sys
from src.entity import config_entity
from src.exception import InsuranceException
from src.entity import artifact_entity
from src.utils import get_collection_as_dataframe
from src.logger import logging
from sklearn.model_selection import train_test_split

class DataIngestion:  #data divide train, test and validation
    def __init__(self, data_ingestion_config : config_entity.DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise InsuranceException(e, sys)
    
    def initiate_data_ingestion(self)-> artifact_entity.DataIngestionArtifact:
        try:
            logging.info(f"Export collection data as pandas dataframe")
            df = pd.DataFrame = get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name,
                collection_name=self.data_ingestion_config.collection_name
            )
            logging.info(f"save data in future store !")
            # replace na value with nan
            df.replace(to_replace="na", value = np.NAN, inplace=True)

            # save data in future store
            logging.info(f"create feature store folder if not available")
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir, exist_ok=True)
            logging.info(f"Feature store folder is created successfully")

            logging.info(f"save df to feature store folder")
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path, index=False, header=True)

            logging.info(f"Spliting our data in train and test set. !!")
            train_df, test_df = train_test_split(df, test_size = self.data_ingestion_config.test_size, random_state = self.data_ingestion_config.random_state)

            logging.info(f"Create directary for storing the train dataset. if not exist !!")
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir, exist_ok=True)

            logging.info(f"save dataset to feature store folder of train and test.")
            train_df.to_csv(path_or_buf = self.data_ingestion_config.train_file_path, index=False, header=True)

            test_df.to_csv(path_or_buf = self.data_ingestion_config.test_file_path, index=False, header=True)

            # prepare artifac folder
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path = self.data_ingestion_config.feature_store_file_path,
                train_file_path = self.data_ingestion_config.train_file_path,
                test_file_path = self.data_ingestion_config.test_file_path
            )

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact


        except Exception as e:
            raise InsuranceException(error_message = e, error_detail = sys)
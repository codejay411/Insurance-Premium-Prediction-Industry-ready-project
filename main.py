from src.logger import logging
from src.exception import InsuranceException
import os
import sys
from src.utils import get_collection_as_dataframe
from src.entity.config_entity import DataIngestionConfig
from src.entity import config_entity

# def test_logger_and_exception():
    # try:
    #     logging.info("Stating the test_logger_and_exception")
    #     result = 3/0
    #     print(result)
    #     logging.info("Ending point of the test_logger_and_exception")
    # except Exception as e:
    #     logging.debug(str(e))
    #     raise InsuranceException(e, sys)


if __name__ == "__main__":
    try:
        # test_logger_and_exception()
        # get_collection_as_dataframe(database_name = "Insurance", collection_name = "Insurance_project")
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())


    except Exception as e:
        print(e)
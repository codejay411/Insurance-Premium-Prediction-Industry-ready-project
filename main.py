from src.logger import logging
from src.exception import InsuranceException
import os
import sys
from src.utils import get_collection_as_dataframe
from src.entity.config_entity import DataIngestionConfig
from src.entity import config_entity
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation

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

        # data ingestion
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        
        # data validation
        data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_validation_config=data_validation_config, 
                                         data_ingestion_artifact=data_ingestion_artifact)
        
        data_validation_artifact = data_validation.initiate_data_validation()
        
        #data transformation
        data_transformation_config = config_entity.DataTransformationConfig(
            training_pipeline_config=training_pipeline_config
        )
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config,
                                                 data_ingestion_artifact=data_ingestion_artifact)
        
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        
        # model training
        model_trainer_config = config_entity.ModelTrainingConfig(
            training_pipeline_config=training_pipeline_config
        )
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
        
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        
        # model evaluation
        model_evaluation_config = config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
        model_evaluation = ModelEvaluation(
            model_evaluation_config = model_evaluation_config,
            data_ingestion_artifact = data_ingestion_artifact,
            data_transformation_artifact = data_transformation_artifact,
            model_trainer_artifact = model_trainer_artifact
        )
        
        model_evaluation_artifact = model_evaluation.iniatiate_model_evaluation()


    except Exception as e:
        print(e)
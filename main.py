from src.mlproject3 import logger
from src.mlproject3.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.mlproject3.pipeline.data_validation_pipeline import DataValidationTrainingPipeline
from src.mlproject3.pipeline.data_transformation_pipeline import DataTransformationTraingPipeline
from src.mlproject3.pipeline.model_trainer_pipeline import ModelTrainerTrainingPipeline

# Stage 1 - Data Ingestion
STAGE_NAME = "Data Ingestion Stage"
try:
    logger.info(f">>>>>{STAGE_NAME} started <<<<")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.initiate_data_ingestion()
    logger.info(f">>>> stage {STAGE_NAME} Completed <<<<")
except Exception as e:
    raise e

# Stage 2 - Data Validation
STAGE_NAME = "Model Validation stage"
try:
    logger.info(f">>>>>{STAGE_NAME} started <<<<")
    data_validation = DataValidationTrainingPipeline()  # ← own variable
    data_validation.initiate_data_validation()
    logger.info(f">>>> stage {STAGE_NAME} Completed <<<<")
except Exception as e:
    raise e

# Stage 3 - Data Transformation
STAGE_NAME = "Model Transformation stage"
try:
    logger.info(f">>>>>{STAGE_NAME} started <<<<")
    data_transformation = DataTransformationTraingPipeline()  # ← correct class
    data_transformation.initiate_data_transformation()          # ← correct method
    logger.info(f">>>> stage {STAGE_NAME} Completed <<<<")
except Exception as e:
    raise e


# Stage 4 - Data Transformation
STAGE_NAME = "Model Trainer stage"
try:
    logger.info(f">>>>>{STAGE_NAME} started <<<<")
    model_trainer = ModelTrainerTrainingPipeline()  # ← correct class
    model_trainer.initiate_model_training()          # ← correct method
    logger.info(f">>>> stage {STAGE_NAME} Completed <<<<")
except Exception as e:
    raise e

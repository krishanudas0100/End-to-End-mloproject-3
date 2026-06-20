from src.mlproject3 import logger
from src.mlproject3.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.mlproject3.pipeline.data_validation_pipeline import DataValidationTrainingPipeline
from src.mlproject3.pipeline.data_transformation_pipeline import DataTransformationTraingPipeline
from src.mlproject3.pipeline.model_trainer_pipeline import ModelTrainerTrainingPipeline
from src.mlproject3.pipeline.model_evalutation_pipeline import ModelEvaluationTrainingpipeline

import os
import mlflow

os.environ["MLFLOW_TRACKING_URI"] = "https://dagshub.com/krishanudas0100/End-to-End-mloproject-3.mlflow"
os.environ["MLFLOW_TRACKING_USERNAME"] = "krishanudas0100"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "5048f4d57b38e3a7fe05f3b7e661879acf8613d3"

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


# Stage 5 - Model Evaluation
STAGE_NAME = "Model evaluation stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")

    model_evaluation = ModelEvaluationTrainingpipeline()
    model_evaluation.initiate_model_evaluation()

    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

except Exception as e:
    logger.exception(e)
    raise e
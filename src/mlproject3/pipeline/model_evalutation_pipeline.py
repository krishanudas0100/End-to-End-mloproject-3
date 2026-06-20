from src.mlproject3.config.configuration import ConfigurationManager
from src.mlproject3.components.model_evalutation import ModelEvaluation
from src.mlproject3 import logger

import os

os.environ["MLFLOW_TRACKING_URI"] = "https://dagshub.com/krishanudas0100/End-to-End-mloproject-3.mlflow"
os.environ["MLFLOW_TRACKING_USERNAME"] = "krishanudas0100"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "5048f4d57b38e3a7fe05f3b7e661879acf8613d3"

STAGE_NAME = "Model Evaluation Stage"

class ModelEvaluationTrainingpipeline:
    def __init__(self):
        pass

    def initiate_model_evaluation(self):
        config = ConfigurationManager()

        model_evaluation_config = config.get_model_evaluation_config()

        model_evaluation = ModelEvaluation(
            config=model_evaluation_config
        )

        model_evaluation.logs_into_mlflow()
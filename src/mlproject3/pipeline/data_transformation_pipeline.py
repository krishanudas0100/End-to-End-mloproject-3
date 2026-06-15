from src.mlproject3.config.configuration import ConfigurationManager
from src.mlproject3.components.data_transformation import DataTransformation
from src.mlproject3 import logger
from pathlib import Path

STAGE_NAME = "Data Transformation Stage"

class DataTransformationTraingPipeline:
    def __init__(self):
        pass

    def initiate_data_transformation(self):
        try:
            with open(Path("artifacts/data_validation/status.txt"), 'r') as f:
                status = f.read().split(" ")[-1]  # fix 1: ssplit → split

            if status == "True":  # fix 2: True → "True"
                config = ConfigurationManager()
                data_transformation_config = config.get_data_transformation_config()  # fix 3: wrong method name
                data_transformation = DataTransformation(config=data_transformation_config)
                data_transformation.train_test_split()  # fix 4: train_test_splitting → train_test_split
            else:
                raise Exception("Your data schema is not valid")

        except Exception as e:
            raise e  # fix 5: print(e) → raise e
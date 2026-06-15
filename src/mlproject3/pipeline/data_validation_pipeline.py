from src.mlproject3.config.configuration import ConfigurationManager
from src.mlproject3.components.data_validation import DataValidation
from src.mlproject3 import logger


STAGE_NAME = "Data Validation Stage"  # ← also fix the stage name

class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def initiate_data_validation(self):
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()  # ← fix here
        data_validation = DataValidation(config=data_validation_config)
        data_validation.validate_all_columns()
        

if __name__ == '__main__':
    try:
        logger.info(f">>>>>{STAGE_NAME} started <<<<")
        obj = DataValidationTrainingPipeline()
        obj.initiate_data_validation()
        logger.info(f">>>> stage {STAGE_NAME} Completed <<<<")

    except Exception as e:
        logger.exception(e)
        raise e
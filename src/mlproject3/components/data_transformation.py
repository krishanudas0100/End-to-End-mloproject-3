import os
from src.mlproject3 import logger
from sklearn.model_selection import train_test_split
from src.mlproject3.entity.config_entity import DataTransformationConfig
import pandas as pd

from sklearn.model_selection import train_test_split as sklearn_train_test_split

class DataTransformation:
    def __init__(self, config):  # ← remove the type hint (can't self-reference)
        self.config = config

    def train_test_split(self):
        data = pd.read_csv(self.config.data_path)

        train, test = sklearn_train_test_split(data)  # ← use sklearn, not self.train_test_split()

        train.to_csv(os.path.join(self.config.root_dir, "train.csv"), index=False)
        test.to_csv(os.path.join(self.config.root_dir, "test.csv"), index=False)  # ← fixed "test_csv" → "test.csv"

        logger.info("Splited data into training and test sets")
        logger.info(train.shape)
        logger.info(test.shape)

        print(train.shape)
        print(test.shape)

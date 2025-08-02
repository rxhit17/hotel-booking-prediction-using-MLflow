import os
import pandas as pd
from google.cloud import storage 
from src.custom_exception import CustomException
from src.logger import get_logger 
from config.path_config import * 
from sklearn.model_selection import train_test_split
from utils.common_function import read_yaml 

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self,config):
        self.config = config["data_ingestion"]
        self.bucket_name= self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_test_ration = self.config["train_ratio"]

        os.makedirs(RAW_DIR, exist_ok= True)
        logger.info(f"data ingestion started with {self.bucket_name} and file name {self.file_name}")


    def download_file_from_gcp(self):
        try:
             client = storage.Client()
             bucket = client.bucket(self.bucket_name)
             blob = bucket.blob(self.file_name)

             blob.download_to_filename(RAW_FILE_PATH)

             logger.info(f" CSV file is downloaded successfully to {RAW_FILE_PATH}")

        except CustomException as e:
            logger.error("error while downloading the csv file ")
            raise CustomException("failed to download csv file ",e)

    def split_data(self):
        try:
            logger.info("starting the split data")
            data = pd.read_csv(RAW_FILE_PATH)
            train_data, test_data  =train_test_split(data,test_size=1-self.train_test_ration,random_state=42)

            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(Test_file_path)

            logger.info(f" train data is save to {TRAIN_FILE_PATH}")

        except CustomException as e:
            logger.error("error while splitting data  ")
            raise CustomException("failed to split data into training and testing data ",e)
    
    def run(self):
        try:
            logger.info("data ingestion is started ")
            self.download_file_from_gcp()
            self.split_data()
            logger.info(" data ingestion is completed successfully")
        except CustomException as ce:
            logger.error(f"customeException :{str(ce)}")     
        finally:
                logger.info("data ingestion completed")

if __name__ == "__main__" :
    
    data_ingestion = DataIngestion(read_yaml(config_path))
    data_ingestion.run()

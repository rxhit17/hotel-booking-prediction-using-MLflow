from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTraining
from utils.common_function import read_yaml
from config.path_config import *


if __name__ =="__main__":

    ### 1. data ingestion #
    data_ingestion = DataIngestion(read_yaml(config_path))
    data_ingestion.run()

    ## 2. data processing 
    processor = DataProcessor(TRAIN_FILE_PATH,Test_file_path,PROCESS_DIR,config_path)
    processor.process()

    ### 3 model training 
    trainer = ModelTraining(PROCESS_TRAIN_DATA,PROCESS_TEST_DATA,MODEL_OUTPUT_PATH)
    trainer.run()
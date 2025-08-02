import os
########### DATA ingection ###################################################################

RAW_DIR ="artifacts/raw"
RAW_FILE_PATH =os.path.join(RAW_DIR,'raw_file.csv')
TRAIN_FILE_PATH =os.path.join(RAW_DIR,'train_file.csv')
Test_file_path =os.path.join(RAW_DIR,'test_file.csv')


config_path ="config/config.yaml"


##################### data processing ###############

PROCESS_DIR = "artifacts/process"
PROCESS_TRAIN_DATA = os.path.join(PROCESS_DIR,"process_train_data.csv")
PROCESS_TEST_DATA = os.path.join(PROCESS_DIR,"PROCESS_test_data.csv")

##################### MODEl traing ###########################

MODEL_OUTPUT_PATH = "artifacts/models/lgbm_model.pkl"
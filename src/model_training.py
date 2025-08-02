import os
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb 
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.model_params import *
from config.path_config import *
from utils.common_function import read_yaml,load_data
from scipy.stats import randint
import mlflow
import mlflow.sklearn



logger = get_logger(__name__)
class ModelTraining:

    def __init__(self,train_path,test_path,model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path
        self.params_dist = LIGHTGM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS


    def load_and_split_data(self):
        try:
            logger.info(f"Loading data froom {self.train_path}")
            train_df = load_data(self.train_path)

            logger.info(f"Loading data froom {self.test_path}")
            test_df = load_data(self.test_path)

            X_train = train_df.drop(columns=["booking_status"])

            Y_train = train_df["booking_status"]

            X_test = test_df.drop(columns=["booking_status"])
            Y_test = test_df["booking_status"]

            logger.info("data splitted successfully for Model Training ")

            return X_train,Y_train,X_test,Y_test
        except Exception as e:
            logger.error(f"Error while loading data {e}")
            raise CustomException("failed to load data", e)
        

    def train_lgbm(self,X_train,Y_train):
        try:
            logger.info("Intializing our model")
            lgbm_model = lgb.LGBMClassifier(random_state=self.random_search_params["random_state"])

            logger.info("starting our Hyperparamater tuning ")

            random_search = RandomizedSearchCV(
                estimator= lgbm_model,
                param_distributions=self.params_dist,
                n_iter=self.random_search_params["n_iter"],
                cv=self.random_search_params["cv"],
                n_jobs=self.random_search_params["n_jobs"],
                verbose=self.random_search_params["verbose"],
                random_state=self.random_search_params["random_state"],
                scoring=self.random_search_params["scoring"]
                
            )

            logger.info("starting our Hyperparamater training")

            random_search.fit(X_train,Y_train)

            logger.info("Hyperparamater tuning completed")
            best_param =random_search.best_params_
            best_lgbm_model = random_search.best_estimator_

            logger.info(f"best param :{best_param}")

            return best_lgbm_model
        except Exception as e:
            logger.error(f"Error while training model data {e}")
            raise CustomException("failed to train model", e)
        
    def evaluate_model(self,model,X_train,Y_train):
        try:


            logger.info("evaluating our model ")
            y_pred = model.predict(X_train)
            accuracy = accuracy_score(Y_train,y_pred)
            recall = recall_score(Y_train,y_pred)
            f1 = f1_score(Y_train,y_pred)
            precision = precision_score(Y_train,y_pred)


            logger.info(f"Accuracy score :{accuracy}")
            logger.info(f"Recall score : {recall}")
            logger.info(f"f1 score :{f1}")
            logger.info(f"precision score ,{precision}")

            return{
                "accuracy ": accuracy,
                "precison" :precision,
                "recall" : recall,
                "f1": f1                       
                }
        except Exception as e:
            logger.error(f"Error while evaluating  model  {e}")
            raise CustomException("failed to evaluate model", e)
        

    def save_model(self,model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path),exist_ok= True)

            logger.info("saving the model")
            joblib.dump(model, self.model_output_path)
            logger.info(f"model save to {self.model_output_path}")
        except Exception as e:
            logger.error(f"Error while saving  model  {e}")
            raise CustomException("failed to save  model", e)
        
    def run(self):
        try:
            with mlflow.start_run():
                logger.info("staring our model training pipeline")

                logger.info("starting our mlflow experimentation")

                logger.info("loging the testing and  dataset to MLflow ")

                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")

                X_train,Y_train,X_test,Y_test=self.load_and_split_data()

                best_lgbm_model = self.train_lgbm(X_train,Y_train)

                metrics =self.evaluate_model(best_lgbm_model,X_test,Y_test)

                self.save_model(best_lgbm_model)

                logger.info("logging to the model into mlflow")

                mlflow.log_artifact(self.model_output_path )

                logger.info("logging to params and MLFlow")
                #mlflow.log_param(best_lgbm_model.get_params())
                
                for key, value in best_lgbm_model.get_params().items():
                          mlflow.log_param(key, value)
                mlflow.log_metrics(metrics)
                logger.info("Model Training sucesfully completed  ")

        except Exception as e:
            logger.error(f"Error while model training pipeline {e}")
            raise CustomException("failed during model training pipeline", e)
        

if __name__ == "__main__":
    trainer = ModelTraining(PROCESS_TRAIN_DATA,PROCESS_TEST_DATA,MODEL_OUTPUT_PATH)
    trainer.run()
    
        
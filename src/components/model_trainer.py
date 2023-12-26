import os,sys
from src.logger import logging
from xgboost import XGBRegressor
from dataclasses import dataclass
from sklearn.metrics import r2_score
from catboost import CatBoostRegressor
from src.exception import CustomException
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from src.utils import evaluate_models, save_object,Load_Object
from sklearn.ensemble import AdaBoostRegressor,RandomForestRegressor,GradientBoostingRegressor








@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join('artifacts','model.pkl')


class ModelTrainer:
    def __init__(self) -> None:
        self.model_trainer_config=ModelTrainerConfig()   

    def initiate_model_trainer(self,train_arr,test_arr):
        try:
            Xtrain,ytrain,Xtest,ytest=(train_arr[:,:-1],train_arr[:,-1],test_arr[:,:-1],test_arr[:,-1])
            params={
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                 
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Linear Regression":{},
                "XGBRegressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "CatBoosting Regressor":{
                    'depth': [6,8,10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    # 'loss':['linear','square','exponential'],
                    'n_estimators': [8,16,32,64,128,256]
                }
                
            }
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }

            model_report:dict=evaluate_models(Xtrain=Xtrain,ytrain=ytrain,Xtest=Xtest,ytest=ytest,models=models,param=params)

            best_model_score=max(model_report.values())
            best_model_name=list(model_report)[list(model_report.values()).index(best_model_score)]
            bestmodel=models[best_model_name]


            bestmodel = models[best_model_name]

            if best_model_score<0.6:
                raise CustomException("No best model found",sys)
            logging.info(f"Best model found on both training and testing dataset")

            logging.info(f'best model {bestmodel} saved as pkl file')
            save_object(file_path=self.model_trainer_config.trained_model_file_path,obj=bestmodel)

            model=Load_Object(self.model_trainer_config.trained_model_file_path)

            ypredicted=model.predict(Xtest)

            r2_scr=r2_score(ytest,ypredicted)

            logging.info(f'from model trainer predit model {model} r2score {r2_scr}')

            return r2_scr

        except Exception as e:
            raise CustomException(e,sys)


    
import sys
import os
import dill
from src.logger import logging
from src.exception import CustomException
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score


def save_object(file_path,obj):
    try:
        dir_name=os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)

        with open(file_path,'wb') as file_obj:
            dill.dump(obj,file_obj) 

    except Exception as e:
        raise CustomException(e,sys)
    


def evaluate_models(Xtrain,ytrain,Xtest,ytest,models,param):
    try:
        report={}
        model_list=list(models)
        for i in range(len(models)):
            model=models[model_list[i]]
            parameter=param[model_list[i]]
            logging.info(f'Model List {model_list}')

            logging.info(f'current model {model} and parameters {parameter}')

            gs=GridSearchCV(model,parameter,cv=3)
            gs.fit(Xtrain,ytrain)

            logging.info('identified best parameters by GridSearchCV.')

            model.set_params(**gs.best_params_)
            model.fit(Xtrain,ytrain)

            logging.info(f'model {model} trained.')

            ytrain_predict=model.predict(Xtrain)
            ytest_predict=model.predict(Xtest)

            logging.info('model Predicted.')


            train_model_score=r2_score(ytrain,ytrain_predict)
            test_model_score=r2_score(ytest,ytest_predict)

            report[model_list[i]]=test_model_score
            logging.info(f'model Score {test_model_score}.')

        return report

    except Exception as e:
        raise CustomException(e,sys)
    



def Load_Object(file_path):
    try:
        with open(file_path,'rb') as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e,sys)
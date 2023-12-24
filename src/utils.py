import sys
import os
import dill
from src.logger import logging
from src.exception import CustomException


def save_object(file_path,obj):
    try:
        dir_name=os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)

        with open(file_path,'wb') as file_obj:
            dill.dump(obj,file_obj) 

    except Exception as e:
        raise CustomException(e,sys)
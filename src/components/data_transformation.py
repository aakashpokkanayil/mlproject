import os
import sys
import numpy as np
import pandas as pd
from  src.logger import logging
from src.utils import save_object
from dataclasses import dataclass
from src.exception import CustomException
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler,OneHotEncoder



@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"preprocessor.pkl")

class DataTransformation:
    def __init__(self) -> None:
        self.data_transformation_config=DataTransformationConfig() 

    def get_data_transformer_object(self):
        '''this function provide transformer obj'''

        try:

            num_col=["writing_score", "reading_score"]
            cat_col=[
                    "gender",
                    "race_ethnicity",
                    "parental_level_of_education",
                    "lunch",
                    "test_preparation_course",
                ]
            
            num_tranformation=Pipeline(steps=[
                ('SimpleImputerWithMedian',SimpleImputer(strategy='median')),
                ('StandardScaler',StandardScaler())

            ])

            cat_transformer=Pipeline(steps=[
                ('SimpleImputerWithMode',SimpleImputer(strategy='most_frequent')),
                ('OneHotEncoder',OneHotEncoder()),
                ('StandardScaler',StandardScaler(with_mean=False))

            ])

            preprocessor=ColumnTransformer(transformers=[
                ('num_tranformation',num_tranformation,num_col),
                ('cat_transformer',cat_transformer,cat_col)
            ])

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
    

    def initiate_data_transformation(self,traindata_path,testdata_path):
        '''Data Transformation is done inside this function.'''
        try:
            traindata=pd.read_csv(traindata_path)
            testdata=pd.read_csv(testdata_path)
            logging.info('train and test data collected.')

            preprocessorobj=self.get_data_transformer_object()
            target_col='math_score'

            input_feature_train_df=traindata.drop(columns=[target_col])
            target_feature_train_df=traindata[target_col]

            input_feature_test_df=testdata.drop(columns=[target_col])
            target_feature_test_df=testdata[target_col]

            input_feature_train_arr=preprocessorobj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessorobj.transform(input_feature_test_df)
            logging.info('preprocessing completed.')

            train_arr=np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr=np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

            
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessorobj
            )
            logging.info('saved preprocessobj as pkl file.')

            logging.info('returning train and test data.')
            return (train_arr,test_arr,self.data_transformation_config.preprocessor_obj_file_path)
        except Exception as e:
            raise CustomException(e,sys)





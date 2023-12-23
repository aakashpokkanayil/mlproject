import pandas as pd
import os
import sys
from  src.exception import CustomException
from src.logger import logging
from sklearn.model_selection import train_test_split
from  dataclasses import dataclass


@dataclass
class DataIngestionConfig:
    '''This class contais paths required for Data Ingestion class.'''
    train_data_path:str=os.path.join('artifact','train.csv')
    test_data_path:str=os.path.join('artifact','test.csv')
    raw_data_path:str=os.path.join('artifact','raw.csv')


class DataIngestion:
    '''DataIngestion class will fetch data from diff data sources and split train and test and put it to their folder. this fn also return path of train and test.'''
    def __init__(self) -> None:
        self.ingestion_config=DataIngestionConfig()


    def Initiate_Data_Ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            df=pd.read_csv('notebook/data/stud.csv') # read
            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True) # create a dir with name artifact.

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True) # put raw data in to artifact.

            logging.info("Train test split initiated")
            train_set,test_set=train_test_split(df,test_size=.2,random_state=42) # Spliting data in to train and test.

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Ingestion of the data is completed")

            return (self.ingestion_config.train_data_path,self.ingestion_config.test_data_path)


        except  Exception as e:
            raise CustomException(e,sys)
        
if __name__=='__main__':
    obj=DataIngestion()
    obj.Initiate_Data_Ingestion()
    logging.info('logginng comblited')



import sys,os
import numpy as np
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from flask import Flask,request,render_template
from src.pipeline.predict_pipeline import CustomData,PredictPipeline


application=Flask(__name__)

app=application

## route for home page

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    try:
        if request.method=='GET':
            return render_template('home.html')
        else:
            data=CustomData(gender=request.form.get('gender'),
                            race_ethnicity=request.form.get('ethnicity'),
                            parental_level_of_education=request.form.get('parental_level_of_education'),
                            lunch=request.form.get('lunch'),
                            test_preparation_course=request.form.get('test_preparation_course'),
                            reading_score=request.form.get('reading_score'),
                            writing_score=request.form.get('writing_score')

                            )
            
            pred_df=data.get_data_as_data_frame()
            logging.info('DataFrame constructed for Prediction in app.py.')

            pipline=PredictPipeline()

            results=pipline.Predict(pred_df)
            logging.info('Prediction completed in app.py.')
            result=results[0]

            logging.info('Prediction Data is returning to UI from app.py.')
            return render_template('home.html',results=result)
        
    except Exception as e:
        raise CustomException(e,sys)     
    

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True,port=8080)
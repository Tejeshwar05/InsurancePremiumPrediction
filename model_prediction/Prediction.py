# performing important imports
import pandas as pd
import os
import numpy as np
from flask import render_template
from application_logging import logger
from prediction_data_validation.prediction_data_validation import PredictionDataValidation
from preprocessing.Preprocessing_data import PreProcessing
from file_operation.file_handler import File_Handler
#from db_operations.database import DataBase


class Prediction:
    def __init__(self):
        self.log_writer = logger.App_Logger()
        #self.database=DataBase()
        #self.database.connect_db()
        self.file_object = open("Prediction_logs/Prediction.txt","w+")
        self.pred_data_val = PredictionDataValidation()

    def predict(self):
        """
        This function applies prediction on the provided data
        :return: output- Prediction
                 probablity- Probablity of predicted class
        """

        try:
            self.log_writer.log(self.file_object, 'Start of Prediction')
            preprocessing = PreProcessing()
            # initializing FileHandler object
            file_handler = File_Handler()
            # getting the data file path
            file = os.listdir('Input_data/')[0]
            # reading data file
            dataframe = pd.read_csv('Input_data/'+file)
            data = dataframe.copy()
            data = preprocessing.encode_data(data, 'Region')
            data = np.array(data)
            print(data)
            # loading Gradient Boosting Regressor model
            gradient_boosting_regressor = file_handler.load_model('GradientBoostingRegressor')
            # predicting
            predicted = gradient_boosting_regressor.predict(data)
            # probability = gradient_boosting_classifier.predict_proba(data)[0]
            # output = 'may be default' if predicted == 1 else 'may not default'
            # probability = round(max(probability) * 100, 2)
            self.log_writer.log(
                self.file_object,
                'Predction complete!!. Exiting Predict method of Prediction class ')
            # self.logger.database.close_connection()
            return np.round(predicted, 2)

        except Exception as e:
            self.log_writer.log(
                self.file_object,
                'Error occured while running the prediction!! Message: ' + str(e))
            raise e
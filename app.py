import os.path
import pandas as pd
from flask_cors import cross_origin
from flask import Flask, request, render_template, redirect, url_for
from db_operations.database import DataBase
from prediction_data_validation.prediction_validation import PredictionValidation
from prediction_data_validation.prediction_data_validation import PredictionDataValidation
from model_prediction.Prediction import Prediction
from preprocessing.Preprocessing_data import PreProcessing
from application_logging import logger
import shutil
from delete_prediction_logs.Delete_Prediction_logs import Del_Pred_logs

app = Flask(__name__)
log_writer= logger.App_Logger()



@app.route("/", methods=["GET"])
@cross_origin()
def home():
    """
    This function initiates the home page
    :return: html
    """

    try:
        del_logs = Del_Pred_logs()
        """deleting previous logs"""


        del_logs.create_log_file("Prediction_logs/")

        #creating Prediction_logs Directory

        file_object = open("Prediction_logs/app.txt", "a+")
        log_writer.log(file_object,"entered into homepage")

        pred_data_val = PredictionDataValidation()
        # deleting Input_data folder
        if os.path.isdir('Input_data/'):
            pred_data_val.delete_input_files()

        #connecting to database
        db = DataBase()
        db.connect_db()

        if db.is_connected():
            log_writer.log(file_object, "database  connected")
            db.create_tables()
            log_writer.log(file_object, 'database connected and created table successfully')
        else:
            log_writer.log(file_object,"database not connected")
        db.close_connection()
        log_writer.log(file_object,"database closed suceesfully@app")


        # creating Input_data folder
        pred_data_val.create_prediction_files('Input_data')
        column_info = pred_data_val.get_schema_values()
        region = column_info[0]
        log_writer.log(file_object, 'App started. Exiting method...')
        return render_template('index.html', data={'region': region})
    except Exception as e:
        log_writer.log(file_object,f'Exception occured in initating or creation/deletion of Input_data directory. Message: {str(e)}')
        raise e
@app.route('/input', methods=['POST'])
@cross_origin()
def manual_input():
    """
    This function helps to get all the manual input provided by the user
    :return: html
    """

    try:
        file_object = open("Prediction_logs/app.txt", "a+")
        log_writer.log(file_object, 'Getting input from Form')
        # getting data
        if request.method == 'POST':
            input_data = []
            pred_data_val = PredictionDataValidation()
            required_columns = pred_data_val.get_schema_values()[2]
            columns = pred_data_val.get_schema_values()[1]
            selected = request.form.to_dict(flat=False)
            for i, v in enumerate(selected.keys()):
                if v in columns.keys():
                    property_col = columns[v][selected[v][0]]
                    input_data.append(property_col)
                else:
                    input_data.append(selected[v][0])
            pd.DataFrame([input_data], columns=required_columns).to_csv('Input_data/input.csv', index=False)



        return redirect(url_for('predict'))
    except Exception as e:
        message = 'Error :: ' + str(e)
        log_writer.log(file_object, f'Error occured in getting input from Form. Message: {str(e)}')



@app.route('/predict', methods=['GET'])
@cross_origin()
def predict():



    try:

        file_object = open("Prediction_logs/app.txt", "a+")
        log_writer.log(file_object, 'Entered into predict function@app')
        #logger.log(table_name, 'Prediction Initiated..', 'Info')
        pred_val = PredictionValidation()
        # initiating validstion
        pred_val.validation()
        df = pd.read_csv("Input_data/input.csv")
        AGE = df["Age"][0]
        BMI = df["Bmi"][0]
        SEX = df["Sex"][0]
        SMOKER = df["Smoker"][0]
        CHILDREN = df["Children"][0]
        REGION = df["Region"][0]
        db = DataBase()
        db.connect_db()
        if db.is_connected():
            db.insert_data(AGE, BMI, SEX, CHILDREN, SMOKER, REGION)
        else:
            log_writer.log(file_object, "unable to enter data into database")
        log_writer.log(file_object, "entered input data into the database successfully@app")
        db.close_connection()
        log_writer.log(file_object, "signout from db@app")

        pred = Prediction()
        # calling perdict to perform prediction
        output = pred.predict()
        log_writer.log(file_object, 'Prediction for data complete')
        return render_template('predict.html', result={"output": output})
    except Exception as e:
        raise e


if __name__ == '__main__':
    app.run(debug=True)



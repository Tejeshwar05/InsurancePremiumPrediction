# performing important imports
import json
import os
import shutil
import pandas as pd
import numpy as np
from application_logging import logger


class PredictionDataValidation:
    def __init__(self):
        self.log_writer = logger.App_Logger()
        self.schema = 'prediction_schema.json'
        self.file_object = open("Prediction_logs/PredictionDataValidation.txt", "w+")

    def delete_input_files(self):
        """
        Deletes the prediction_logs directory and it's content
        """
        try:

            self.log_writer.log(self.file_object,
                'Entered deletePredictionFiles method of PredictionDataValidation class')

            shutil.rmtree('Input_data/')
            self.log_writer.log(self.file_object,'Input_data deleted.')
        except Exception as e:
            self.log_writer.log(
                self.file_object,
                'Error occured in deleting folder in deletePredictionFiles method of \
                PredictionDataValidation class. Message: '+str({e}))
            self.log_writer.log(self.file_object,'Failed to delete folder.')
            raise e

    def create_prediction_files(self,folder_name):
        """
        Creates new directory
        :param folder_name: Name of the folder to create
        """
        self.folder_name=folder_name
        try:

            self.log_writer.log(
                self.file_object,
                'Entered create_PredictionFiles method of PredictionDataValidation class')
            os.mkdir(f'{self.folder_name}/')
            self.log_writer.log(self.file_object, 'Input_data created.')
        except Exception as e:

            self.log_writer.log(self.file_object,
                               " Error occured in creating folder in createPredictionFiles method \
                               of PredictionDataValidation class. Message:  + str({e})")
            self.log_writer.log(self.file_object,
                                'Failed to create folder.')
            raise e


    def get_schema_values(self):
        """
        Retrives important data from Schema
        :return:
        """


        try:

            self.log_writer.log(self.file_object, 'Entered getSchemaValue method of PredictionDataValidation class')
            with open(self.schema, 'r') as f:
                dic = json.load(f)
                f.close()
            column_names = dic["columnNames"]
            region = dic["region"]
            required_columns = dic["RequiredColumns"]

            message = "region: "+str(region)+"\t"+"RequiredColumns: "+str(required_columns)+"\n"
            self.log_writer.log(self.file_object, message)

        except ValueError as v:
            message = "ValueError:Value not found inside Schema_prediction.json"
            self.log_writer.log(self.file_object, message)
            raise v

        except KeyError as k:
            message = "KeyError:key value error incorrect key passed"
            self.log_writer.log(self.file_object, message)
            raise k

        except Exception as e:
            self.log_writer.log(self.file_object, str(e))
            raise e
        # returning tuple of these 3 values
        return region, column_names, required_columns

    def validate_data_type(self):
        """
        Validate the incoming datatype
        """


        try:
            self.log_writer.log(self.file_object, 'Entered ValidateDataType method of PredictionDataValidation class')
            data = pd.read_csv('Input_data/input.csv')
            for i in data.columns:
                if data[[i]].dtypes[0] == np.int64 or data[[i]].dtypes[0] == np.float64:
                    pass
                elif i == 'Region' and data[[i]].dtypes[0] == np.dtype('O'):
                    pass
                else:
                    self.log_writer.log(self.file_object, 'Failed valiadtion. Exiting.....')
                    raise Exception('Different Datatype found..')
            self.log_writer.log(
                self.file_object,
                'Datatype validation complete exiting ValidateDataType method of PredictionDataValidation class')
        except Exception as e:
            self.log_writer.log(self.file_object, 'Error occured in Validating datatypes. Message: '+str(e))
            self.log_writer.log(self.file_object, 'Failed to validate datatype. Exiting.....')
            raise e

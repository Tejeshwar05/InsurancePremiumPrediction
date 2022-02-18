import pandas as pd
from application_logging import logger
from file_operation.file_handler import File_Handler


class PreProcessing:
    def __init__(self):
        self.file_object = open("Prediction_logs/PreProcessing.txt", 'w+')
        self.log_writer = logger.App_Logger()

    def encode_data(self, data, column):
        """
        :param data:
        :param column:
        :return:
        """

        try:
            self.log_writer.log(self.file_object, "Starting encoding of data")
            file_handler = File_Handler()
            encoder = file_handler.load_model('OneHotEncoder')
            encoded_data = pd.DataFrame(encoder.transform(data[[column]]))
            data.drop([column], axis=1, inplace=True)
            data = pd.concat([data, encoded_data], axis=1, join='inner')
            self.log_writer.log(self.file_object, "Encoding complete exiting")
            return data
        except Exception as e:
            self.log_writer.log(self.file_object, "An error has ocured while performing encoding. Error: " + str(e))
            raise e

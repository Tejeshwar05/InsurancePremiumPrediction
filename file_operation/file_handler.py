import pickle
from application_logging import logger

class File_Handler:
    def __init__(self):
        self.log_writer = logger.App_Logger()
        self.file_object = open("Prediction_logs/file_handler_Log.txt", 'w+')
        self.model_path = "models/"

    def load_model(self, filename):
        try:

            self.log_writer.log(self.file_object, "Entered into load_model func!!")

            with open(self.model_path + filename + '.sav', 'rb') as f:

                self.log_writer.log(
                    self.file_object, ' loaded. Exiting loadModel method of FileHandler class')
                return pickle.load(f)
        except Exception as e:
            self.log_writer.log(self.file_object, "unable to load the model file in the file handler class.")
            raise e

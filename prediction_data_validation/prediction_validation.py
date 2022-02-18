# performing important imports
from application_logging import logger
from prediction_data_validation.prediction_data_validation import PredictionDataValidation


class PredictionValidation:
    def __init__(self):
        self.raw_data = PredictionDataValidation()
        self.log_writer = logger.App_Logger()
        self.file_object = open("Prediction_logs/PredictionValidation.txt", "w+")

    def validation(self):
        """
        Calling the validation
        """

        try:
            self.log_writer.log(self.file_object, "Validation started for Prediction Data")
            # validating Datatype
            self.log_writer.log(self.file_object, "Starting datatype validation")
            self.raw_data.validate_data_type()
            self.log_writer.log(self.file_object, "Datatype validation complete!!")
        except Exception as e:
            self.log_writer.log(self.file_object, "Error ocurred while performing validation. Error: " + str(e))
            raise e
import os.path
import shutil


class Del_Pred_logs:
    def __init__(self):
        pass



    def create_log_file(self, folder_name):
        self.folder_name = folder_name
        if os.path.isdir("Prediction_logs/"):
            pass
        else:
            os.mkdir(f'{self.folder_name}')

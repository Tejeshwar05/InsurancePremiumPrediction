from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from configparser import ConfigParser


class DataBase:
    def __init__(self):
        config = ConfigParser()
        config.read('config/config.ini.txt')
        config.sections()
        self.cloud_config = {
            'secure_connect_bundle': config["database"]["path"]
        }
        self.auth_provider = PlainTextAuthProvider(config['database']['clientid'], config['database']['clientsecret'])
        self.session = None

    def connect_db(self):
        """
        Connecting to the database
        """
        try:
            cluster = Cluster(cloud=self.cloud_config, auth_provider=self.auth_provider)
            self.session = cluster.connect()
        except Exception as e:
            raise e

    def insert_data(self, AGE,BMI,SEX,CHILDREN,SMOKER,REGION):

        """
        :param region: region
        :param smoker: smoker
        :param children: children
        :param sex:gender
        :param bmi: bmi
        :param age: age will be entered from ui

data is keyspace and t is table name
        """

        try:
            if self.is_connected():

                data = self.session.prepare(
                    f"INSERT INTO data.t(age,bmi,sex,children,smoker,region) VALUES(?,?,?,?,?,?)")
                self.session.execute(data, [AGE,BMI,SEX,CHILDREN,SMOKER,REGION])

            else:
                raise Exception('Database not connected')
        except Exception as e :
            raise e



    def create_tables(self):
        """
        Create table if don't exist
        """

        try:
            table = self.session.execute("SELECT * FROM system_schema.tables WHERE keyspace_name= 'data' ;")
            if table:
                return
            else:
                self.session.execute(
                    "CREATE TABLE data.t( \
                    age int,bmi int ,sex int,children int, smoker int,region text, PRIMARY KEY(age)) ;")

        except Exception as e:
            raise e

    def is_connected(self):
        """
        Check is database is connected
        :return: True- Connected
                 False- Not Connected
        """

        try:
            if self.session:
                return True
            else:
                return False
        except Exception as e:
            raise e

    def close_connection(self):
        """
        Close database connection
        """

        try:
            if not self.session.is_shutdown:
                self.session.shutdown()
        except Exception as e:
            raise e

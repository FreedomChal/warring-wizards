import sys
import os
import sqlite3

ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/../../../"

def convert_to_dict(column_values, columns):

    dict = {columns[i]: column_values[i] for i in range(len(columns))}

    return dict

class Connection:
    def __init__(self, database = ROOT_DIRECTORY + "database.db"):
        self.database = database

    def connect(self):
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

        return self.cursor

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.commit()
        self.close()

    def close(self):
        self.connection.close()

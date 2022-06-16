import pyodbc as pyo
import pandas as pd


class AzureConnection:
    def __init__(self):
        cnn_azure = (
            r"Driver={SQL Server};Server=catalog-website"
            ".database.windows.net;Database=Catalog;UID=emckevitt;PWD=Olives6515!@;"
        )
        self.cnn = pyo.connect(cnn_azure)

    def execute(self, sql):
        try:
            return pd.read_sql(sql, self.cnn)
        except Exception as e:
            pass

    def close(self):
        self.cnn.close()
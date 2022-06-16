from azure_connect import AzureConnection
import pandas as pd
import pyodbc as pyo
import numpy as np

az = AzureConnection()

result = az.execute("""
SELECT * FROM [dbo].[all_courses];
""")
print(result)

az.close()
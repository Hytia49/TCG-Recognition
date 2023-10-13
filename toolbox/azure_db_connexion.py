import pypyodbc as odbc
import textwrap
import pandas as pd
import sys
import os

# Local imports
parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) 
sys.path.append(parent)

from settings import DRIVER, SERVER, DATABASE, USERNAME, PASSWORD


connection_string = f"Driver={DRIVER};Server={SERVER},1433;Database={DATABASE};Uid={USERNAME};Pwd={PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

conn = odbc.connect(connection_string)

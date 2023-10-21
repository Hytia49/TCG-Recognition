from configparser import ConfigParser
import os
from pathlib import Path

DIR_PATH = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


PROCESSED_PATH = os.path.join(DIR_PATH,'tcg-recognition','data', 'processed')
RAW_PATH = os.path.join(DIR_PATH,'tcg-recognition','data', 'raw')
IMGS_PATH = os.path.join(DIR_PATH,'tcg-recognition','data', 'imgs')

# Azure db part

CONF_INI_PATH = os.path.join(DIR_PATH, 'tcg-recognition')

parser = ConfigParser()
parser.read(f"{CONF_INI_PATH}\conf.ini")

DRIVER = parser['settings']['driver']
SERVER = parser['settings']['server']
DATABASE = parser['settings']['database']
USERNAME = parser['settings']['username']
PASSWORD = parser['settings']['password']

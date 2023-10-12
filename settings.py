import os
from pathlib import Path

DIR_PATH = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


DF_PATH = os.path.join(DIR_PATH,'tcg-recognition','data', 'processed')
import os
import pandas as pd
import urllib.request
import sys

sys.path.append('../')

from settings import PROCESSED_PATH, IMGS_PATH

if len(os.listdir(PROCESSED_PATH)) != 0 :
    database = pd.read_csv(f'{PROCESSED_PATH}\\dataframe_pokemon.csv', index_col=[0])
else:
    print('The database does not exist')

for i in range(5):
        
    if not os.path.exists(f"{IMGS_PATH}\\{database['nameserie'][i]}") :

        os.makedirs(f"{IMGS_PATH}\\{database['nameserie'][i]}")

    urllib.request.urlretrieve(database['urlimgcard'][i], f"{IMGS_PATH}\\{database['nameserie'][i].replace(':', '')}\\{database['numcard'][i].replace('/','_')}.{database['urlimgcard'][i][-3:]}")



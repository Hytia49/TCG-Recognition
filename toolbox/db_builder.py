import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import sys

sys.path.append('../')

from settings import DF_PATH

start_time = time.time()

# Get the site with all pokemon series are referenced
soup_all = BeautifulSoup(requests.get("https://www.pokecardex.com/series").text, 'lxml')
# Find img and url blocks div
all_url = soup_all.find_all('a', {'class' : 'd-block no-decoration-link text-reset'})
all_name_series = soup_all.find_all('img', {'class' : 'img-fluid symbole'})

# Initialise urls & names_serie lists, and the dict_ that will contain all the useful variables
urls = []
names_serie = []
dict_ = {}

# Iterate through the soup element
for element in all_url :
    url = element['href'].replace('//', 'https://')
    urls.append(url)

for element in all_name_series : 
    name_serie = element['alt']
    names_serie.append(name_serie)


# Transform dict_ to dataframe (not mandatory, but I prefere work with df)
dict_['Urls_serie'] = urls
dict_['Nom_serie'] = names_serie
df_serie_and_url = pd.DataFrame(dict_)

# Create the final dict which will become the final dataframe and the final database
dict_for_df = {'Name':[], 'Number':[], 'Serie':[], 'URL_img':[]}
# Initialise list which contain wrong soup (possible if the html code has mistakes)
error_element = []

# Iterate through urls list
for url in urls : 
    
    # Initialize url img list and serie names list 
    imgs = []
    names = []

    # Get the general URL serie and serie's name
    df_unique_name_and_url = df_serie_and_url[df_serie_and_url['Urls_serie'] == url]
    df_unique_name_and_url = df_unique_name_and_url.reset_index()

    # Stock the serie's name in a variable
    serie_name = df_unique_name_and_url['Nom_serie'][0]

    soup = BeautifulSoup(requests.get(url).text, 'lxml')

    # Get all the card img block
    all_pokemon_name_and_number = soup.find_all('img', {'class' : 'img-fluid br-10 dark-shadow'})


    for element in all_pokemon_name_and_number:
        # if alt is not empty, if it's empty -> mistake in the html code
        if element['alt'] != "":

            dict_for_df['Name'].append(' '.join(element['alt'].split()[:-1]))
            dict_for_df['Number'].append(element['alt'].split()[-1])
            dict_for_df['Serie'].append(serie_name)
            dict_for_df['URL_img'].append(element['src'].replace("//", "https://"))
    
        else:
            # Transforme the mistake html code to the standard site html code to get the name card
            str_list = list(str(element).replace('=""/>', '="" />').split(" "))
            string_list = []

            for s in str_list:

                # Condition not
                if '=""' in s and s != 'alt=""':
                    s = s.replace('=""', "")
                    string_list.append(s)

            element_clean = BeautifulSoup(str(element).replace('alt=""', f'alt="{" ".join(string_list)}"'), features='lxml')
            all_pokemon_name_and_number = element_clean.find_all('img', {'class' : 'img-fluid br-10 dark-shadow'})

            for element_clean in all_pokemon_name_and_number:

                dict_for_df['Name'].append(' '.join(element_clean['alt'].split()[:-1]))
                dict_for_df['Number'].append(element_clean['alt'].split()[-1])
                dict_for_df['Serie'].append(serie_name)
                dict_for_df['URL_img'].append(element_clean['src'].replace("//", "https://"))


# Transform dict to df and save the databse in the processed folder
dataframe = pd.DataFrame(dict_for_df)
dataframe.to_csv(f'{DF_PATH}\\dataframe_pokemon.csv')
print(time.time() - start_time)
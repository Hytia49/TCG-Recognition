from bs4 import BeautifulSoup
import pandas as pd
import pyodbc
import requests
import sys

sys.path.append('../')

from settings import PROCESSED_PATH, DRIVER, DATABASE, SERVER


def csv_creation():
    """
    Create a csv file that represents the fr pokemon cards normal series database in the data/processed folder.
    """
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

    # Remove special series : Divers, MCDonald's, World championships, Trainer kits and promos
    del urls[len(urls) - 102:]
    del names_serie[len(names_serie) - 102:]

    # Remove Legendary Treasures serie because it's english series only
    urls.remove('https://www.pokecardex.com/series/LTR')
    names_serie.remove('Legendary Treasures')

    # Transform dict_ to dataframe (not mandatory, but I prefere work with df)
    dict_['Urls_serie'] = urls
    dict_['Nom_serie'] = names_serie
    df_serie_and_url = pd.DataFrame(dict_)
    df_serie_and_url.to_csv(f'{PROCESSED_PATH}\\dataframe_pokemon_serie.csv')    

    # Create the final dict which will become the final dataframe and the final database
    dict_for_df = {'namecard':[], 'numcard':[], 'nameserie':[], 'urlimgcard':[]}

    # Iterate through urls list
    for url in urls : 

        # Get the general URL serie and serie's name
        df_unique_name_and_url = df_serie_and_url[df_serie_and_url['Urls_serie'] == url]
        df_unique_name_and_url = df_unique_name_and_url.reset_index()

        # Stock the serie's name in a variable
        serie_name = df_unique_name_and_url['Nom_serie'][0]

        soup = BeautifulSoup(requests.get(url).text, 'lxml')

        # Get all the card img block
        all_pokemon_name_and_number = soup.find_all('img', {'class' : 'img-fluid br-10 dark-shadow'})
        all_url_hd = soup.find_all('a', {'class':'fancybox'})


        for element in all_pokemon_name_and_number:
            # if alt is not empty, if it's empty -> mistake in the html code
            if element['alt'] != "":

                dict_for_df['namecard'].append(' '.join(element['alt'].split()[:-1]))
                dict_for_df['numcard'].append(element['alt'].split()[-1])
                dict_for_df['nameserie'].append(serie_name)
        
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

                    dict_for_df['namecard'].append(' '.join(element_clean['alt'].split()[:-1]))
                    dict_for_df['numcard'].append(element_clean['alt'].split()[-1])
                    dict_for_df['nameserie'].append(serie_name)

                for element_clean in all_url_hd : 

                    dict_for_df['urlimgcard'].append(element_clean['href'].replace('//', 'https://'))

        for element in all_url_hd : 

            dict_for_df['urlimgcard'].append(element['href'].replace('//', 'https://'))

    # Transform dict to df and save the databse in the processed folder
    dataframe = pd.DataFrame(dict_for_df)
    dataframe.index.rename('idcard', inplace=True)
    dataframe.to_csv(f'{PROCESSED_PATH}\\dataframe_pokemon.csv')

def database_connexion(driver : str, server : str, database : str):
    """
    This function return the connexion with sql server local database
    Arguments should be initialize in the conf.ini file

    args:
        str : the driver sql database
        str : server name
        str : database name

    return:
        pyodbc.Connection : connexion with sql server
        pyodbc.Cursor : cursor
    """

    conn = pyodbc.connect(f'DRIVER={driver}; SERVER={server};DATABASE={database};Trusted_Connection=yes;')

    cursor = conn.cursor()
    print(type(conn))
    return conn, cursor

def database_csv_upload(conn : pyodbc.Connection, cursor : pyodbc.Cursor, csv_file : str):
    """
    This function create the Pokemon Cards tables
    
    args : 
        pyodbc.Cursor : cursor
        str : the csv file

    """
    cursor.execute('''
                    CREATE TABLE Tcg(
                        idtcg INTEGER,
                        nametcg VARCHAR(100),
    
                    );
                   
                    CREATE TABLE Serie(
                        idserie INTEGER,
                        idtcg INTEGER,
                        nameserie VARCHAR(100),
                        anneeserie INTEGER,
                    )
                   
                   CREATE TABLE Card(
                        idcard INTEGER,
                        idserie INTEGER,
                        namecard VARCHAR(100),
                        numcard VARCHAR(50),
                        typecard INTEGER,
                        languagecard VARCHAR(50),
                        urlimgcard VARCHAR(200)

                   )
                ''')

    tcgdataframe = pd.DataFrame(pd.read_csv(csv_file))

    for index, row in tcgdataframe.iterrows() :
        print(row)

        cursor.execute(f"""
                INSERT INTO Tcg(idtcg, nametcg)
                VALUES(0, 'Pokemon');  

                INSERT INTO Serie(idserie, idtcg, nameserie, anneeserie)
                VALUES (0,0,'{row['nameserie']}',2000);

                INSERT INTO Card(idcard, idserie, namecard, numcard, typecard, languagecard, urlimgcard)
                VALUES ({row['idcard']},0,'{row['namecard']}','{row['numcard']}',0,'fr', '{row['urlimgcard']}');
                """)
        
    conn.commit()

csv_creation()
conn, cursor = database_connexion(DRIVER, SERVER, DATABASE)
database_csv_upload(conn, cursor, f'{PROCESSED_PATH}\\dataframe_pokemon.csv')

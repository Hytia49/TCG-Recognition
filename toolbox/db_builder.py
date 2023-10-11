import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd

start_time = time.time()

soup_all = BeautifulSoup(requests.get("https://www.pokecardex.com/series").text, 'lxml')
all_url = soup_all.find_all('a', {'class' : 'd-block no-decoration-link text-reset'})
all_name_series = soup_all.find_all('img', {'class' : 'img-fluid symbole'})

urls = []
names_serie = []
dict_ = {}

for element in all_url :
    url = element['href'].replace('//', 'https://')
    urls.append(url)

for element in all_name_series : 
    name_serie = element['alt']
    names_serie.append(name_serie)

dict_['Urls'] = urls
dict_['Nom_serie'] = names_serie

df = pd.DataFrame(dict_)

dict_for_df = {'Name':[], 'Number':[], 'Serie':[], 'URL_img':[]}

for url in urls : 
    
    # soup = BeautifulSoup(requests.get(url).text, "lxml")

    # images = soup.find_all("img", {"class": "img-fluid br-10 dark-shadow"})

    # done_names = []

    # for i, img in enumerate(images):

    #     name = img["alt"].split("/")[-1].split(".")[0]
    #     img_url = img["src"].replace("//", "https://")

    #     response = requests.get(img_url).content

    #     done_names.append(name)

    #     with open(f"data/{name}.png", "wb+") as file:
    #         file.write(response)

    #     print(f"{datetime.now() }    {name}    {i+1}/{len(images)}")
    #     time.sleep(0.1) 
    # print(done_names)
    # print(time.time() - start_time)
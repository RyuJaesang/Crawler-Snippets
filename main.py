import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

base_url = 'https://www.imsdb.com/'

#Get movie list ( Select Genre )
res = requests.get(base_url + 'genre/Action')
res_html = BeautifulSoup(res.content, 'html.parser')
res_movie_list_html = res_html.select('#mainbody > table:nth-child(3) p > a')

movie_title_list = []
for i in range(len(res_movie_list_html)):
    movie_title_list.append(res_movie_list_html[i].text.replace(" ", "-"))

#Get each movie script
csv_index = 0
for i in range(len(movie_title_list)):
    if i >= 100:
        break

    script_res = requests.get(base_url + 'scripts/' + movie_title_list[i] + '.html')
    print('Action' + str(csv_index) + '.txt')
    print(base_url + 'scripts/' + movie_title_list[i] + '.html')
    script_html = BeautifulSoup(script_res.content, 'html.parser')

    #For two case of Page's HTML structure
    script_list = script_html.select('#mainbody > table:nth-child(3) tr > td > pre pre')
    if len(script_list) == 0:
        script_list = script_html.select('#mainbody > table:nth-child(3) tr > td > pre')

    #Crawling Fail
    if (len(script_list) != 0):
        script = script_list[0].get_text()

        constraint = re.compile("<[a-z]>")
        match = re.search(constraint, script)

        if not match:
            script = script.replace(",", "").replace(".", "").replace("-", "").replace("'", "").replace('"', "").replace("?", "").replace("(", "").replace(")", "").replace(";", "").replace(":", "").replace("`", "").lower()
            text = open('./data/Action' + str(csv_index) + '.txt', mode='wt', encoding='utf-8')
            text.write(script)
            text.close()
            csv_index=csv_index+1
        else:
            print("Ooooops")





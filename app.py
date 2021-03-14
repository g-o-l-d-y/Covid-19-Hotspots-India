import folium
# importing the required libraries
import pandas as pd

# Visualisation libraries
import matplotlib.pyplot as plt
from flask import Flask, render_template, request


# Manipulating the default plot size
plt.rcParams['figure.figsize'] = 10, 12

# Disable warnings 
import warnings
warnings.filterwarnings('ignore')
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

state=[]
content=[]
image=[]
d={}

app=Flask(__name__)

@app.route("/")
def home():
  my_url = "https://news.google.com/covid19/map?hl=en-IN&mid=%2Fm%2F03rk0&gl=IN&ceid=IN%3Aen"
    
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    
    containers = page_soup.findAll("tbody", {"class": "ppcUXd"})
    container = containers[0]
    
    state = container.findAll("div",{"class":"pcAJd"})
    total_case = container.findAll("td",{"class":"l3HOY"})
    
    state=[state[i].text for i in range(0,len(state))]
    total_case = [total_case[i].text for i in range(0,len(total_case))]
    
    total_case = [total_case[i] for i in range(0,len(total_case),5)]
    total_case = [total_case[i].split(',') for i in range(0,len(total_case))]
    total_case = [int("".join(map(str,total_case[i]))) for i in range(0,len(total_case))]
    
    India_coord = pd.read_excel('Indian Coordinates.xlsx')
    lat = list(India_coord['Latitude'])
    long = list(India_coord['Longitude'])
    st = list(India_coord['Name of State / UT'])
    d = {st[i]:[lat[i],long[i]] for i in range(0,len(st))}
    
    del state[0]
    del state[0]
    
    del total_case[0]
    del total_case[0]
    
    myMap = folium.Map(location=[20, 70], zoom_start=4,tiles='Stamenterrain')
    for i in range(0,len(state)):
        folium.CircleMarker(d[state[i]], popup = ('<strong>State</strong>: ' + state[i] + '<br>''<strong>Total Cases</strong>: ' + str(total_case[i]) + '<br>'),color='red',fill_color='red' ).add_to(myMap)
    
    # Generate map
    myMap.save('templates/map.html')
    return render_template("home.html")

if __name__ == '__main__':
    app.run()

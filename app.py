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
    
    d = {'Andaman and Nicobar Islands': [11.66702557, 92.73598262], 'Andhra Pradesh': [14.7504291, 78.57002559], 'Arunachal Pradesh': [27.10039878, 93.61660071], 'Assam': [26.7499809, 94.21666744], 'Bihar': [25.78541445, 87.4799727], 'Chhattisgarh': [22.09042035, 82.15998734], 'Dadra and Nagar Haveli and Daman and Diu': [20.26657819, 73.0166178], 'Delhi': [28.6699929, 77.23000403], 'Goa': [15.491997, 73.81800065], 'Haryana': [28.45000633, 77.01999101], 'Himachal Pradesh': [31.10002545, 77.16659704], 'Jammu and Kashmir': [33.45, 76.24], 'Jharkhand': [23.80039349, 86.41998572], 'Karnataka': [12.57038129, 76.91999711], 'Kerala': [8.900372741, 76.56999263], 'Lakshadweep': [10.56257331, 72.63686717], 'Madhya Pradesh': [21.30039105, 76.13001949], 'Maharashtra': [19.25023195, 73.16017493], 'Manipur': [24.79997072, 93.95001705], 'Meghalaya': [25.57049217, 91.8800142], 'Mizoram': [23.71039899, 92.72001461], 'Nagaland': [25.6669979, 94.11657019], 'Odisha': [19.82042971, 85.90001746], 'Puducherry': [11.93499371, 79.83000037], 'Punjab': [31.51997398, 75.98000281], 'Rajasthan': [26.44999921, 74.63998124], 'Sikkim': [27.3333303, 88.6166475], 'Telangana': [18.1124, 79.0193], 'Tamil Nadu': [12.92038576, 79.15004187], 'Tripura': [23.83540428, 91.27999914], 'Uttar Pradesh': [27.59998069, 78.05000565], 'Uttarakhand': [30.32040895, 78.05000565], 'West Bengal': [22.58039044, 88.32994665], 'Ladakh': [34.1, 77.34], 'Gujarat': [22.2587, 71.1924]}
    
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

@app.route("/option")
def option():
    return render_template("option.html")

@app.route("/content")
def content():
    return render_template("content.html")

@app.route("/map")
def myMap():
    return render_template("map.html")

@app.route("/restriction")
def restriction():
    global state,content,image
    my_url = "https://www.goibibo.com/info/statewise-covid-guidelines/"

    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    
    containers = page_soup.findAll("p", {"class": "state-head pad-t-6"})
    state=[containers[i].text for i in range(0,len(containers))]
    
    containers = page_soup.findAll("p", {"class": "state-sub-txt"})
    content = [containers[i].text for i in range(0,len(containers))]
    
    containers = page_soup.findAll("div", {"class": "state-img"})
    image = [containers[i].img["src"] for i in range(0,len(containers))] 
    
    for i in range(0,len(state)):
        d[state[i]]=[content[i],image[i]]
    
    return render_template("restriction.html",info=d)

if __name__ == '__main__':
    app.run()

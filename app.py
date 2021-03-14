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


app=Flask(__name__)

@app.route("/")
def home():
  return "hi"

if __name__ == '__main__':
    app.run()

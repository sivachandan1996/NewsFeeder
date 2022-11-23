import urllib
from selenium import webdriver
import requests
import time
from bs4 import BeautifulSoup
import re
import argparse
import sys


# Fucntion to Create the URL
def build_url(search_item):
    try:
        google_main_url = 'https://www.google.com/search?'
        params = {'q':search_item,'tbm':'nws'}
        print("Succesfully build the URL \n")
        print(f"The URL is: {google_main_url+urllib.parse.urlencode(params)} \n")
        return google_main_url+urllib.parse.urlencode(params)
    except:
        print("Couldn't build the URL \n")
        return None

# Fucntion to get the HTML PAGE
def get_html(url):
    response = requests.get(url)
    if response:
        print(f'Successfully completed the Search for {search_item} \n')
    else:
        print('An error has occurred. \n')
        return None

    return response.content

#  Fucntion to extract the News out of the HTML
def main_content(html):
    soup  = BeautifulSoup(html,'html5lib')
    divs = soup.findAll('div',attrs={'id':'main'})
    div_element = divs[0].text
    # Pattern for extracting ALL Headlines text
    combined_headlines_pattern = re.compile('weight:bold}([A-Za-z].*[0-9]{1,2}\s(?:hours|days|day|hour)s\sago)')
    combined_headlines = re.findall(combined_headlines_pattern,div_element)
    # Pattern to extract individual Headlines
    individual_headlines_pattern = re.compile('([\w].*?\.{0,3}[0-9]\s(?:hours|days|day|hour)\sago)')
    individual_headlines = re.findall(individual_headlines_pattern,combined_headlines[0])
    return individual_headlines

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='News Feeder App')
    parser.add_argument('-s', metavar='--search', nargs=1,
                    help='The Item we want to search News for',required=True)
    try:
        args = parser.parse_args()
        search_item = sys.argv[2]
        print(f"Scrapping Google News for {search_item} \n")
        url = build_url(search_item)
        if url is not None:
            html = get_html(url)
            if html is not None:
                print(*main_content(html), sep = "\n\n")
    except:
        print("Pass a string along with '-s' to get the scrapped news \n")




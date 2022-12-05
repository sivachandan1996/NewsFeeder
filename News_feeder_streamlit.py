import urllib
import requests
from bs4 import BeautifulSoup
import re
import argparse
import sys
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os 


logging.basicConfig(filename='NewsFeeder.log', encoding='utf-8', level=logging.DEBUG)


def build_url(search_item):
    """
    Creates Google News URL with regards to search_item 

    Arguments:
        search_item: str
                    The Public figure that we are seaching Google News For
    
    Return
        url: str
            The constructed URL for Google News

    """
    try:
        google_main_url = 'https://www.google.com/search?'
        params = {'q':search_item,'tbm':'nws'}
        logging.info("Succesfully build the URL \n")
        logging.info(f"The URL is: {google_main_url+urllib.parse.urlencode(params)} \n")
        return google_main_url+urllib.parse.urlencode(params)
    except UserWarning:
        logging.error("Couldn't build the URL\
                     ..exiting the process")
        return False


# Fucntion to get the HTML PAGE
def get_html(url,search_item):
    """

    Gets the HTML Page of the URL we Built

    Argumnets:
        url: str
            The url we constructed using build_url() function
        search_item: str
                    The Public figure for which we are scrapping the Google News
    
    Return
        response.content: str
                        HTML Page
    
    """
    response = requests.get(url)
    if response.status_code == 200:
        logging.info(f'Successfully completed the Search for {search_item} \n')
        return response.content
    else :
        logging.error(f"Got Status code {response.status_code} \n couldn't retrieve HTML page\
                     ..exiting the process")
        return False

    


def main_content(html,search_item):
    """
    
    Scraps the HTML Page for Headlines using Beautiful Soup

    Arguments:
        html: str
            HTML page we got from get_html() function
        search_item: str
            The public person for whon we are scraping the HTML Page for
    
    Return:
        email_hmtl_body: str
                        Scrapped News embedded in the form of HTML
            
    """
    soup  = BeautifulSoup(html,'html5lib')
    text = soup.find_all(string=re.compile(f"{search_item}|{search_item.title()}"))[1:] # First element is not Headline Hence ignored
    if len(text) == 0:
        logging.warning(f"Regular Expression Didnt Capture the target:{search_item}\
                        ..exiting the process")
        return False
    logging.info("Scrapping completed from the HTML page")
    email_html_body = "<html><body>" 
    for index in  range(0,len(text),2):
        if index == len(text)-1:
            email_html_body = email_html_body+f"<h1>Headline</h1><p>{text[index]}</p>"
        else:
            email_html_body = email_html_body+f"<h1>Headline</h1><p>{text[index]}</p><p>{text[index+1]}</p>"
    email_html_body = email_html_body + "</body></html>"
    return email_html_body



def mail(email_html_body,to_mail,search_item):
    """
    Send the Scrapped News as form of HTML though email(!! Only works if sender has gmail account)

    Arguments:
        email_html_body: str
            HTML containing embedded Scraped Headlines. This is retuned by main_content() Function
        to_mail: str
            Recipient of your HTML embedded mail 
        search_item: str
            The public person for whon we are scraping the HTML Page for
    
    Return:
        True
    """
    from_mail = os.getenv('from_mail') 
    from_password = os.getenv('from_password')
    smtp_server = "smtp.gmail.com" 
    smtp_port = 465
    msg = MIMEMultipart()
    msg['Subject'] = f'Headlines on {search_item}'
    msg['From'] = from_mail
    COMMASPACE = ', '
    msg['To'] = COMMASPACE.join([from_mail, to_mail])
    msg.preamble = f'News on {search_item}'
    msg.attach(MIMEText(email_html_body,'html','utf-8'))

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.ehlo()
        server.login(from_mail, from_password)
        server.sendmail(from_mail, [from_mail, to_mail], msg.as_string())
        logging.info("Completed Sending the email")
        return True
    except UserWarning:
        logging.exception()
        return False


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='News Feeder App')
    parser.add_argument('--search', nargs=1,
                    help='The Item we want to search News for',required=True)
    parser.add_argument('--to_mail',nargs=1,help='The reciepient\'s email',required=True)
    try:
        args = parser.parse_args()
        search_item = args.search[0]
        to_mail = args.to_mail[0]
        logging.info(f"Calling the relevant fucntionts to scarp Google News for {search_item} \n")
        url = build_url(search_item)
        html =get_html(url,search_item)
        email_html_body =main_content(html,search_item)
        mail(email_html_body,to_mail)

    except UserWarning:
        print("Pass a string along with '-s' to get the scrapped news \n")




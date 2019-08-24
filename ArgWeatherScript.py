#!/usr/bin/python3.6
from bs4 import BeautifulSoup
import sys
import requests
import pandas as pd
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.message import MIMEMessage
import argparse

#Adds argparse functionality
parser = argparse.ArgumentParser()
#Adds positional argument and stores the value in the variable dest_email
parser.add_argument("dest_email")

args = parser.parse_args()


#Consider using Travis functionality to encrypt variables in program. Also has cronjob functionality to set up weekly running of script

location_url = "https://forecast.weather.gov/MapClick.php?lat=32.7157&lon=-117.1617#.XS-Gyd-YXO8"

#This sets the variable page to the value of the specified url. In this case, the url contains the weather data to be retrieved
page = requests.get(location_url)

#Using beautiful soup, the soup variable is set equal to the HTML contents of the specified page 
soup = BeautifulSoup(page.content, 'html.parser')

#seven_day is set equal to HTML objects with the id "detailed-forecast". This particular HTML object contains the forecast for the next seven days
seven_day = soup.find(id="detailed-forecast")

#desc contains all HTML objects with class "col-sm-10 forecast-text" WITHIN the previously retrieved HTML object. This information is the weather description for the given time period
desc = soup.find_all(class_="col-sm-10 forecast-text")

#Similar to the above variable, this one contains the time period for each respective weather description
day = seven_day.find_all(class_="col-sm-2 forecast-label")

keys = day
values = desc

#Creates a dictionary with the information gathered in the previous two variables
dictionary = dict(zip(keys, values))

#Creates a list
weather_list = []

#This for loop runs through the dictionary, setting the previous variables equal to "i" and "v", and uses BeautifulSoup functionality to convert the information into strings. The i and v variables are then concatenated into a new variable, which is then appended into the weather_list
for i, v in dictionary.items():
    weather_data = i.string + ": " + v.string
    
    weather_list.append(weather_data)

tonight = weather_list[0]

#print(tonight)

#Email information
email_from_addr = "weatherpythontest007@gmail.com"
email_to_addr = args.dest_email
email_smtp_server = "smtp.gmail.com"
email_smtp_port = "587"
email_user = "weatherpythontest007@gmail.com"
email_pw = "Weathertest2019"
email_sub = "Weather Report"
email_body = str(tonight)

message = MIMEMultipart('alternative')
message['From'] = email_from_addr
message['To'] = email_to_addr
message['Subject'] = email_sub
body = email_body
message.attach(MIMEText(body))

server = smtplib.SMTP(email_smtp_server,int(email_smtp_port))
text = message.as_string()
server.starttls()
server.login(email_user, email_pw)
server.sendmail(email_from_addr,email_to_addr,message.as_string())
server.quit()

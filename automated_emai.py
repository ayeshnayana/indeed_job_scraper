import requests  # For http requests

from bs4 import BeautifulSoup  # For web scraping

import smtplib  # To send the email

# To create the email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# For system date and time manipulation
import datetime

# when sending the email we need the appropriate date on the heading
# To do that we need to get the current date and time
# Also, we can make sure now that the same email will not be repeated everyday
now = datetime.datetime.now()

# Create a empty python string object
# This is a placeholder for the email content
content = ''
records = []


# Extarcting the Hacker News Stories
def get_url(position, location):
    # Generate a url from position and location
    template = 'https://www.indeed.com/jobs?q={}&l={}'
    url = template.format(position, location)
    print(url)
    return url


def extract_jobs(url, position, location):
    print(f"Extracting Indeed {position} jobs in {location}")
    # Create a placeholder for the content
    cnt = ''
    # create the email heading by passing the heading into the placeholder
    cnt += (f"<b>Extracting Indeed {position} jobs in {location} MI:</b>\n'+'<br>'+'-'*50+'<br>")
    # Create the body of the email

    # get the content in the url using the requests and store the info in response
    response = requests.get(url)
    # In the object response there is a method called content.
    # We use the method content to get the content in the response
    content = response.content  # This content is a local field inside the request class

    soup = BeautifulSoup(content, 'html.parser')  # Create a soup of text from the website

    # We want to extract only the table (tb) and the title
    # Using valign we can seperate from one link to another link
    # Since python starts from zero, we need "i+1"
    # Use soup.find_all to find all the 'td'
    # cards = soup.find_all('div', 'job_seen_beacon')
    cards = soup.find_all('a', 'tapItem')
    # print(len(cards))
    return cards
    # card = cards[1]


def get_record(card):
    tag = card.h2.span
    job_title = tag.get('title')
    company_Name = card.find('span', {"class": "companyName"}).text.strip()
    job_url = 'https://www.indeed.com' + card.a.get('href')
    job_Location = card.find('div', 'companyLocation').text
    job_Summery = card.find('li').text.strip()
    job_posted_Date = card.find('span', 'date').text.strip()
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    try:
        job_Salary = card.find('span', 'estimated-salary').text.strip()
    except AttributeError:
        job_Salary = ''

    record = (job_title, company_Name, job_url, job_Location, job_Summery, job_posted_Date)
    return record


def full_record(cards):
    for card in cards:
        record = get_record(card)
        records.append(record)


position = 'work from home'
location = 'grand rapids MI'

url = get_url(position, location)
cards = extract_jobs(url, position, location)
full_record(cards)
print(records[2])

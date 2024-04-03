#!/usr/bin/python3
import locale
import pytz
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import parser
from feedgen.feed import FeedGenerator

class FrenchParserInfo(parser.parserinfo):
    MONTHS = [
        ('Jan', 'Janvier'),
        ('Fév', 'Févr', 'Février'),
        ('Mar', 'Mars'),
        ('Avr', 'Avril'),
        ('Mai',),
        ('Juin',),
        ('Juil', 'Juillet'),
        ('Aoû', 'Août'),
        ('Sep', 'Septembre'),
        ('Oct', 'Octobre'),
        ('Nov', 'Novembre'),
        ('Déc', 'Décembre'),
    ]

def fetch_page():
    resp = requests.get('https://www.lemagit.fr/ressources/Securite')
    resp.raise_for_status()
    page_source = resp.text

    return page_source

def parse_page(html):
    soup    = BeautifulSoup(html, 'html.parser')
    entries = []

    notable = soup.find('ul', class_='new-notable-items')    
    #process notable items
    items = notable.find_all("li")
    for li in items:
        #get the content of the span of class date
        date = li.find('span', class_='date').get_text()
        date = parser.parse(date, FrenchParserInfo())

        data = li.find('h4')
        #get the link of the a in h4
        link = data.find('a').get('href')
        #get the text content the a of the h4
        title= data.find('a').get_text()
        #get the text content of the p in the h4 
        summary = li.find('p').get_text()
        
        entry    = {'pubDate' : date, 'url' : link, 'title' : title, 'summary' : summary}
        entries.append(entry)

    main = soup.find('ul', class_='topic-related-content-list')
    #process full list items
    items = main.find_all("li")
    for li in items:
        #get the content of the span of class date
        date = li.find('span', class_='date').get_text()
        date = parser.parse(date, FrenchParserInfo())

        data = li.find('h3')
        #get the link of the a in h3
        link = data.find('a').get('href')
        #get the text content the a of the h3
        title= data.find('a').get_text()
        #get the text content of the p in the h3 
        summary = li.find('p').get_text()

        entry    = {'pubDate' : date, 'url' : link, 'title' : title, 'summary' : summary}
        entries.append(entry)
        
    entries.reverse()
    return entries

def main():

    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    entries = parse_page(fetch_page())

    fg = FeedGenerator()
    fg.id('https://raw.githubusercontent.com/TechTargetFR/Topical-RSS/main/LeMagIT-cybersecurite-rss.xml')
    fg.title('LeMagIT - Cybersécurité')
    fg.author( {'name':'LeMagIT','email':'editorial@fr.techtarget.com'} )
    fg.language('fr')
    fg.link( href='https://www.lemagit.fr/ressources/Securite', rel='self')
    fg.description('Toute l\'information en cybersécurité avec LeMagIT.')

    for entry in entries:
        fe = fg.add_entry()
        fe.id(entry.get('url'))
        fe.title(entry.get('title'))
        fe.description(entry.get('summary'), isSummary=True)
        fe.link( href=entry.get('url'), rel='self')
#        date = datetime.strptime(entry.get('pubDate'), '%d %b %Y')
#        date = pytz.utc.localize(date)
        date = entry.get('pubDate')
        fe.pubDate(date.astimezone(pytz.timezone('CET')))

    locale.setlocale(locale.LC_TIME, '')
    # Save the output to a file
    fg.rss_str(pretty=True)
    fg.rss_file('./LeMagIT-cybersecurite-rss.xml')

if __name__ == '__main__':
    main()

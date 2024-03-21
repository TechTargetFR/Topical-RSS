#!/usr/bin/python3
import locale
import pytz
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from feedgen.feed import FeedGenerator

authors = [
  'https://www.techtarget.com/contributor/Jim-ODonnell',
  'https://www.techtarget.com/contributor/Patrick-Thibodeau',
  'https://www.techtarget.com/contributor/Don-Fluckinger',
  'https://www.techtarget.com/contributor/Eric-Avidon',
  'https://www.techtarget.com/contributor/George-Lawton',
  'https://www.techtarget.com/contributor/Cameron-McKenzie',
  'https://www.techtarget.com/contributor/Chris-Tozzi',
  'https://www.techtarget.com/contributor/Beth-Pariseau',
  'https://www.techtarget.com/contributor/Esther-Ajao',
  'https://www.techtarget.com/contributor/Tom-Nolle',
  'https://www.techtarget.com/contributor/Alexander-Culafi',
  'https://www.techtarget.com/contributor/Arielle-Waldman',
  'https://www.techtarget.com/contributor/Michael-Cobb',
  'https://www.techtarget.com/contributor/Dave-Shackleford',
  'https://www.techtarget.com/contributor/Andrew-Froehlich',
  'https://www.techtarget.com/contributor/Rob-Wright',
  'https://www.techtarget.com/de/autor/Malte-Jeschke',
  'https://www.techtarget.com/de/autor/Ulrike-Riess',
  'https://www.techtarget.com/de/autor/Tobias-Servaty-Wendehost',
  'https://www.techtarget.com/de/autor/Michael-Eckert',
]

def fetch_page(author):
    resp = requests.get(author)
    resp.raise_for_status()
    page_source = resp.text

    return page_source

def parse_page(html):
    soup    = BeautifulSoup(html, 'html.parser')
    entries = []

    notable = soup.find('ul', class_='contributor-articles-list')    
    #process notable items
    items = notable.find_all("li")
    for li in items:
        #get the content of the span of class date
        date = li.find('span', class_='date').get_text()

        data = li.find('h4')
        #get the link of the a in h4
        link = data.find('a').get('href')
        #get the text content the a of the h4
        title= data.find('a').get_text()
        #get the text content of the p in the h4 
        summary = li.find('p').get_text()
        
        entry    = {'pubDate' : date, 'url' : link, 'title' : title, 'summary' : summary}
        entries.append(entry)
        
    entries.reverse()
    return entries

def main():

    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    entries = parse_page(fetch_page())

    fg = FeedGenerator()
    fg.id('https://raw.githubusercontent.com/TechTargetFR/Topical-RSS/main/TTGT-Authors-rss.xml')
    fg.title('TechTarget - Veille')
    fg.author( {'name':'LeMagIT','email':'editorial@fr.techtarget.com'} )
    fg.language('fr')
    fg.link( href='https://www.lemagit.fr/', rel='self')
    fg.description('Veille sur quelques journalistes de TechTarget.')

    for entry in entries:
        fe = fg.add_entry()
        fe.id(entry.get('url'))
        fe.title(entry.get('title'))
        fe.description(entry.get('summary'), isSummary=True)
        fe.link( href=entry.get('url'), rel='self')
        date = datetime.strptime(entry.get('pubDate'), '%d %b %Y')
        date = pytz.utc.localize(date)
        fe.pubDate(date.astimezone(pytz.timezone('CET')))

    locale.setlocale(locale.LC_TIME, '')
    # Save the output to a file
    fg.rss_str(pretty=True)
    fg.rss_file('./TTGT-Authors-rss.xml')

if __name__ == '__main__':
    main()

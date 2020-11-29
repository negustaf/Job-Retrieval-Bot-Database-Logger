
# Noah Gustafson & Maxton Fil

# commit 2

from bs4 import BeautifulSoup
import requests
import re
import os
import csv

def getKeyword(keyword, locale):
    #soup = BeautifulSoup(requests.get('https://www.linkedin.com/jobs/search?').text, 'html.parser')
    soup = BeautifulSoup(requests.get(f'https://www.linkedin.com/jobs/search?keywords={keyword}&location={locale}-fl&redirect=false&position=1&pageNum=0').text, 'html.parser')
    aTags = soup.find_all("a", class_="result-card__full-card-link")
    print(aTags)
    
    
def getLocation(location):
    pass

def getCompany(company):
    pass

def main():

if __name__ == '__main__':
    main()
    #print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)

# Noah Gustafson & Maxton Fil

# commit 3

from bs4 import BeautifulSoup
import requests
#import re
import os
#import csv

# Function takes in keyword and locale as parameters representing a LinkedIn search keyword and location. 
def jobTupsBySearchParams(keyword, locale):

    # Gets a list of job postings from the LinkedIn search page with specified keyword and locale params.
    link = f'https://www.linkedin.com/jobs/search?keywords={keyword}&location={locale}-fl&redirect=false&position=1&pageNum=0'
    soup = BeautifulSoup(requests.get(link).text, 'html.parser')

    # Finds all h3 links with specified class 'result-card__full-card-link' in each job card and assigns them to aTags. 
    aTags = soup.find_all('a', class_='result-card__full-card-link')

    # Finds all job titles in aTags and appends them to positionTitles.
    positionTitles = []
    for tag in aTags:
        title = tag.find('span', class_='screen-reader-text')
        positionTitles.append(title.text)

    # Finds all URLs in aTags and appends them to urlList.
    urlList = []
    for tag in aTags:
        urlHref = tag['href']
        urlList.append(urlHref)

    # Finds all h4 links with specified class 'job-result-card__subtitle-link' in each job card and assigns them to aTags2. Finds all companies in aTags2 and appends them to companyList.
    aTags2 = soup.find_all('a', class_='job-result-card__subtitle-link')
    companyList = []
    for tag in aTags2:
        companyList.append(tag.text)
    
    # Takes lists from positionTitles, companyList, and urlList and returns the items from each list in a order-respective list of tuples.
    resultList = []
    for i in range(len(positionTitles)):
        tup = (positionTitles[i],companyList[i],urlList[i])
        resultList.append(tup)
    return resultList

def main():
    print(jobTupsBySearchParams("product-designer", "california"))

if __name__ == '__main__':
    main()

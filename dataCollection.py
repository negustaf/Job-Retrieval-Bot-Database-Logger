from bs4 import BeautifulSoup
import requests
#import re
import os
import sqlite3
import time

def createDB(dbName):
    try:
        conn = sqlite3.connect(path+'/'+dbName) #open the database if it already exists!
        cur = conn.cursor()
    except:
        path = os.path.dirname(os.path.abspath(__file__)) #if it does not exist, create it
        
        conn = sqlite3.connect(path+'/'+dbName)
        cur = conn.cursor()

    return cur, conn #either way, return cur and conn.

def writeDB(cur, conn, postingList):
    cur.execute("CREATE TABLE IF NOT EXISTS job_postings (position_title TEXT, company_name TEXT, location TEXT, url TEXT, post_id INTEGER PRIMARY KEY)")

    for posting in postingList:
        title = posting[0]
        company = posting[1]
        url = posting[2]
        location = posting[3]
        id = posting[4]
        cur.execute("INSERT OR IGNORE INTO job_postings (position_title, company_name, location, url, post_id) VALUES (?,?,?,?,?)", (title, company, location, url,id))

    conn.commit()


def scrapeByPosition(positionName): #scrapes data from the entire united states for new positions matching a certain position title
    link = f'https://www.linkedin.com/jobs/search?keywords={positionName}&location=United%2BStates&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&sortBy=DD&redirect=false&position=1&pageNum=0'
    soup = BeautifulSoup(requests.get(link).text, 'html.parser')

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

    locationList = []
    spanTags = soup.find_all("span", class_="job-result-card__location")
    for tag in spanTags:
        locationList.append(tag.text)

    dataIDlist = []
    liTags = soup.find_all("li", class_="result-card")
    for tag in liTags:
        dataIDlist.append(tag['data-id'])

    resultList = []
    for i in range(len(positionTitles)):
        try:
            tup = (positionTitles[i],companyList[i],urlList[i],locationList[i],dataIDlist[i])
            resultList.append(tup)
        except:
            return resultList
    return resultList

def main():

    '''aeList = scrapeByPosition("automotive-engineer")
    curAE, connAE = createDB("Automotive_Engineer.db")
    writeDB(curAE, connAE, aeList)'''

    print("Scraping data")
    uxList = scrapeByPosition("ux-designer")
    
    curUX, connUX = createDB("ux_designer.db")

    writeDB(curUX,connUX, uxList)

    print("\nData collected, pausing 10 seconds...\n")
    time.sleep(10) #pauses the program so LinkedIn doesn't get suspicious

    print("Scraping more data...")
    iaList = scrapeByPosition('data-analyst')
    
    curIA, connIA = createDB("data_analyst.db")

    writeDB(curIA,connIA,iaList)
    print("Done!")
if __name__ == '__main__':
    main()

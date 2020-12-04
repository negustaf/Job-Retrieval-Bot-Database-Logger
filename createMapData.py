import requests
import json
import sqlite3
import os
import time
import csv

def openDB(dbName): #step 0, open database
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+dbName)
    cur = conn.cursor()
    print("Database accessed")
    return cur, conn, path
    #except:
        #print("Database not found, try again")


def getCoordinates(locale): # step 1.2 this gets used by getLocationDict to collect coordinates!

    urlLocation = ''
    for ch in locale:
        if ch == ' ':
            urlLocation += "+"
        if ch != "," and ch != ' ':
            urlLocation += ch.lower()

    key = '0d3fc91aa05cfef42add0028d662785e'
    link = f'http://api.positionstack.com/v1/forward?access_key={key}&query={urlLocation}&limit=1&output=json'
    data1 = requests.get(link)
    data2 = data1.text
    data3 = json.loads(data2)
    dataList = data3['data']
    try:
        lat = dataList[0]['latitude']
        lon = dataList[0]['longitude']
        return [lat,lon]
    except:
        print("Failed to retrieve, trying again...")
        time.sleep(2)
        try:
            data1 = requests.get(link)
            data2 = data1.text
            data3 = json.loads(data2)
            dataList = data3['data']
            lat = dataList[0]['latitude']
            lon = dataList[0]['longitude']
            return [lat,lon]
        except:
            print("Failed to retrieve data twice. Moving on.")

            print(urlLocation)
            print(dataList)
            return ['E', 'E']

def getLocationDict(cur, conn): #step 1.1, get a dict of UNIQUE LOCATIONS, number of postings there, and their coordinates!
    cur.execute("SELECT location FROM job_postings")
    locationList = cur.fetchall()
    locationDict = {}
    #print(locationList.count('Auburn Hills, MI'))
    for tup in locationList:
        locale = tup[0]
        if locale not in locationDict:
            
            coords = getCoordinates(locale)
            locationDict[locale] = [1, coords[0], coords[1]]
            print(locationDict[locale])
            time.sleep(.2)

        else:
            locationDict[locale][0] += 1

    '''for key in locationDict:
        coords = getCoordinates(key)
        for coord in coords:
            locationDict[key].append(coord)'''

    return locationDict
    
def writeCSV(locationDict, path, csvName): #writes csv file that the visualization can use
    f = csv.writer(open(path+'/'+csvName, 'w', newline= ''))
    f.writerow(["Location","Number of Postings","Latitude","Longitude"])
    for entry in locationDict:
        f.writerow([entry, locationDict[entry][0],locationDict[entry][1],locationDict[entry][2]])
    
    


def getNumPostings(cur, conn, locale, dbName): #step 2, gets the number of postings by location
    cur.execute("SELECT position_title FROM job_postings WHERE locations = (?)", (locale))


if __name__ == '__main__':
    #town = "erie+pa"
    #print(town)
    #print(getCoordinates(town))
    cur, conn, path = openDB("Automotive_Engineer.db")
    dicto = getLocationDict(cur, conn)
    writeCSV(dicto, path, "automotive_engineer_map_data.csv")
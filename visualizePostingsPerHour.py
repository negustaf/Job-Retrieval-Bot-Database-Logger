import time
import matplotlib.pyplot as plt
import os
import sqlite3

def openDB(dbName):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+dbName)
    cur = conn.cursor()
    print("Database accessed")
    return cur, conn, path

def checkSize(cur, conn):
    cur.execute("SELECT position_title FROM job_postings")
    results = cur.fetchall()
    return len(results)


def collectForAnHour(path, script):
    print('Performing initial scrape...')
    for i in range(6):
        exec(open(path+'/'+"dataCollection.py").read())
        print("Waiting 10 minutes")
        time.sleep(600)
    print("1 hour of collection finished")

def calculateDifference(ini, final):
    return final - ini

def visualize(x,y):
    x_pos = [i for i, _ in enumerate(x)]

    plt.bar(x_pos, y, color='green')
    plt.xlabel('Job Type')
    plt.ylabel('New Postings')
    plt.title("New Postings in Last Hour")

    plt.xticks(x_pos,x)

    plt.show()

if __name__ == '__main__':
    curUX, connUX, path = openDB("ux_designer.db")
    curIA, connIA, path = openDB("data_analyst.db")

    iaInitCount = checkSize(curIA, connIA)
    uxInitCount = checkSize(curUX, connUX)

    #collectForAnHour(path,"dataCollection.py")
    #exec(open(path+'/'+"dataCollection.py").read())
    '''print('Performing initial scrape...')
    for i in range(6):
        exec(open(path+'/'+"dataCollection.py").read())
        print("Waiting 10 minutes")
        time.sleep(600)
    print("1 hour of collection finished")
'''
    iaFinalCount = checkSize(curIA, connIA)
    uxFinalCount = checkSize(curUX, connUX)

    keyList = ['UX Designer', "Data Analyst"]
    valList = []
    valList.extend([calculateDifference(uxInitCount,uxFinalCount),calculateDifference(iaInitCount,iaFinalCount)])
    visualize(keyList, valList)
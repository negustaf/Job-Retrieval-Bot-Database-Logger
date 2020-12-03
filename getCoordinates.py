import requests
import json

def getCoordinates(locale):
    
    key = '0d3fc91aa05cfef42add0028d662785e'
    link = f'http://api.positionstack.com/v1/forward?access_key={key}&query={locale}&limit=1&output=json'
    data1 = requests.get(link)
    data2 = data1.text
    data3 = json.loads(data2)
    dataList = data3['data']
    
    lat = dataList[0]['latitude']
    lon = dataList[0]['longitude']

    return [lat,lon]


if __name__ == '__main__':
    print(getCoordinates('birmingham-al'))
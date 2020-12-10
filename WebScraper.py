from bs4 import BeautifulSoup
import requests
import os

# Class to be imported to Slack bot.
class WebScraperBot:

    # __init__() takes in slackChannel, keyword, and locale as parameters. Then the class constructor gets html code from the param-specified LinkedIn jobs search page and sets soup as an instance.
    def __init__(self, slackChannel, keyword, locale):
        self.slackChannel = slackChannel
        self.keyword = keyword#.replace(keyword, '-', 1)
        self.locale = locale#.replace(locale, '-', 1)
        link = f'https://www.linkedin.com/jobs/search?keywords={keyword}&location={locale}-fl&redirect=false&position=1&pageNum=0'
        self.soup = BeautifulSoup(requests.get(link).text, 'html.parser')

    # fetchTitles() finds all h3 links with specified class "result-card__full-card-link" in each job card and assigns them to aTags. Then it finds all job titles in aTags and appends them to the list posTitles. It returns posTitles.
    def fetchTitles(self):
        aTags = self.soup.find_all('a', class_='result-card__full-card-link')
        posTitles = []
        for tag in aTags:
            title = tag.find('span', class_='screen-reader-text')
            posTitles.append(title.text)
        return posTitles
    
    # fetchCompanies() finds all h4 links with specified class "job-result-card__subtitle-link" in each job card and assigns them to aTags. Then it finds all companies in aTags and appends them to the list posCompanies. It returns posCompanies.
    def fetchCompanies(self):
        aTags = self.soup.find_all('a', class_='job-result-card__subtitle-link')
        posCompanies = []
        for tag in aTags:
            posCompanies.append(tag.text)
        return posCompanies

    # fetchURLs() again finds all h3 links with specified class "result-card__full-card-link" in each job card and assigns them to aTags. Then it finds all URLs in aTags and appends them to the list posURLs. It returns posURLs.
    def fetchURLs(self):
        aTags = self.soup.find_all('a', class_='result-card__full-card-link')
        posURLs = []
        for tag in aTags:
            urlHref = tag['href']
            posURLs.append(urlHref)
        return posURLs
    
    # combinedPositionTups() takes lists from posTitles, posCompanies, and posURLs and returns the items from each list in an order-respective list of tuples called posData. It returns posData. If the data has no new titles, it returns a message telling the user to try again.
    def combinedPosTups(self):
        posData = []
        if self.fetchTitles() != None:
            for i in range(len(self.fetchTitles())):
                tup = (self.fetchTitles()[i], self.fetchCompanies()[i], self.fetchURLs()[i])
                posData.append(tup)
            return posData
        else:
            return 'There are no new job postings for this position. Try again in 10 seconds.'
    
    # craftPosStr() takes the tuple list from combinedPosTups() and crafts a string from the data to cooperate with the Slack API's message payload requirements. The string stops returning after 5 jobs, 12 pieces of data (3 per job: title, company, url).
    def craftPosStr(self):
        comStr = ''
        count = 0
        for i in self.combinedPosTups():
            comStr += '\n'
            if count != 4:
                count += 1
                comStr += ', '.join(i)
                comStr += '\n\n'
            if count == 4:
                comStr += ', '.join(i)
                return comStr
    
    # insertPositionsIntoSlackMessageDict() takes craftPosStr()'s returned tuple list of recent job position data and puts it into the Slack message dictionary. It returns the dictionary.
    def insertPosIntoSlackMessageDict(self):
        text = self.craftPosStr()
        return {"type": "section", "text": {"type": "mrkdwn", "text": text}},

    # craftMessage() contains a constant, SLACK_MESSAGE, that contains the text formatted to be displayed in the Slack message. It returns the Slack message-compatible dictionary with an output of the various instances.
    def craftMessage(self):
        SLACK_MESSAGE = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    f"The five most recent {self.keyword} positions in {self.locale} are: \n{self.craftPosStr()}"
                ),
            },
        }
        return SLACK_MESSAGE
    # getMessagePayload() crafts a message for the specified channel and returns the entire message payload as a dictionary.
    def getMessagePayload(self):
        return {
            "channel": self.slackChannel,
            "blocks": [
                self.craftMessage(),
                #*self.craftPosStr(),
            ],
        }

# print(WebScraperBot('#job-retriever', 'product-designer', 'california').combinedPosTups())
print(WebScraperBot('#job-retriever', 'product design intern', 'california').craftPosStr())

'''
^ Note On Print():
"#job-retriever" slackChannel parameter is useless without importing "from slack import WebClient"

See RunWebScraperTest.py for import.
'''

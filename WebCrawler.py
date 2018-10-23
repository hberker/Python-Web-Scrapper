import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import csv

class Scraper(object):
    MaxPages = 0
    Connections = []
    Frontier = []
    Visited = []
    Context = []
   
    

    def __init__(self, Filename,Tables, URL):
        print("Crawler crawling...\n")
        self.Outfile = open(Filename, "w")
        self.Writer = csv.writer(self.Outfile)
        self.Writer.writerow(Tables)        
        self.parsePageForLinks(URL)   

    def parsePageForLinks(self, aPage):
        newLink = ""
        soup = BeautifulSoup(requests.get(aPage).text, 'lxml')
        for tag in soup.findAll('a'):
            if tag.get('href'):# and "https://" in tag.get('href'):
                newLink = tag.get('href')
                if "https://" not in newLink:
                    newLink = aPage[0 : len(aPage) - 1] + tag.get('href')
                if newLink not in self.Visited:
                    self.Frontier.append(newLink)


    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True


    def parsePageForString(self, aPage,stringList):
        stringCount = 0
        textOcc = []

        pageContent = requests.get(aPage)
        soup = BeautifulSoup(pageContent.text, 'lxml')
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)
        
        for t in visible_texts:
            t.strip()
            for s in stringList:
                if s in t:
                    #print("found: " + str(t))
                    stringCount+=t.count(s)
                    self.Connections.append(aPage)
                    textOcc.append(t)
                    self.Context.append(t)
        return [str(stringCount), textOcc] 


    def loopEnd(self, page):
        self.Visited.append(page)
        self.Frontier.remove(page)

        set(self.Visited)
        set(self.Frontier)
        set(self.Connections)

        for i in self.Visited:
            if i in self.Frontier:
                self.Frontier.remove(i)
        
    def scrapForFixedData(self,string,dataNeeded):
        visits = 0
        index = 0
        usedData = 0
        while(index < len(self.Frontier) and usedData < dataNeeded):
            link = self.Frontier[index]
            if link not in self.Visited:
                try:
                    returnVal = (self.parsePageForString(link, string))                    
                    if(int(returnVal[0]) > 0):
                        for i in returnVal[1]:
                            if usedData < dataNeeded:
                                self.sendOutData([str(string), returnVal[0], link, i])
                                usedData+=1
                            else:
                                break

                    self.parsePageForLinks(link)
                    visits+=1
                    print("Visited: " + link)
                except:
                    print("Error: " + link)
                
                #self.loopEnd(link)
            else:
                print("Invalid: " + link)
            index += 1
            self.loopEnd(link)
    
    def sendOutData(self, data):#[str(string), returnVal[0], link, i]
        self.Writer.writerow(data)
    def parsePagesForOccurances(self,string, stopAt):#assumes PPFL() has been run
        totalOccurances = 0
        visits = 0
        
        index = 0
        while(index < len(self.Frontier) and visits < stopAt):
            link = self.Frontier[index]
            if link not in self.Visited:
                #try:
                    returnVal = (self.parsePageForString(link, string))
                    totalOccurances += int(returnVal[0])
                    
                    if(int(returnVal[0]) > 0):
                        for i in returnVal[1]:
                            
                            #writer.writerow([str(string), returnVal[0], link, i])
                            self.sendOutData([str(string), returnVal[0], link, i])
                    self.parsePageForLinks(link)
                    visits+=1
                    print("Visited: " + link)
                #except:
                    print("Error: " + link)
                
                    self.loopEnd(link)
            else:
                print("Invalid: " + link)
            index += 1
        #print("\nFound " + string + ": " + str(totalOccurances) + "\nWebsites Visited: " + str(visits))
    

#https://blog.hartleybrody.com/web-scraping-cheat-sheet/#inspecting-the-response
#https://www.reddit.com/r/FortNiteBR/
#'http://www.petercollingridge.co.uk/'
#https://www.buzzfeed.com/
#https://twitter.com/search?q=news&src=typd&lang=en
#https://twitter.com/POTUS
#outfile = open("./scrap.csv", "w") 
#writer = csv.writer(outfile)
#writer.writerow(["Word","Occurances", "Url", "Text"])

scraper = Scraper("./scrap.csv", ["Word","Occurances", "Url", "Text"], 'http://www.startrek.com/')
scraper.scrapForFixedData(["New"],5)


set(scraper.Frontier)
for i in scraper.Connections:
    print("Connection: " + i)

for i in scraper.Context:
    print("Context: " + str(i))
print("Pages Scraped: " + str(len(scraper.Frontier)))
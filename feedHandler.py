from __future__ import print_function
import configReader
import feedparser
import urllib
import time
import json
import os

#
## Goals
#
# 1. Reads a CSV-style file to get the various feed URL's, as well as the
# associated aliases
#
#
# Example format
#
# http://somefeedurl/,The feed alias
# http://anotherFeedUrl/,Alias for the second feed
#
#
# 2. Reads a CSV-style file to get the existing entries for the feeds
#
# Example Format:
#
# http://the_feed_url/,http://entry1/,http://entry2/,http://entry3
# http://second_feed_url/,http://entry1/,http://entry2,http://entry3

#
### Why does this exist, you might ask?
#
# Well, when you try to take a feedparser feed object and create a JSON dump
# of it, you'll normally get a nice TypeError letting you know that the object
# "time.struct_time" is not JSON serializable. This class extends the normal
# JSON encoder and puts in a simple way to serialize a 'time.struct_time'
# object. This is then specified waaaaaay down in the json.dumps() with the
# 'cls=' specifier
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, time.struct_time):
            return list(obj)

        return json.JSONEncoder.default(self, obj)


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def location(file):
    return os.path.join(__location__,file)

def getCListImgs(url):
    # A very nasty technique that attempts to get the list of images from Craigslist.
    try:
        myDat = urllib.urlopen(url).read()

        myDat = myDat.split('imgList = ')[1]
        myDat = myDat.split(';')[0]

        imgList = json.loads(myDat)
    except:
        imgList = []
    return imgList



class feed(object):
    """Object which holds data about feed, as well as feedparser object. """
    def __init__(self, data):
        self.url = data['url']
        self.alias = data['alias']
        self.feedData = self.getFeed()
        self.oldEntries = data['entries']
        self.newEntries = self.getNewEntries()

    def getFeed(self, url=None):
        if not url:
            url = self.url
        feedData = feedparser.parse(url)
        return feedData

    def getNewEntries(self,feedData = None, oldEntries = None):
        if not feedData: feedData = self.feedData
        if not oldEntries: oldEntries = self.oldEntries
        newEntries = []
        for i in range(0, len(feedData['entries'])):
            entry = feedData['entries'][i].link
            if entry not in oldEntries:
                newEntries.append({
                    'url': feedData['entries'][i].link,
                    'summary': feedData['entries'][i].summary,
                    'title' :  feedData['entries'][i].title,
                    'imgs' :   getCListImgs(feedData['entries'][i].link)
                    })

        return newEntries

    def getAllEntries(self):
        allEntries = []

        if self.oldEntries:
            for entry in self.oldEntries:
                allEntries.append(entry)

        for entry in self.newEntries:
            allEntries.append(entry['url']) 
            # Newentries is a list of dictionaries, so we have to get the url
            # attribute from each. Oldentries is just a list of old urls.
        
        return allEntries

    def buildEntryLine(self):
        # Since the "entries.txt" file requires a particular format, this
        # method builds the appropriate string. The gist of the format is:
        #
        #   feed_url,entry1,entry2,entry3,entry4
        #
        # Where feed url is the url of the rss feed, and each entry is a URL
        # that has already been "seen" in the feed.
        toReturn = ""
        entries = self.getAllEntries()

        toReturn+=self.url
        for entry in entries:
            toReturn+=','+entry
        toReturn+='\n'
        return toReturn

    def formatEmail(self):
        # Method to format a message for email.
        toReturn = {}

        # This is a super, super ugly way to build this, but I guess it is
        # what it is.
        text = ""
        
        # I am so sorry for this formatting....
        text += '<br><h1><a href="{}">{}</a></h1><br><ul>'.format(
            self.url,
            "Link to feed '{}'".format(self.alias) # Nested '.formats' *shudders*
        )

        for data in self.newEntries:
            text+= '<li><hr>'
            text+= '<p>\n{}\n<h2><a href="{}">{}</a></h2>\
            \n\t{}<br>'.format(data["url"],data["url"],data['title'],data["summary"])

            for urls in data['imgs']:
                text+= '\t<img src="{}" height="150">\n'.format(urls)

            text+= '</p></li>'

        toReturn['body'] = text
        toReturn['subject'] = 'New from "'+self.alias+'"'

        return toReturn

    def formatSMS(self):
        # Method to format a message to be delivered by SMS (text message)
        toReturn = ""
        for data in self.newEntries:
            toReturn += data["url"] + '\n'

        return toReturn

    def __str__(self):
        # Takes all the data in the object (or at least the most important
        # stuff) and makes a pretty JSON-representation of it.
        def pjp(x): return json.dumps(x, cls = MyEncoder,  sort_keys=True, indent=4, separators=(',', ': '))
        toReturn = {}
        toReturn['url'] = self.url
        toReturn['alias'] = self.alias
        toReturn['oldEntries'] = self.oldEntries
        toReturn['newEntries'] = self.newEntries
        toReturn['writeEntriesLine'] = self.buildEntryLine()
        return pjp(toReturn)


def buildFeeds():
    
    feedData = configReader.getAllFeedData()

    feedObjs = []
    for item in feedData:
        feedObjs.append(feed(item))

    return feedObjs

if __name__ == '__main__':
    buildFeeds()

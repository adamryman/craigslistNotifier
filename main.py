import feedparser
from twilio.rest import TwilioRestClient
import urllib
import os

##Setting up variables
rssfeed = 'http://seattle.craigslist.org/search/sss?catAbb=sss&query=expedit&sort=date&format=rss'
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
entries = {}
newEntries = []

#Setting up Twilio Stuff
accountData = open(os.path.join(__location__,'accountData.txt' ), 'r')

ACCOUNT_SID = accountData.readline().rstrip()
AUTH_TOKEN = accountData.readline().rstrip()
phoneSender = accountData.readline().rstrip()
phoneReciver = accountData.readline().rstrip()

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

##Loading entries file into entries object
entriesFile = open(os.path.join(__location__,'entries.txt'), 'r')
for line in entriesFile:
  entries[line.rstrip()] = True
entriesFile.close()

##get read to append to the entries
entriesFile = open(os.path.join(__location__,'entries.txt'), 'a')

feed = feedparser.parse(rssfeed)

##Go though all the entries, if there ones that were not in the entries
##file before, add them. Also add them to newEntries so we know what data
##to send
for i in range(0, len(feed['entries'])):
  entrie = feed['entries'][i].link
  if entrie not in entries:
    entriesFile.write(entrie + '\n')
    newEntries.append(entrie + "")
    listing = urllib.urlopen(entrie)

##Put all of the links into one string
text = ""
for link in newEntries:
  text += link + '\n'

##If the string is blank send it along
if text is not "":
  client.messages.create(
    from_= phoneSender, to = phoneReciver, body = text
  )

##Close the filestream
entriesFile.close()



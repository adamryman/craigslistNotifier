import feedparser
from twilio.rest import TwilioRestClient
import urllib
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

rssfeed = 'http://seattle.craigslist.org/search/sss?catAbb=sss&query=expedit&sort=date&format=rss'

accountData = open(os.path.join(__location__,'accountData.txt' ), 'r')

ACCOUNT_SID = accountData.readline().rstrip()
AUTH_TOKEN = accountData.readline().rstrip()
phoneSender = accountData.readline().rstrip()
phoneReciver = accountData.readline().rstrip()

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

entries = {}
newEntries = []
entriesFile = open(os.path.join(__location__,'entries.txt'), 'r')

for line in entriesFile:
  entries[line.rstrip()] = True

entriesFile.close()
entriesFile = open(os.path.join(__location__,'entries.txt'), 'a')

feed = feedparser.parse(rssfeed)

for i in range(0, len(feed['entries'])):
  entrie = feed['entries'][i].link
  if entrie not in entries:
    entriesFile.write(entrie + '\n')
    newEntries.append(entrie + "")
    listing = urllib.urlopen(entrie)

text = ""
for link in newEntries:
  text += link + '\n'

if text is not "":
  client.messages.create(
    from_= phoneSender, to = phoneReciver, body = text
  )

entriesFile.close()

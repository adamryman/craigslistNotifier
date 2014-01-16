import feedparser
from twilio.rest import TwilioRestClient
import urllib
import os
import sys

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def location(file):
	return os.path.join(__location__,file)

##Setting up variables
if(len(sys.argv) > 1):
	rssfeed = sys.argv[1]
	open(location('rss.txt'), 'w').write(rssfeed)

if not os.path.exists(location('rss.txt')):
	print "Pass an RSS feed as a string parameter; Exiting."
	sys.exit()
rssfeed = open(location('rss.txt'), 'r')

entries = {}
newEntries = []

#Setting up Twilio Stuff
if not os.path.exists(location('accountData.txt')):
	accountData = open(location('accountData.txt'), 'w')
	accountData.write(raw_input('Twillio ACCOUNT_SID:') + '\n')
	accountData.write(raw_input('Twillio AUTH_TOKEN:') + '\n')
	accountData.write(raw_input('Twillio Phone Number (+19876543210):') + '\n')
	accountData.write(raw_input('Receiving Phone Number (+19876543210):') + '\n')
	accountData.close()

accountData = open(location('accountData.txt'), 'r')

ACCOUNT_SID = accountData.readline().rstrip()
AUTH_TOKEN = accountData.readline().rstrip()
phoneSender = accountData.readline().rstrip()
phoneReciver = accountData.readline().rstrip()

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

##Loading entries file into entries object
if not os.path.exists(location('entries.txt')):
	open(location('entries.txt'), 'w').close()
entriesFile = open(location('entries.txt'), 'r')
for line in entriesFile:
	entries[line.rstrip()] = True
entriesFile.close()

##get read to append to the entries
entriesFile = open(location('entries.txt'), 'a')

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



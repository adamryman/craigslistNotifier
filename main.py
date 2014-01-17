# The MIT License (MIT)

# Copyright (c) 2014 Adam Ryman

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import feedparser
from twilio.rest import TwilioRestClient
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import urllib
import json
import sys
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def location(file):
	return os.path.join(__location__,file)

def getCListImgs(url):
	myDat = urllib.urlopen(url).read()

	myDat = myDat.split('imgList = ')[1]
	myDat = myDat.split(';')[0]

	imgList = json.loads(myDat)
	return imgList


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
text = ""


if not os.path.exists(location('accountData.txt')):
	accountData = open(location('accountData.txt'), 'w')
	if int(raw_input('Which way would you like to receive notifications?:\n\t[0] Twilio\n\t[1] Gmail\n')):
		print "You've selected 'Gmail'"
		accountData.write('GMAIL\n')
		accountData.write(raw_input('Gmail user (user_name@gmail.com):') + '\n')
		accountData.write(raw_input('Gmail password:') + '\n')
	else:
		print "You've selected 'Twilio'"
		accountData.write('TWILIO\n')
		accountData.write(raw_input('Twilio ACCOUNT_SID:') + '\n')
		accountData.write(raw_input('Twilio AUTH_TOKEN:') + '\n')
		accountData.write(raw_input('Twilio Phone Number (+19876543210):') + '\n')
		accountData.write(raw_input('Receiving Phone Number (+19876543210):') + '\n')
		accountData.close()


#
## Get Feed Data
#

##Loading entries file into entries object
if not os.path.exists(location('entries.txt')):
	open(location('entries.txt'), 'w').close()
entriesFile = open(location('entries.txt'), 'r')
for line in entriesFile:
	entries[line.rstrip()] = True
entriesFile.close()

##get read to append to the entries
entriesFile = open(location('entries.txt'), 'a')

feed = feedparser.parse(rssfeed.read())

##Go though all the entries, if there ones that were not in the entries
##file before, add them. Also add them to newEntries so we know what data
##to send
for i in range(0, len(feed['entries'])):
	entry = feed['entries'][i].link
	if entry not in entries:
		entriesFile.write(entry + '\n')
		# newEntries.append(entry + "")
		newEntries.append({
			'link':	feed['entries'][i].link,
			'summary': feed['entries'][i].summary,
			'title' :  feed['entries'][i].title,
			'imgs' :   getCListImgs(feed['entries'][i].link)
			})
		listing = urllib.urlopen(entry) # Why does this exist?



#
## Sending the Data
#
# Sends the data using the method that's specified at the top of the 

accountData = open(location('accountData.txt'), 'r')
sendType = accountData.readline().rstrip()

if sendType == "TWILIO":
	ACCOUNT_SID = accountData.readline().rstrip()
	AUTH_TOKEN = accountData.readline().rstrip()
	phoneSender = accountData.readline().rstrip()
	phoneReciver = accountData.readline().rstrip()

	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

	# Do string processing for 
	for data in newEntries:
		text += data["link"] + '\n'


	##If the string is blank send it along
	if text is not "":
		client.messages.create(
			from_= phoneSender, to = phoneReciver, body = text
		)

	##Close the filestream
	entriesFile.close()

elif sendType == "GMAIL":

	# We do this string formatting here because we format the text differently
	# for emails verses non-emails
	#
	# Additionally, this is currently a really, really ugly way to format
	# html. This could be formatted soooo much better/done in a less hacky
	# way.
	for data in newEntries:
		text+= '<hr>'
		text+= '<p>\n{}\n<h3><a href="{}">{}</a></h3>\
		\n\t{}<br>'.format(data["link"],data["link"],data['title'],data["summary"])

		for links in data['imgs']:
			text+= '\t<img src="{}" height="150">\n'.format(links)
		pass
		text+= '</p>'


	# Taken largely from here: http://stackoverflow.com/a/12424439
	# and here: http://blog.spritecloud.com/2010/03/creating-and-sending-html-e-mails-with-python/

	GMAIL_USER = accountData.readline().rstrip()
	GMAIL_PSWD = accountData.readline().rstrip()

	if text:
		FROM = GMAIL_USER
		TO = GMAIL_USER 
		SUBJECT = "New Results from Feed!"
		EMAIL_BODY = "New Feed Results:\n"+text

		MESSAGE = MIMEMultipart('alternative')
		MESSAGE['subject'] = SUBJECT
		MESSAGE['From'] = FROM
		MESSAGE['To'] = TO
		MESSAGE.preamble = EMAIL_BODY

		text = MIMEText(text,'html')
		MESSAGE.attach(text)

		# Attempt to send email
		try:
			# exit()
			server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
			server.ehlo()
			server.starttls()
			server.login(GMAIL_USER, GMAIL_PSWD)
			server.sendmail(FROM, TO, MESSAGE.as_string())
			server.close()
			print 'Successfully sent email'
		except Exception as e:
			print "Failed to send mail"
			print e


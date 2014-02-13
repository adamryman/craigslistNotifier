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


from twilio.rest import TwilioRestClient
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import feedHandler
import smtplib
import sys
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def location(file):
	return os.path.join(__location__,file)


def checkAccountData(silent = True):
	if not os.path.exists(location('accountData.txt')):
		accountData = open(location('accountData.txt'), 'w')
		if int(raw_input('Which way would you like to receive notifications?:\n\t[1] Twilio\n\t[2] Gmail\n')) == 2:
			print "You've selected 'Gmail'"
			accountData.write('GMAIL\n')
			accountData.write(raw_input('Gmail user (user_name@gmail.com): ') + '\n')
			accountData.write(raw_input('Gmail password: ') + '\n')
		else:
			print "You've selected 'Twilio'"
			accountData.write('TWILIO\n')
			accountData.write(raw_input('Twilio ACCOUNT_SID: ') + '\n')
			accountData.write(raw_input('Twilio AUTH_TOKEN: ') + '\n')
			accountData.write(raw_input('Twilio Phone Number (+19876543210): ') + '\n')
			accountData.write(raw_input('Receiving Phone Number (+19876543210): ') + '\n')
			accountData.close()
	# This is so if this function is used else where it can give the user
	# feedback if there's already account data. However, when it's usually
	# being run silent will be set to false and nothing will be printed.
	elif not silent:
		print "There's already account information entered. If you'd like to \
re-enter account information, delete the 'accountData.txt' file and try again."

def getAccountData():
	accountData = {}
	accountFile = open(location('accountData.txt'), 'r')
	sendType = accountFile.readline().rstrip()
	if sendType == "GMAIL":
		accountData['sendMethod'] = 'GMAIL'
		accountData['GMAIL_USER'] = accountFile.readline().rstrip()
		accountData['GMAIL_PSWD'] = accountFile.readline().rstrip()

	elif sendType == "TWILIO":
		accountData['sendMethod'] = "TWILIO"
		accountData['ACCOUNT_SID'] = accountFile.readline().rstrip()
		accountData['AUTH_TOKEN'] = accountFile.readline().rstrip()
		accountData['phoneSender'] = accountFile.readline().rstrip()
		accountData['phoneReciver'] = accountFile.readline().rstrip()

	return accountData

def sendEmail(feed, accountData):
	# print feed
	data = feed.formatEmail()
	if data['body']:
		FROM = accountData['GMAIL_USER']
		TO = accountData['GMAIL_USER']
		MESSAGE = MIMEMultipart('alternative')
		MESSAGE['subject'] = data['subject']
		MESSAGE['From'] = FROM
		MESSAGE['To'] = TO
		MESSAGE.preamble = data['body']
		MESSAGE.attach(MIMEText(data['body'], 'html'))
		# Attempt to send email
		try:
			server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
			server.ehlo()
			server.starttls()
			server.login(accountData['GMAIL_USER'], accountData['GMAIL_PSWD'])
			server.sendmail(FROM, TO, MESSAGE.as_string())
			server.close()
			print 'Successfully sent email'
		except Exception as e:
			print "Failed to send mail"
			print e


def sendSMS(feed, accountData):
	ACCOUNT_SID = accountData['ACCOUNT_SID']
	AUTH_TOKEN = accountData['AUTH_TOKEN']
	phoneSender = accountData['phoneSender']
	phoneReciver = accountData['phoneReciver']

	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)    

	text = feed.formatSMS()

	##If the string is blank send it along
	if text is not "":
		client.messages.create(
			from_= phoneSender, to = phoneReciver, body = text
		)

def writeOldEntries(feeds):
	entriesFile = open(location('entries.txt'), 'w')

	for feed in feeds:
		entriesFile.write(feed.buildEntryLine())
	entriesFile.close()



def main():
	##Setting up variables
	if(len(sys.argv) > 2):
		rssfeed = sys.argv[1]+","+sys.argv[2]
		open(location('rss.txt'), 'a').write(rssfeed+'\n')

	if not os.path.exists(location('rss.txt')):
		print "Add an RSS feed using install.py or pass an RSS feed and a name for that feed as two separate argument; Exiting."
		sys.exit()


	checkAccountData()
	
	transmitDict = {}
	transmitDict['GMAIL'] = sendEmail
	transmitDict['TWILIO'] = sendSMS

	feeds = feedHandler.buildFeeds()

	accountData = getAccountData()
	# sendFunc is a function that we get out of the transmit dict. By doing
	# this, it means not much code is required to add other ways of sending
	# information.
	sendFunc = transmitDict[accountData['sendMethod']]

	for x in feeds:
		sendFunc(x, accountData)

	writeOldEntries(feeds)






if __name__ == '__main__':
	main()


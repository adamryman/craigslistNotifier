from __future__ import print_function
from main import checkAccountData
import subprocess 
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def location(file):
    return os.path.join(__location__,file)


def installCrontab(timeInterval=10, pythonPath=None):
    # Wrapper function for installation of crontab
    
    if not pythonPath:
        pythonPath = subprocess.check_output(['which','python']).strip()    
    mainFilePath = os.getcwd().strip()+'/main.py'
    
    # Do the actual crontab installation
    oldCron = subprocess.check_output(['crontab','-l'])
    oldCron += buildCron(timeInterval, pythonPath, mainFilePath)
    subprocess.Popen(['crontab','-'],stdin=subprocess.PIPE).communicate(input = oldCron)


def buildCron(timeInt, pyPath, mainLocation):
    # Builds the appropriate string for a cron command. Currently the only
    # time increment that's supported is minutes, and such can only be between
    # 1 and 59. As well, 
    if (timeInt > 59) or (timeInt < 1):
        print(timeInt)
        print(type(timeInt))
        raise IndexError("Time interval needs to be within 1 to 59 minutes")

    cronLine = "*/{} * * * * {} {}\n".format(timeInt, pyPath, mainLocation)
    return cronLine

def cronQuestions():
    timeInt = int(raw_input("Enter time interval in minutes for the cron job to be run (1 - 59): "))
    pythonLocation = raw_input("Enter path to python for use with crontab (entering nothing means it will use system default): ")

    return timeInt, pythonLocation

def addRssFeed():
    rssUrl = raw_input("Enter url for the RSS feed to be added (cannot be empty): ")
    rssAlias = raw_input("Enter the label you'd like to give this new RSS feed (cannot be empty): ")

    rssStr = rssUrl+','+rssAlias+'\n'
    open(location('rss.txt'),'a').write(rssStr)


def main():
    doneFlag = False

    while not doneFlag:

        print("Options:\n\t[1] - Install crontab\n\t[2] - Add RSS feed\n\t[3] - Enter Notification Credentials\n\t[4] - Exit")
        selectedOption = int(raw_input("Enter your choice: "))
        
        if selectedOption == 1:
            timeInt, pyPath = cronQuestions()
            installCrontab(timeInt, pyPath)
        elif selectedOption == 2:
            addRssFeed()
        elif selectedOption == 3:
            checkAccountData(silent=False)
        elif selectedOption == 4:
            doneFlag = True

# installCrontab(10)
main()
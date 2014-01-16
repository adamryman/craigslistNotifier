#craigslistNotifier

Uses Twilo to text you when new craigslist listings are posted.  
  
Appending `&format=rss` to any craigslist search will give you an RSS version of that search.  
  
Example:  
[http://seattle.craigslist.org/search/?sort=rel&areaID=2&subAreaID=&query=table&catAbb=sss](http://seattle.craigslist.org/search/?sort=rel&areaID=2&subAreaID=&query=table&catAbb=sss)  

[http://seattle.craigslist.org/search/?sort=rel&areaID=2&subAreaID=&query=table&catAbb=sss&format=rss](http://seattle.craigslist.org/search/?sort=rel&areaID=2&subAreaID=&query=table&catAbb=sss&format=rss)  
  
This could be used for any RSS feed but craigslist is my current focus.

##Requires
[Twillio Python API](https://github.com/twilio/twilio-python)  
[FeedParser](https://pypi.python.org/pypi/feedparser/#downloads)

##Useage

Download `main.py` and put in any directory that python has write access to.

    python main.py 'RSS-FEED-LINK'

The application will prompt you for your Twillio ACCOUNT_SID, AUTH_TOKEN, and phone number and then ask for the receiving phone number.  

Currently I am using `crontabs` to run the python script every 30 minutes. [Getting started with crontabs](http://askubuntu.com/questions/2368/how-do-i-set-up-a-cron-job/2371#2371)

    */10 * * * * python /home/adamryman/craigslistNotifier/main.py

##ToDo

+ Improve setup experience
+ Include crontab script or use alternate way of updating
+ Add email support because twillio cost money (Email servers are a lot harder to setup than I thought)  

##License
MIT
import feedparser


entries = {}
feed = feedparser.parse('http://seattle.craigslist.org/search/sss?catAbb=sss&query=expedit&sort=date&format=rss')

for i in range(0, len(feed['entries'])):
  if feed['entries'][i].link not in entries:
    print feed[entries][i].link

for i in range(0, len(feed['entries'])):
  entries[feed['entries'][i].link] = feed['entries'][0]
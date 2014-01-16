import feedparser


entries = {}
entriesFile = open('entries.txt', 'r')

for line in entriesFile:
  entries[line.rstrip()] = True

entriesFile.close()
entriesFile = open('entries.txt', 'a')

feed = feedparser.parse('http://seattle.craigslist.org/search/sss?catAbb=sss&query=expedit&sort=date&format=rss')
print entries.keys()

for i in range(0, len(feed['entries'])):
  entrie = feed['entries'][i].link
  if entrie not in entries:
    entriesFile.write(entrie + '\n')
    print entrie

  entries[feed['entries'][i].link] = feed['entries'][i]

entriesFile.close()
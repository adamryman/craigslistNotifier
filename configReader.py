from __future__ import print_function
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def location(file):
    return os.path.join(__location__,file)

def readEntries(fName = 'entries.txt' ):
    # Reads the "entries.txt" file (or any specified file), returning the data
    # inside structured in a JSON-like object

    # Creates 'entries.txt' if it doesn't exist already
    if not os.path.exists(location(fName)):
        open(location(fName), 'w').close()

    # Reads and interprets entries file
    entriesFile = open(location(fName), 'r')
    feedEntries = []
    for line in entriesFile:
        line = line.rstrip()
        feedEntries.append({
            'url' : line.split(',')[0],
            'entries' : line.split(',')[1::]
            })
    entriesFile.close()

    return feedEntries

def rssConfigReader(fName = 'rss.txt'):
    # Reads the given file ('rss.txt' by default) and moves the data into a
    # JSON-like object.

    # Checks if the specified rss configuration file exists. If it doesn't, it
    # prompts the user and initiates a hard exit (behaviour I may want to
    # change in the future).
    if os.path.exists(location(fName)):
        rssFile = open(location(fName),'r')
    else:
        # May want to change this behaviour in the future
        print("Make an rss file")
        exit()

    # Moves the data into the JSON-like object
    feedIdentifiers = []
    for line in rssFile:
        line = line.rstrip()
        feedIdentifiers.append({
            'url':line.split(',')[0],
            'alias':line.split(',')[1]
            }) 
    rssFile.close()

    return feedIdentifiers

# I maaaay want to rename this something less unweildy in the future...
def configAndEntryConsolidate(config, entries):
    # Takes the rss configuration data and the entries data and consolidates
    # them into a single JSON-like object

    # Consolidates the entries and feed identifiers into the same dictionary (if they exist)
    for entry in entries:
        for ids in config:
            if ids['url'] == entry['url'] :
                ids['entries'] = entry['entries']
    
    # If there where no entries for a feed, then insert an empty list of
    # entries (just to make sure there is a dictionary item, even if it is
    # empty)
    for ids in config:
        if 'entries' not in ids.keys():
            ids['entries'] = []

    return config

def getAllFeedData():
    # Wraps the other functions and joins them all together.

    entries = readEntries()
    config = rssConfigReader()
    entries = configAndEntryConsolidate(config, entries)

    return entries

def readAllFeedData():
    # This entire function exists to read the data files ('rss.txt',
    # 'entries.txt') and parse the data into a form that can be turned into
    # feed objects.
    #
    # It reads and parses each file separately, then consolidates the data
    # from each into a single big json-like object.
    #
    if os.path.exists(location('rss.txt')):
        rssFile = open(location('rss.txt'),'r')
    else:
        print("Make an rss file")
        exit()
    feedIdentifiers = []
    for line in rssFile:
        line = line.rstrip()
        feedIdentifiers.append({
            'url':line.split(',')[0],
            'alias':line.split(',')[1]
            }) 
    
    # Creates 'entries.txt' if it doesn't exist already
    if not os.path.exists(location('entries.txt')):
        print('Make sure there\'s stuff in the entries.txt file.')
        open(location('entries.txt'), 'w').close()
    entriesFile = open(location('entries.txt'), 'r')
    feedEntries = []
    for line in entriesFile:
        line = line.rstrip()
        feedEntries.append({
            'url' : line.split(',')[0],
            'entries' : line.split(',')[1::]
            })

    # Consolidates the entries and feed identifiers into the same dictionary (if they exist)
    for entry in feedEntries:
        for ids in feedIdentifiers:
            if ids['url'] == entry['url'] :
                ids['entries'] = entry['entries']
    
    # If there where no entries for a feed, then insert an empty list of
    # entries (just to make sure there is a dictionary item, even if it is
    # empty)
    for ids in feedIdentifiers:
        if 'entries' not in ids.keys():
            ids['entries'] = []


    rssFile.close()
    entriesFile.close()

    return feedIdentifiers
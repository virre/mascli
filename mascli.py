#!/usr/bin/python3 

import urllib.request
import json
import re
import configparser
import argparse
import os

class Mastadon: 

    def __init__(self, instance):
        self.instance = instance
        self.allowSpoilered = False
        self.allowSensitive = False
        self.tabbed = False
        self.skip = { }
        self.arrow = False
        self.limit = 3

    def getLocalTimeline(self):
        self.getPublicTimeline('local')

    def getRemoteTimeline(self):
        self.getPublicTimeline('remote')

    def getPublicTimeline(self, type):
        query = "?"
        if (type == "local"):
            query = query + "local=true"
        if (type == "remote"):
            query = query + "remote=true"
        endpoint = "/api/v1/timelines/public" + query + "&limit=" + str(self.limit) 
        toots = self.callApi(endpoint)
        for toot in toots:
            t = Toot(self.instance)
            t.populate(toot)
            t.showToot()

    def getToot(self, id):
        endpoint = "/api/v1/statuses/" + id
        toot = self.callApi(endpoint)
        t = Toot(self.instance)
        t.populate(toot)
        t.showToot()
    
    def allowSpoilers(self):
        self.allowSpoilered = True

    def disallowSpoilers(self):
        self.allowSpoilered = False

    def callApi(self, endpoint):
        url = "https://" + self.instance + endpoint 
        with urllib.request.urlopen(url) as response:
            content = response.read()
        return json.loads(content)

    def setLimit(self, limit):
        self.limit = limit

class Toot(Mastadon):

    def __init__(self, instance):
        Mastadon.__init__(self, instance)

    def populate(self, toot):
        self.id = toot['id']
        self.displayName = toot['account']['display_name']
        self.userUrl = toot["account"]["url"]
        self.createdAt = toot["created_at"]
        self.tootUrl = toot["url"]
        self.spoilerText = toot["spoiler_text"]
        self.content = toot["content"]
        self.replyTo = toot["in_reply_to_id"]
        if (toot["sensitive"] == "true"):
            self.sensitive = True
        else:
            self.sensitive = False
        self.replyCount = toot["replies_count"]
        self.boosts = toot["reblogs_count"]
        self.favoriteCount = toot["favourites_count"]
        self.images = []
        if (toot["media_attachments"]):
            for media in toot["media_attachments"]:
                if (media['type'] == "image"):
                    imgstr = ""
                    if (media["description"]):
                        imgstr = "Image description: " + media["description"] + ". "
                    if (media['url']):
                        imgstr = imgstr + "Image url " + media['url'] + "."
                    if (media["remote_url"]):
                        imgstr = imgstr + "Image url " + media['url'] + "."
                    self.images.append(imgstr)
                else:
                    print("Other media: " + media["type"])
        self.tags = ""
        self.mentions = []
        if (toot["tags"]):
            for tag in toot["tags"]:
                self.tags = self.tags + " " + tag["name"] + " (" + tag["url"] + ")"
        if (toot["mentions"]):
            for mention in toot["mentions"]:
                print(mention)
                self.mentions.append(mention)

    def showToot(self):
        if (self.skip.get(self.id) is not None):
            return
        hide = False
        if (self.sensitive and self.allowSensitive):
            hide = True
        if (self.allowSpoilered == False and self.spoilerText):
            hide = True
        content = re.sub("<.*?>", "", self.content)
        prestring = ""
        if (self.replyTo):
            self.arrow = True
            self.getToot(self.replyTo)
            self.arrow = False
            self.skip.update({self.replyTo : self.replyTo})
            self.tabbed = True
        if (self.tabbed == True):
            prestring = prestring + "\t"
        print(prestring + self.displayName + " ( " + self.userUrl + " ) ")
        print(prestring + self.createdAt + " " + self.id + " " + self.tootUrl )
        if (self.tags):
            print(prestring + self.tags)
        infostring = ""
        if (self.replyCount > 0):
            infostring = infostring + "Replied to " + str(self.replyCount) + " times "
        if (self.boosts > 0):
            infostring = infostring + "Boosted " + str(self.boosts) + " times "
        if (self.favoriteCount > 0):
            infostring = infostring + "Favorited " + str(self.favoriteCount) + " times "
        if (infostring):
            print (prestring + infostring)
        if (hide == False):
            print(prestring + content)
        else:
            print(prestring + "Spoilerd: " + self.spoilerText)
        for image in self.images:
            print(prestring + image)
        if (self.tabbed == True):
            self.tabbed = False
        if (self.arrow == True):
            print("-->")
        else:
            print("---")


parser = argparse.ArgumentParser(description="Mastadon cli reader")
parser.add_argument("--limit", default=3)
args = parser.parse_args()
config = configparser.ConfigParser()

confdir = os.path.expanduser('~') + "/.mascli.ini"
config.read(confdir)
for instance in config['instances']['instances'].split(','):
    m = Mastadon(instance)
    m.setLimit(args.limit)
    print("\nShowing {} timeline\n".format(instance))
    m.getLocalTimeline()


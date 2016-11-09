import requests
import csv
from html.parser import HTMLParser


class PublisherParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.getting_there = False
        self._publisher = None

    def get_publisher(self):
        return self._publisher

    def feed(self, data):
        self.getting_there = False
        self._publisher = None
        HTMLParser.feed(self, data)

    def handle_data(self, data):

        data = data.strip()
        if data == "Publisher":
            self.getting_there = True
        elif data != ":" and self.getting_there:
            self._publisher = data
            self.getting_there = False


class UrlRetriever(object):

    def __init__(self, base):
        self._base_url = base

    def get_base_url(self):
        return self._base_url

    def retrieve(self, url):
        return requests.get(self.get_base_url() + url).text


retriever = UrlRetriever("http://uk.ign.com")
parser = PublisherParser()

with open("../data/ign.csv") as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        if row[3] == "url":
            row.append("Publisher")
            with open("../data/ign_with_publishers.csv", "w") as g:
                writer = csv.writer(g, delimiter=",")
                writer.writerow(row)
        else:
            parser.feed(retriever.retrieve(row[3]))
            row.append(parser.get_publisher())
            with open("../data/ign_with_publishers.csv", "a") as g:
                writer = csv.writer(g, delimiter=",")
                writer.writerow(row)




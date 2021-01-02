#VERSION: 1.0
#AUTHORS:   CravateRouge (github.com/CravateRouge)

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the author nor the names of its contributors may be
#      used to endorse or promote products derived from this software without
#      specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from re import compile as re_compile
from re import search as re_search

from html.parser import HTMLParser
#qBt
from novaprinter import prettyPrinter
from helpers import retrieve_url

class oxtorrent(object):
    """ Search engine class """
    url = 'https://www.oxtorrent.co'
    name = 'OxTorrent'
    supported_categories = {'all': '', 'music': 'musique', 'movies': 'films', 'books': 'ebook', 'software': 'logiciels', 'tv':'series'}

    def download_torrent(self, desc_link):
        """ Downloader """
        page = retrieve_url(desc_link)
        magnet_match = re_search(r"href\s*\=\s*\"(magnet[^\"]+)\"", page)
        if magnet_match and magnet_match.groups():
            print(magnet_match.groups()[0] + " " + desc_link)
        else:
            raise Exception('Error, please fill a bug report!')

    class MyHtmlParser(HTMLParser):
        """ Parser class """
        def __init__(self, list_searches, url):
            HTMLParser.__init__(self)
            self.list_searches = list_searches
            self.url = url
            self.current_item = None
            self.save_item = None
            self.result_tbody = False
            self.add_query = True
            self.result_query = False
            self.index_td = 0

        def handle_start_tag_default(self, attrs):
            """ Default handler for start tag dispatcher """
            pass

        def handle_start_tag_a(self, attrs):
            """ Handler for start tag a """
            params = dict(attrs)
            link = self.url+params["href"]
            self.current_item["desc_link"] = link
            self.current_item["link"] = link
            self.save_item = "name"

        def handle_start_tag_td(self, attrs):
            """ Handler for start tag td """
            if self.index_td == 1:
                self.save_item = "size"
            elif self.index_td == 2:
                self.save_item = "seeds"
            elif self.index_td == 3:
                self.save_item = "leech"

            self.index_td += 1

        def handle_starttag(self, tag, attrs):
            """ Parser's start tag handler """
            if self.current_item:
                dispatcher = getattr(self, "_".join(("handle_start_tag", tag)), self.handle_start_tag_default)
                dispatcher(attrs)

            elif self.result_tbody:
                if tag == "tr":
                    self.current_item = {"engine_url" : self.url}

            elif tag == "table":
                self.result_tbody = True

            elif self.add_query and attrs:
                if self.result_query and tag == "a":
                    if len(self.list_searches) < 10:
                        self.list_searches.append(attrs[0][1])
                    else:
                        self.add_query = False
                        self.result_query = False


        def handle_endtag(self, tag):
            """ Parser's end tag handler """
            if self.result_tbody:
                if tag == "tr":
                    prettyPrinter(self.current_item)
                    self.current_item = None
                    self.index_td = 0
                elif tag == "table":
                    self.result_tbody = False

        def handle_data(self, data):
            """ Parser's data handler """
            if data == "\n":
                return
            if self.save_item:
                if self.save_item == "name":
                    # names with special characters like '&' are splitted in several pieces
                    if 'name' not in self.current_item:
                        self.current_item["name"] = ''
                    self.current_item["name"] += data.strip() 
                else:
                    self.current_item[self.save_item] = data
                    self.save_item = None


    def search(self, what, cat='all'):
        """ Performs search """
        #prepare query. 7 is filtering by seeders
        cat = cat.lower()
        query = "/".join((self.url, "recherche", what))
        response = retrieve_url(query)
        list_searches = []
        parser = self.MyHtmlParser(list_searches, self.url)
        parser.feed(response)
        parser.close()

        parser.add_query = False
        for search_query in list_searches:
            response = retrieve_url(search_query)
            parser.feed(response)
            parser.close()

        return

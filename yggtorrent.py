#VERSION: 0.3
#AUTHORS: CravateRouge (github.com/CravateRouge)

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

import tempfile, os, io, gzip

from urllib import request, error, parse

# import qBT modules
from html.parser import HTMLParser
from novaprinter import prettyPrinter
from helpers import htmlentitydecode

class yggtorrent(object):
    """ Search engine class """

    # Login information ######################################################
    #
    # SET THESE VALUES!!
    #
    username = "YOUR USERNAME"
    password = "YOUR PASSWORD"
   ###########################################################################

    url = 'https://www2.yggtorrent.si'
    name = 'YGG Torrent'
    supported_categories = {'all': '', 'music': '2139', 'movies': '2145', 'games':'2142', 'software': '2144', 'books': '2140'}

    ua = 'Mozilla/5.0 (X11; Linux i686; rv:38.0) Gecko/20100101 Firefox/38.0'
    sesh = None

    def login(self):        
        formdata = {"id": self.username, "pass": self.password}
        data_encoded = parse.urlencode(formdata).encode('utf-8')

        opener = request.build_opener(request.HTTPCookieProcessor)
        opener.addheaders = [('User-Agent',self.ua)]
        opener.open(self.url)
        opener.open('/'.join((self.url, 'user', 'login')), data_encoded)
        
        self.sesh = opener
        
    #We must use a custom function because we must handle cookies to have access to the site
    def retrieve_url(self, url):
        if self.sesh is None:
            self.login()
            
        try:
            response = self.sesh.open(url)
        except error.URLError as errno:
            print(" ".join(("Connection error:", str(errno.reason))))
            return ""
            
        dat = response.read()
        
        # Check if it is gzipped
        if dat[:2] == b'\x1f\x8b':
            # Data is gzip encoded, decode it
            compressedstream = io.BytesIO(dat)
            gzipper = gzip.GzipFile(fileobj=compressedstream)
            extracted_data = gzipper.read()
            dat = extracted_data
        info = response.info()
        charset = 'utf-8'
        try:
            ignore, charset = info['Content-Type'].split('charset=')
        except Exception:
            pass
        dat = dat.decode(charset, 'replace')
        dat = htmlentitydecode(dat)
         
        return dat
        
    class MyHtmlParseWithBlackJack(HTMLParser):
        """ Parser class """
        def __init__(self, list_searches, url):
            HTMLParser.__init__(self)
            self.list_searches = list_searches
            self.url = url
            self.current_item = None
            self.save_item = None
            self.result_table = False #table with results is found
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
            
            if 'href' in params:
                link = params["href"]
                if '/torrent/' in link:
                    self.current_item["desc_link"] = link
                    self.save_item = "name"
            elif 'target' in params:
                self.current_item["link"] = '/'.join((self.url, 'engine', 'download_torrent?id=%s'%(params['target'])))

        def handle_start_tag_td(self, attrs):
            """ Handler for start tag td """
            if self.index_td == 5:
                self.save_item = "size"
            elif self.index_td == 7:
                self.save_item = "seeds"
            elif self.index_td == 8:
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
                self.result_table = "table" == attrs[0][1]

            elif self.add_query:
                if self.result_query and tag == "a" and attrs[0][1] and attrs[0][1] not in self.list_searches:
                    if len(self.list_searches) < 10:
                        self.list_searches.append(attrs[0][1])
                    else:
                        self.add_query = False
                        self.result_query = False
                elif tag == "ul" and attrs:
                    self.result_query = "pagination" == attrs[0][1]

        def handle_endtag(self, tag):
            """ Parser's end tag handler """
            if self.result_tbody:
                if tag == "tr":
                    prettyPrinter(self.current_item)
                    self.current_item = None
                    self.index_td = 0
                    self.save_item = None
                elif tag == "table":
                    self.result_table = self.result_tbody = False
                    

            elif self.result_table:
                if tag == "thead":
                    self.result_tbody = True
                elif tag == "table":
                    self.result_table = self.result_tbody = False

            elif self.add_query and self.result_query:
                if tag == "ul":
                    self.add_query = self.result_query = False

        def handle_data(self, data):
            """ Parser's data handler """
            if self.save_item:
                    self.current_item[self.save_item] = data.strip()
                    self.save_item = None

    def search(self, what, cat='all'):
            """ Performs search """
            #prepare query. 7 is filtering by seeders
            cat = cat.lower()
            what = parse.quote_plus(what)
            query_string = 'search?name=%s&category=%s&do=search&order=desc&sort=seed'%(what, self.supported_categories[cat]) 
            query = "/".join((self.url, "engine", query_string))

            response = self.retrieve_url(query)

            list_searches = []
            parser = self.MyHtmlParseWithBlackJack(list_searches, self.url)
            parser.feed(response)
            parser.close()

            parser.add_query = False
            for search_query in list_searches:
                response = self.retrieve_url(search_query)
                parser.feed(response)
                parser.close()

            return
      
    def download_file(self, url, referer=None):
        """ Download file at url and write it to a file, return the path to the file and the url """
        file, path = tempfile.mkstemp()
        file = os.fdopen(file, "wb")

        if self.sesh is None:
            self.login()
            
        try:
            response = self.sesh.open(url)
        except error.URLError as errno:
            print(" ".join(("Connection error:", str(errno.reason))))
            return ""
            
        dat = response.read()
        
        # Check if it is gzipped
        if dat[:2] == b'\x1f\x8b':
            # Data is gzip encoded, decode it
            compressedstream = io.BytesIO(dat)
            gzipper = gzip.GzipFile(fileobj=compressedstream)
            extracted_data = gzipper.read()
            dat = extracted_data
        
        # Write it to a file
        file.write(dat)
        file.close()
        
        # return file path
        return path+" "+url

    def download_torrent(self, info):
        """ Downloader """
        print(self.download_file(info))

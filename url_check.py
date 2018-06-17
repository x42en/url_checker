#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys, requests
from fake_useragent import UserAgent
from urlparse import urlparse

class Spider:
    def __init__(self, headers={}):
        self.urls = []
        self.headers = headers
        self.current = None

    def follow(self, url):
        self.current = url
        r = requests.head(self.current, timeout=10, headers=self.headers)
        location = r.headers.get('location')
        
        if r.status_code == 200:
            return False
        
        # Correct location
        if location:
            location = location[1:] if location.startswith('/') else location
            if not (location.startswith('http://') or location.startswith('https://') or location.startswith('ftp://')):
                parsed_uri = urlparse(self.current)
                location = '{uri.scheme}://{uri.netloc}/{i}'.format(uri=parsed_uri, i=location)

        while r.status_code in range(300,399):
            self.urls.append(location)
            self.display(r.status_code, location)
            self.follow(location)
            return False

        # Append final destination
        self.display(r.status_code, location)
        self.urls.append(location)
        return True
        
    def display(self, code, location):
        print "[{i}] ({c}) {u}".format(i=len(self.urls),c=code, u=location)

    def download(self, uid):
        try:
            url = self.urls[int(uid)-1]
        except IndexError:
            print 'Invalid entry.'
            return False

        r = requests.get(url, timeout=10, headers=self.headers)
        print r.text

def main(argv):
    try:
        url = argv[1]
    except IndexError:
        print "Usage: {p} http://url.tocheck.com".format(p=argv[0])
        sys.exit(1)

    # Fake user-agent to bypass IDS
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    spider = Spider(headers)
    print "[+] Following {u}".format(u=url)
    print ''

    try:
        spider.follow(url)
    except KeyboardInterrupt, SystemExit:
        print '\nBye!'
        sys.exit(0)
    except Exception as err:
        print "[!] Unable to retrieve {u}: {e}".format(u=spider.current, e=err)
        sys.exit(1)
    
    try:
        if len(spider.urls):
            download = raw_input('Do you want to download a url ? [y/N]: ')
            if download and (download.lower() == 'y'):
                while True:
                    nb = raw_input('Select a url to download [{d}]: '.format(d=len(spider.urls)))
                    if not nb:
                        nb = len(spider.urls)
                        break
                    try:
                        nb = int(nb)
                    except ValueError:
                        print 'Invalid entry!'
                        continue
                    
                    if nb > len(spider.urls):
                        print('Invalid entry')
                        continue
                    break
                spider.download(nb)
    except KeyboardInterrupt, SystemExit:
        print '\nBye!'

if __name__ == '__main__':
    main(sys.argv)
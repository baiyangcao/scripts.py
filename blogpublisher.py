# -*- coding: UTF-8 -*-

"""
publish blog to blog site, cnblog or oschina
"""

import xmlrpc.client
from datetime import datetime
from optparse import OptionParser

import requests
from markdown2 import Markdown

import os


class BlogPublisher:
    """
    base class for blog publish
    """

    def __init__(self, username, password, url):
        """
        initialize the username, password and mateWeblog url
        :param username:
        :param password:
        :param url: mateWeblog url
        """
        self.username = username
        self.password = password
        self.url = url
        self.appKey = "baiyangcao"
        self.server = self._get_server()
        self.blogid = self.__get_blogid()

    def _get_server(self):
        """
        create the ServerProxy Object
        :return:
        """
        return xmlrpc.client.ServerProxy(self.url)

    def __get_blogid(self):
        """
        get the blogid by XML-RPC API blogger.getUsersBlogs
        :return:
        """
        return self.server.blogger.getUsersBlogs(self.appKey, self.username, self.password)[0]["blogid"]

    def publish(self, title, content, date=None):
        """
        publish blog to 
        :param date: blog publish date, default None
        :param content: blog content to publish (markdown syntax)
        :return: 
        """
        post = {"title": title, "description": content}
        if date is not None:
            post["dateCreated"] = date
        self.server.metaWeblog.newPost(self.blogid, self.username, self.password, post, True)

    def delete(self, postid):
        """
        delete blog by postid
        :param postid:
        :return:
        """
        self.server.blogger.deletePost(self.appKey, postid, self.username, self.password, True)


class CnBlogPublisher(BlogPublisher):
    """
    blog publisher to cnblog.com
    """

    def __init__(self):
        super(CnBlogPublisher, self).__init__("baiyangcao", "y2211612", "http://rpc.cnblogs.com/metaweblog/baiyangcao")


class OsChinaPublisher(BlogPublisher):
    """
    blog publisher to oschina.com
    """

    def __init__(self):
        super(OsChinaPublisher, self).__init__("497462386@qq.com", "y2211612", "https://my.oschina.net/action/xmlrpc")

    def _get_server(self):
        """
        create ServerProxy and set the user_agent
        :return:
        """
        transport = xmlrpc.client.SafeTransport()
        transport.user_agent = "Fiddler"
        return xmlrpc.client.ServerProxy(self.url, transport=transport)


def main():
    parser = OptionParser("usage: %prog [options] arg")
    parser.add_option("-f", "--file", dest="filename",
                      help="the blog file want to be publish")
    parser.add_option("-t", "--type", dest="type",
                      type="choice", default="cnblog",
                      choices=("cnblog", "oschina"),
                      help="target blog website, available values: cnblog, oschina")
    (options, args) = parser.parse_args()
    if len(args) < 0 or not options.filename:
        print("Please input the blog file want to be published")

    if os.path.exists(options.filename):
        title = ''
        date = ''
        content = ''
        sperator_count = 0
        with open(options.filename, 'r', encoding='utf-8') as f:
            for line in iter(f.readline, ''):
                # deal with the meta data
                if sperator_count < 2:
                    if line.strip() == '---':
                        sperator_count = sperator_count + 1
                    else:
                        key, value = line.split(':')
                        if key == 'title':
                            title = value
                        elif key == 'date':
                            date = value
                else:
                    content = content + '\r\n' + line

        if content != '':
            publisher = None
            if options.type == 'cnblog':
                publisher = CnBlogPublisher()
            elif options.type == 'oschina':
                publisher = OsChinaPublisher()
            else:
                pass
            # convert markdown to html by github api
            api_url = 'https://api.github.com/markdown/raw'
            data = content.encode()
            headers = {
                'Content-Type': 'text/plain',
                'Content-Length': str(len(data))
            }
            resp = requests.post(api_url, data=data, headers=headers)
            html = resp.text
            publisher.publish(title, html, date)

    else:
        print("Input file not exists!")


if __name__ == '__main__':
    main()

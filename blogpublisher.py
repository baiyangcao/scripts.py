# -*- coding: UTF-8 -*-

"""
publish blog to blog site, cnblog or oschina
"""

import xmlrpc.client

from datetime import datetime
from optparse import OptionParser

import requests

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

    def publish(self, post):
        """
        publish blog to 
        :param post: post data, content title, description, createdate
        :return: 
        """
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
        publishblog(options.filename, options.type)
    else:
        print("Input file not exists!")


def getmetadata(filename):
    '''
    read the meta data and the content of blog
    :param filename: the blog filename
    :return:
    '''
    data = {}
    fieldsmap = {
        "title": "title",
        "date": "dateCreated"
    }
    content = ''
    sperator_count = 0
    with open(filename, 'r', encoding='utf-8') as f:
        for line in iter(f.readline, ''):
            # deal with the meta data
            if sperator_count < 2:
                if line.strip() == '---':
                    sperator_count = sperator_count + 1
                else:
                    key, value = line.split(':')
                    keys = fieldsmap.keys()
                    if key in keys:
                        if key == 'date':
                            value = datetime.strptime(value.strip(), '%Y-%m-%d')
                        data[fieldsmap[key]] = value
            else:
                content = content + '\r\n' + line

    data["description"] = content
    return data

def mdtohtml(raw):
    '''
    convert markdown content to html format by github api
    :param raw: markdown content
    :return: the html format content
    '''
    api_url = 'https://api.github.com/markdown/raw'
    data = raw.encode()
    headers = {
        'Content-Type': 'text/plain',
        'Content-Length': str(len(data))
    }
    resp = requests.post(api_url, data=data, headers=headers)
    return resp.text


def publishblog(filename, type):
    '''
    publish blog to blog website
    :param filename: the blog file name
    :param type: blog website type, cnblog/oschina
    :return:
    '''
    data = getmetadata(filename)
    if data["description"] != '':
        publisher = None
        if type == 'cnblog':
            publisher = CnBlogPublisher()
        elif type == 'oschina':
            publisher = OsChinaPublisher()
        else:
            pass
        # convert markdown to html by github api
        data["description"] = mdtohtml(data["description"])
        publisher.publish(data)


if __name__ == '__main__':
    main()

# -*- coding: UTF-8 -*-

"""
publish blog to blog site, cnblog or oschina
"""

import xmlrpc.client


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

    def publish(self, title, content):
        """
        publish blog to 
        :param content: blog content to publish (markdown syntax)
        :return: 
        """
        post = {
            "title": title,
            "description": content
        }
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

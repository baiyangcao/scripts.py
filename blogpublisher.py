# -*- coding: UTF-8 -*-

"""
publish blog to blog site, cnblog or oschina
"""


class BlogPublisher:
    """
    base class for blog publish
    """

    def __init__(self):
        self.username = ""
        self.password = ""
        self.baseurl = ""
        self.loginurl = ""
        self.publishurl = ""

    def publish(self, content):
        """
        publish blog to 
        :param content: blog content to publish (markdown syntax)
        :return: 
        """
        pass


class CnBlogPublisher(BlogPublisher):
    """
    blog publisher to cnblog.com
    """

    def __init__(self):
        super.__init__()

    def publish(self, content):
        """
        publish blog to 
        :param content: blog content to publish (markdown syntax)
        :return: 
        """
        pass


class OsChinaPublisher(BlogPublisher):
    """
    blog publisher to oschina.com
    """

    def __init__(self):
        super.__init__()

    def publish(self, content):
        """
        publish blog to 
        :param content: blog content to publish (markdown syntax)
        :return: 
        """
        pass

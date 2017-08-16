# -*- coding: utf-8 -*-

import sys
import xmlrpc
from unittest import TestCase
from blogpublisher import CnBlogPublisher, OsChinaPublisher;

sys.path.append('..')


class BlogPublisherTest(TestCase):
    def test_cnblog_publish(self):
        """
        publish blog to cnblog
        :return:
        """
        cnblog = CnBlogPublisher()
        cnblog.publish("test", "this is a test")

    def test_oschina_getUsersBlogs(self):
        url = "https://my.oschina.net/action/xmlrpc"
        appKey = "baiyangcao"
        username = "497462386@qq.com"
        password = "y2211612"
        transport = xmlrpc.client.SafeTransport()
        transport.user_agent = "Fiddler"
        server = xmlrpc.client.ServerProxy(url, transport=transport)
        print(server.blogger.getUsersBlogs(appKey, username, password))

    def test_oschina_publish(self):
        oschina = OsChinaPublisher()
        oschina.publish("test", "<h1>this is a test</h1>")
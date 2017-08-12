# -*- coding: utf-8 -*-

import sys
from unittest import TestCase
from blogpublisher import CnBlogPublisher;

sys.path.append('..')


class BlogPublisherTest(TestCase):
    def test_cnblog_publish(self):
        """
        publish blog to cnblog
        :return:
        """
        cnblog = CnBlogPublisher()
        cnblog.publish("test", "this is a test")

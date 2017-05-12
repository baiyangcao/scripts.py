# -*- coding: utf-8 -*-

import sys

sys.path.append('..')

from unittest import TestCase, main
from blogformatter import formatline


class BlogFormatterTest(TestCase):
    def test_formateline_start_rouge(self):
        '''
        formateline function test
        target rouge syntax
        code range start
        :return: 
        '''
        source = '```javascript'
        result = '{% highlight javascript %}'
        self.assertEqual(result, formatline(source, 'rouge').strip('\n'))

    def test_formateline_end_rouge(self):
        '''
        formateline function test
        target rouge syntax
        code range end
        :return: 
        '''
        source = '```'
        result = '{% endhighlight %}'
        self.assertEqual(result, formatline(source, 'rouge').strip('\n'))

    def test_formateline_start_md(self):
        '''
        formateline function test
        target markdown syntax
        code range start
        :return: 
        '''
        source = '{% highlight javascript %}'
        result = '```javascript'
        self.assertEqual(result, formatline(source, 'markdown').strip('\n'))

if __name__ == '__main__':
    main()
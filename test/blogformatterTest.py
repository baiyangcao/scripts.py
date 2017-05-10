# -*- coding: utf-8 -*-

import sys

sys.path.append('..')

from unittest import TestCase, main
from blogformatter import formatline


class BlogFormatterTest(TestCase):
    def test_formateline_start_rouge(self):
        '''
        formateline function test
        target markdown syntax
        :return: 
        '''
        source = '```javascript'
        result = '{% highlight javascript %}'
        self.assertEqual(result, formatline(source, 'rouge').strip('\n'))

if __name__ == '__main__':
    main()
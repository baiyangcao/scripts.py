# -*- coding: UTF-8 -*-
import re
import os

from optparse import OptionParser


def formatline(line):
    """
    format line, change ```javascript to {% highlight javascript %}
    :param line: raw line string 
    :return: formatted line string
    """
    start_regexp = r"^\s*```(.+)\s*$"
    start_replace = r"{% highlight \1 %}"
    end_regexp = r"^\s*```\s*$"
    end_replace = r"{% endhighlight %}"
    if re.fullmatch(start_regexp, line) is not None:
        return re.sub(start_regexp, start_replace, line)
    if re.fullmatch(end_regexp, line) is not None:
        return re.sub(end_regexp, end_replace, line)


def main():
    parser = OptionParser("usage: %prog [options] arg")
    parser.add_option("-f", "--file", dest="filename",
                      help="the file want to be formatted")
    (options, args) = parser.parse_args()
    if len(args) < 0 or options.filename:
        print("Please input the file want to be formatted")

    if os.path.exists(options.filename):
        with open(options.filename, 'rw') as f:
            lines = []
            for line in iter(f.readline, ''):
                lines.append(formatline(line))
            f.writelines(lines)
    else:
        print("Input file not exists!")


if __name__ == '__main__':
    main()

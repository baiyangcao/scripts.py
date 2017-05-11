# -*- coding: UTF-8 -*-
import re
import os

from optparse import OptionParser


def formatline(line, type):
    """
    format line according to type, change code style to markdown or rouge syntax
    :param line: raw line string 
    :param type: target format type, available value: markdown, rouge 
    :return: formatted line string
    """
    md_start_regexp = r"^\s*```(.+)\s*$"
    rouge_start_regexp = r"{% highlight \1 %}\n"
    md_end_regexp = r"^\s*```\s*$"
    rouge_end_regexp = r"{% endhighlight %}\n"

    if type.lower() == "rouge":
        start_regexp = md_start_regexp
        start_replace = rouge_start_regexp
        end_regexp = md_end_regexp
        end_replace = rouge_end_regexp
    elif type.lower() == "markdown":
        start_regexp = rouge_start_regexp
        start_replace = md_start_regexp
        end_regexp = rouge_end_regexp
        end_replace = md_end_regexp

    if re.fullmatch(start_regexp, line) is not None:
        return re.sub(start_regexp, start_replace, line)
    elif re.fullmatch(end_regexp, line) is not None:
        return re.sub(end_regexp, end_replace, line)
    else:
        return line


def main():
    parser = OptionParser("usage: %prog [options] arg")
    parser.add_option("-f", "--file", dest="filename",
                      help="the file want to be formatted")
    parser.add_option("-t", "--type", dest="type",
                      type="choice", default="rouge",
                      choices=("markdown", "rouge"),
                      help="target format type, available values: markdown, rouge")
    (options, args) = parser.parse_args()
    if len(args) < 0 or not options.filename:
        print("Please input the file want to be formatted")

    if os.path.exists(options.filename):
        lines = []
        with open(options.filename, 'r', encoding='utf-8') as f:
            for line in iter(f.readline, ''):
                lines.append(formatline(line, options.type))

        with open(options.filename, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    else:
        print("Input file not exists!")


if __name__ == '__main__':
    main()

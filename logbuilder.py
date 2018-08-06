# -*- coding : utf-8 -*-

'''
------------------------------------------
generate the daily log
according to the specific repos
------------------------------------------
'''

import time
import os

from datetime import datetime, date
from git import Repo
from optparse import OptionParser

# project config
CONFIGS = [{
    'path': 'F:\yjm\实习\platform1.4.test.02',
    'name': '平台1-4测试项目'
}]

def RepoMessages(config, date, max_count=20, branch='master'):
    repo = Repo(config['path'])
    messages = []

    str_date = date.strftime('%Y%m%d')
    # get the recent commit
    for index, commit in enumerate(repo.iter_commits(branch, max_count=max_count)):
        commit_date = time.strftime('%Y%m%d', time.gmtime(commit.committed_date))
        if(str_date == commit_date):
            messages.append('\t%s. %s' % (index + 1, commit.message))
        else:
            break

    # add the project name
    if len(messages) > 0:
        messages.insert(0, config['name'])
    return messages

if __name__ == '__main__':
    parser = OptionParser('usage: %prog [options] arg')
    parser.add_option('-f', '--file', dest="path", default='../杨家明-%s.txt' % datetime.now().strftime('%Y%m%d'), help='the generate file path')
    parser.add_option('-d', '--date', dest="date", default=datetime.now(), help='the commit date to filter, eg: 20180205')
    parser.add_option('-n', '--number', dest="number", default=20, help='the commit number to fetch')
    parser.add_option('-b', '--branch', dest="branch", default='master', help='the branch to generate the log')
    
    # generate the log file
    (options, args) = parser.parse_args()
    # convert the date option
    if isinstance(options.date, str):
        options.date = time.strptime(options.date, '%Y%m%d')
    # get the absolute path
    #options.path = os.path.realpath(options.path)

    with open(options.path, 'w', encoding='utf-8') as f:
        for config in CONFIGS:
            f.writelines(RepoMessages(config, options.date, max_count=options.number))

    print('生成成功，不要忘记打卡哟！')
# -*- encoding: utf-8 -*-
import os
import threading
import traceback

import requests


class HaiXue():
    def __init__(self):
        self.cookies = None
        self.goods_id = '1066185'
        self.catalog_id = '16'
        self.catalogs = None
        self.path = r'C:\Users\Administrator\Downloads\Video\二级建造师'
        self.__login()
        self.__get_goods()

    def __login(self):
        resp = requests.post('http://highso.cn/doLogin.do',
                             data=dict(j_username=18396517057, j_password='yf920624',
                                       _spring_security_remember_me='off'))
        # print(resp.text)
        self.cookies = resp.cookies

    def __get_goods(self):
        resp = requests.post('http://highso.cn/course/white/getGoodsWithRecord.do',
                             data={'categoryId': self.catalog_id},
                             cookies=self.cookies)
        json = resp.json()
        self.catalogs = json['result'][0]['firstCatalog']

    def __get_catalog(self, catalog_id):
        resp = requests.post('http://highso.cn/course/white/getCatalog.do',
                             data={
                                 'goodsCatalogId': catalog_id,
                                 'goodsId': self.goods_id
                             },
                             cookies=self.cookies)
        return resp.json()['result']

    def __get_videos(self, module_id):
        resp = requests.post('http://highso./course/module/findGoodsModuleVideo.do',
                             data={
                                 'catalogId': module_id,
                                 'goodsId': self.goods_id
                             },
                             cookies=self.cookies)
        return resp.json()['videos']

    def __download_videos(self, id, path, name, type='Video', format='.mp4'):
        url = 'http://highso.cn/goods/downloadUrl.do?itemId=%s&type=%s&isCatalog=No&goodsId=%s' % (
            id, type, self.goods_id)
        resp = requests.get(url, cookies=self.cookies, allow_redirects=False)
        self.__check_path(path)
        filepath = os.path.join(path, name + format)
        print('开始下载：', filepath)
        self.__multithreading_download(resp.headers['Location'], filepath)

    def __multithreading_download(self, url, filepath, num=8):
        """
        download file by multithreading
        :param url:
        :param filepath: local file path including file name
        :param num: threads count
        :return:
        """
        try:
            # 获取文件总大小
            r = requests.head(url, cookies=self.cookies)
            total = int(r.headers['Content-Length'])

            # 检查是否需要下载文件
            if os.path.exists(filepath):
                # 检查本地文件大小是否符合，若符合则跳过，否则删除重新下载
                if os.path.getsize(filepath) == total:
                    print('跳过文件：', filepath)
                    return
                else:
                    os.remove(filepath)

            # 获取每一块的下载范围
            ranges = []
            offset = int(total / num)
            for i in range(num):
                if i == num - 1:
                    ranges.append((i * offset, ''))
                else:
                    ranges.append((i * offset, (i + 1) * offset))

            # 开始下载
            with open(filepath, 'wb') as fd:
                thread_list = []
                n = 0
                for ran in ranges:
                    start, end = ran
                    n += 1
                    thread = threading.Thread(target=self.__download, args=(url, fd, start, end))
                    thread.start()
                    thread_list.append(thread)
                for i in thread_list:
                    i.join()

            print('成功下载：', filepath)
        except:
            print('下载失败：', filepath)
            traceback.print_exc()

    def __download(self, url, fd, start, end):
        """
        download method for each range
        :param start:
        :param end:
        :return:
        """
        headers = {'Range': 'Bytes=%s-%s' % (start, end), 'Accept-Encoding': '*'}
        res = requests.get(url, headers=headers, cookies=self.cookies)
        fd.seek(start)
        fd.write(res.content)

    def __check_path(self, path):
        """
        check whether the `path` exists, if not create it
        :param path:
        :return:
        """
        if not os.path.exists(path):
            os.makedirs(path)


if __name__ == '__main__':
    haixue = HaiXue()
    print(haixue.catalogs)

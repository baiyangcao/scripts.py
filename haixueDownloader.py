# -*- encoding: utf-8 -*-
import os
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
        # download


if __name__ == '__main__':
    haixue = HaiXue()
    print(haixue.catalogs)

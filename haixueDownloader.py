# -*- encoding: utf-8 -*-
import requests


class HaiXue():
    def __init__(self):
        self.cookies = None
        self.goods_id = '1066185'
        self.catalog_id = '16'
        self.catalogs = None
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


if __name__ == '__main__':
    haixue = HaiXue()
    print(haixue.catalogs)

# -*- encoding: utf-8 -*-
import requests


class HaiXue():
    def __init__(self):
        self.cookies = None

    def __login(self):
        resp = requests.post('http://highso.cn/doLogin.do',
                             data=dict(j_username=18396517057, j_password='yf920624',
                                       _spring_security_remember_me='off'))
        # print(resp.text)
        self.cookies = resp.cookies

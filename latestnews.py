import requests
import time

from bs4 import BeautifulSoup
from win10toast import ToastNotifier


# 获取最新的通知公告
def get_latest_news():
    # 获取通知公告页面
    response = requests.get('http://www.fyldbz.gov.cn/content/channel/52ba4de8f9a09af01d000034/')
    response.encoding = "utf-8"

    # 获取通知公告列表
    soup = BeautifulSoup(response.text, "lxml")
    lis = soup.find_all("ul", attrs={"class": "news"})[0].children
    news = list(lis)[1].text

    return news


# 获取最新排名信息
def find_latest_ranking():
    while True:
        # 判断最新是否是事业单位信息
        news = get_latest_news()
        if news.find("市直事业单位") > -1:
            # 创建windows toast 通知
            toaster = ToastNotifier()
            toaster.show_toast("死期到了", news, duration=20)
            break
        time.sleep(60)


if __name__ == "__main__":
    find_latest_ranking()

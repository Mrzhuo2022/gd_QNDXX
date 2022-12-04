import requests
from bs4 import BeautifulSoup
import re
import time
import json
import random


class Start:
    # 最新一期青年大学习
    url1 = "https://youthstudy.12355.net/saomah5/api/young/chapter/new"
    # 大学习事件
    url2 = "https://gqti.zzdtec.com/api/event"

    headers1 = {
        "Host": "youthstudy.12355.net",
        "X-Litemall-Token": "", # 青年大学习token
        "X-Litemall-IdentiFication": "young",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63080021)",
        "Accept": "*/*",
        "Referer": "https://youthstudy.12355.net/h5/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate"
    }
    headers2 = {
        "Host": "h5.cyol.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63080021)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://youthstudy.12355.net/h5/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate"
    }
    headers3 = {
        "Host": "gqti.zzdtec.com",
        "Origin": "https://h5.cyol.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63080021)",
        "Content-Type": "text/plain",
        "Accept": "*/*",
        "Referer": "", # m.html
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate"
    }

    def __init__(self):
        self.ur = ""
        self.info = ""
        self.key = ["打开页面", "开始学习", "播放完成", "课后习题"]
        self.guid = ""
        self.tc = ""
        self.tn = ""
        self.n = ""
        self.u = ""
        self.r = ""
        self.d = "cyol.com"
        self.w = 448
        self.m = ""

    def start(self):
        # 获取最新一期青年大学习地址
        r1 = requests.get(url=self.url1, headers=self.headers1, stream=True, verify=False)
        b1 = BeautifulSoup(r1.content, "lxml")
        self.ur = re.search("daxuexi/([a-zA-Z0-9]+)/index.html", str(b1)).group(0)[8:-11]
        self.u = "https://h5.cyol.com/special/daxuexi/%s/m.html?t=1" % self.ur
        self.r = "https://h5.cyol.com/special/daxuexi/%s/index.html" % self.ur
        # get https://h5.cyol.com/special/daxuexi/%s/m.html?t=1&z=201
        r2 = requests.get(url=self.u, headers=self.headers2, stream=True, verify=False)
        b2 = BeautifulSoup(r2.content, "lxml")
        sc = json.loads(re.search("打开页面.+", str(b2)).group()[8:-4])
        print("%s年第%s期青年大学习" % (sc['c'], sc['s']))
        self.headers3["Referer"] = self.u
        self.info = "{\"c\":\"%s\",\"s\":\"%s\"" % (sc['c'], sc['s'])
        self.tc = self.get_time(13)
        self.guid = self.generate_guid()

    def run(self):
        info = ["[%s}]" % self.info,
                "[%s,\"prov\":\"19\",\"city\":\"1\"}]" % self.info]
        self.tc = self.get_time(13)
        for i in range(4):
            self.tn = self.get_time(13)
            self.n = self.key[i]
            self.m = info[0] if i == 0 else info[1]
            data = {
                "guid": self.guid,
                "tc": self.tc,
                "tn": self.tn,
                "n": self.n,
                "u": self.u,
                "d": self.d,
                "r": self.r,
                "w": 448,
                "m": self.m
            }
            # post https://gqti.zzdtec.com/api/event
            post = requests.post(url=self.url2, headers=self.headers3, data=json.dumps(data), stream=True, verify=False)
            if "ok" in post.text:
                print("%s ok" % self.n)
            else:
                raise Exception("错误")
            time.sleep(3)


    @staticmethod
    def get_time(i) -> str:
        return str(time.time())[:i].replace(".", "")

    def generate_guid(self) -> str:
        guid = self.generate_num() + self.generate_num() + "-" + self.generate_num() + \
               "-" + self.generate_num() + "-" + self.generate_num() + "-" + \
               self.generate_num() + self.generate_num() + self.generate_num()
        return guid

    @staticmethod
    def generate_num() -> str:
        num = str(hex(random.randint(65536, 131072)))[2:6]
        return num


requests.packages.urllib3.disable_warnings()
new = Start()
new.start()
new.run()

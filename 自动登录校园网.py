import configparser
import requests
import time
import pywifi
import os
import re

class Loding(object):

    class WifiConnectError(BaseException):
        pass

    def connect(self):
        # 构造url
        url = 'http://10.2.5.251:801/eportal/?c=Portal&a=login&login_method=1&user_account=' + str(self.account) + '%40' + str(self.operator) + '&user_password=' + str(self.password)
        # 连接
        responed = requests.get(url=url)
        # 查验信息

        if(re.match(responed.text,'UmFkOkxpbWl0IFVzZXJzIEVycg==')):
            print("登录超限，请登录服务网页下线终端")


    def check_connect(self):
        try:
            print("正在验证网络状态")
            html = requests.get('https://cn.bing.com/')
            if(html.status_code == 200):
                return True
            else:
                return False
        except:
            return False

    def lode_ini(self):
        conf = configparser.ConfigParser()
        conf.read(r'相关信息.ini', encoding="utf-8")
        self.account = conf['MESSAGE']['account']
        self.password = conf['MESSAGE']['password']
        self.operator = conf['MESSAGE']['operator']
        self.wifi_name = conf['MESSAGE']['wifi_name']
        self.use_wifi = conf['MESSAGE']['use_wifi']

    def wifi_connect(self):
        print("正在连接 %s" % self.wifi_name)
        wifi = pywifi.PyWiFi()
        ifaces = wifi.interfaces()[0]
        ifaces.disconnect()
        #配置WiFi文件
        profile_info = pywifi.Profile()  
        profile_info.ssid = self.wifi_name
        profile_info.akm.append(pywifi.const.AKM_TYPE_NONE)
        #删除其他配置文件
        ifaces.remove_all_network_profiles()
        #加载配置文件
        temp_profile = ifaces.add_network_profile(profile_info)
        ifaces.connect(temp_profile)
        time.sleep(1)
        if ifaces.status() != pywifi.const.IFACE_CONNECTED:
            return False
        else:
            return True
        
    def main(self):
        try:
            self.lode_ini()
            if(self.use_wifi == '1'):  # 注意.ini文件读入的是str
                self.wifi_connect()
                time.sleep(1)
            self.connect()
            if self.check_connect():
                print("登录成功")
                return True
            else:
                print("登录失败,正在重试")
                return False
        except KeyError:
            print("请检查 相关信息.ini 文件位置")
            return False
        except :
            print("出现错误，正在重试")
            return False


while(not Loding().main()):
    pass
os.system('pause')








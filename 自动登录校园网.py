import configparser
import requests
import urllib
import socket
import time
import pywifi
import os
import re

class Loding(object):

    class WifiConnectError(BaseException):
        pass

    def connect(self):
        # 获取本机IP
        hostname = socket.gethostname()
        ip = socket.getaddrinfo(hostname,None)[-1][4][0]
        # 获取时间戳
        time_1 = round(time.time()*1000)
        # 构造url
        base_url = 'http://10.2.5.251:801/eportal/?'

        data = {
            'c':'Portal',
            'a':'login',
            'callback':'dr' + str(time_1),
            'login_method': '1',
            'user_account': str(self.account) + '@' + str(self.operator),
            'user_password': str(self.password),
            'wlan_user_ip': ip,          
            'wlan_user_mac': '',
            'wlan_ac_ip': '',
            'wlan_ac_name': '',
            'jsVersion': '3.0',
            '_':str(time_1+1500)
        }

        url = base_url + urllib.parse.urlencode(data)

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
            raise self.WifiConnectError
        
    def main(self):
        try:
            self.lode_ini()
            if(self.use_wifi == '1'):  # 注意.ini文件读入的是str
                self.wifi_connect()
                time.sleep(1)          # 等待1秒后继续，防止 [WinError 10051] 错误
            self.connect()
            if self.check_connect():
                print("登录成功")
            else:
                print("登录失败,请检查相关信息,并重试")
        except KeyError:
            print("请检查 相关信息.ini 文件位置")
        except self.WifiConnectError:
            print("wifi连接错误，请重新运行本程序")
        except :
            print("程序错误,请检查相关信息,并重试")
        finally:
            os.system('pause')

    def text(self):
        pass
        

Loding().main()







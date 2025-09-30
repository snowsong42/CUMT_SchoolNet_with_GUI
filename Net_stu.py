import requests
import pyautogui as pg

url = "http://10.2.5.251/"

# 修正data为字典格式
data = {
    "c": "Portal",
    "a": "login",
    "callback": "dr1759114957067",
    "login_method": "1",
    "user_account": "06245011@unicom",
    "user_password": "Snowsong_42",
    "wlan_user_ip": "10.3.20.131",
    "wlan_user_mac": "000000000000",
    "wlan_ac_ip": "wlan_ac_name",
    "jsVersion": "3.0",
    "_": "1759114945966"
}

# 修正header为字典格式
header = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "PHPSESSID=4kpirs4g4r5es03v8776pdf5d4",
    "Host": "10.2.5.251:801",
    "Referer": "http://10.2.5.251/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}

try:
    response = requests.post(url, data=data, headers=header)
    print(f"POST请求状态码: {response.status_code}")

    x = requests.get(url)
    arr1 = pg.alert(title='连接成功(oﾟvﾟ)ノ', text=x.reason, button='冲浪，冲！')
    print(arr1)
except Exception as e:
    print(f"发生错误: {e}")
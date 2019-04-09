import time
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
import zipfile
import requests
import pymongo
from pymongo.collection import Collection
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from mouse import move, click
from selenium.webdriver.support.ui import WebDriverWait


def get_random_info():
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['huya']
    id_collection = Collection(db, 'huya_users')
    info = id_collection.find_one_and_delete({})
    user_name = info["user_name"]
    password = info["user_password"]
    return user_name, password


def get_proxy():
    response = requests.get("http://111.231.77.152:9999/https.php?user=aqa314&pass=aqa314&count=1&tdsourcetag=s_pcqq_aiomsg")
    proxy = response.text.split(" ")[0]
    ip = proxy.split(":")[0]
    port = proxy.split(":")[1]
    return ip, port


def browser_login():
    search_key = eval(input("输入主播房间号:"))
    num = eval(input("输入机器人数量："))
    # time_sleep = eval(input("输入挂机时长："))
    ua = UserAgent()
    dcap = dict(DesiredCapabilities.CHROME)
    dcap["phantomjs.page.settings.userAgent"] = ua.random
    for i in range(num):
        info = get_random_info()
        ip = get_proxy()[0]
        port = get_proxy()[1]
        username = "aqa314"
        password = "aqa314"
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            }
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                  singleProxy: {
                    scheme: "http",
                    host: "%(ip)s",
                    port: %(port)s
                  }
                }
              }
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%(username)s",
                    password: "%(password)s"
                }
            }
        }
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        )
        """ % {'ip': ip, 'port': port, 'username': username, 'password': password}

        plugin_file = 'proxy_auth_plugin.zip'
        with zipfile.ZipFile(plugin_file, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_extension(plugin_file)
        driver = webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=dcap)
        driver.get("http://www.huya.com/{}".format(search_key))
        wait = WebDriverWait(driver, 10)
        try:
            if wait.until(lambda x: x.find_element_by_xpath(
                    "//div[@class='hy-nav-right un-login']/a[1]/span[@class='title clickstat']")):
                driver.find_element_by_xpath("//div[@class='hy-nav-right un-login']/a[1]/span[@class='title clickstat']"
                                             ).click()
                if wait.until(lambda x: x.find_element_by_xpath(
                        "//div[@class='UDBSdkLgn-switch UDBSdkLgn-webQuick']/img")):
                    time.sleep(1)
                    driver.find_element_by_xpath("//div[@class='UDBSdkLgn-switch UDBSdkLgn-webQuick']/img").click()
                    time.sleep(1)
                    # 输入账号与密码，并取消勾选一周之内自动登录
                    driver.find_element_by_xpath("//div[@class='UDBSdkLgn-common']/div[1]//input").clear()
                    driver.find_element_by_xpath("//div[@class='UDBSdkLgn-common']/div[1]//input").send_keys(info[0])
                    driver.find_element_by_xpath("//div[@class='UDBSdkLgn-common']/div[2]//input").clear()
                    driver.find_element_by_xpath("//div[@class='UDBSdkLgn-common']/div[2]//input").send_keys(info[1])
                    driver.find_element_by_xpath('//div[@class="UDBSdkLgn-mt10"]//input').click()
                    time.sleep(1)
                    # 点击登录按钮
                    driver.find_element_by_xpath("//div[@class='UDBSdkLgn-mt20 clearfix']/a").click()
                    # 捕捉是否出现要求进行手机验证异常，如果出现则关闭手机验证窗口
                    if WebDriverWait(driver, 1.5).until(lambda x: x.find_element_by_xpath(
                            "//i[@class='UDBSdkLgn-close J_UDBSdkLgnClose']")):
                        driver.find_element_by_xpath("//i[@class='UDBSdkLgn-close J_UDBSdkLgnClose']").click()
                    # 点击暂停播放按钮，限制流量
                    move(286, 629)
                    if WebDriverWait(driver, 1.5).until(lambda x: x.find_element_by_xpath(
                            "//div[@class='player-pause-btn']")):
                        click()
        except Exception as e:
            print(e.args)
            driver.quit()


browser_login()

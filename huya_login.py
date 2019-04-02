import time
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from tomorrow import threads
import zipfile
import requests

login_data = {}
ua = UserAgent().chrome
search_key = eval(input("输入主播房间号:"))
with open("C:/Users/admin/Desktop/100.txt", "r") as f:
    for each_line in f:
        ls = each_line.replace("\n", "").split("----")
        login_data[ls[0]] = ls[1]


def get_proxy():
    response = requests.get("http://111.231.77.152:9999/https.php?user=aqa314&pass=aqa314&count=1&tdsourcetag=s_pcqq_aiomsg")
    proxy = response.text.split(" ")[0]
    ip = proxy.split(":")[0]
    port = proxy.split(":")[1]
    return ip, port


@threads(10)
def browser_control():
    for k, v in login_data.items():
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
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_extension(plugin_file)
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get("http://www.huya.com/{}".format(search_key))
        time.sleep(3)
        driver.find_element_by_xpath("//div[@class='hy-nav-right un-login']/a[1]/span[@class='title clickstat']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='UDBSdkLgn-switch UDBSdkLgn-webQuick']/img").click()
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='UDBSdkLgn-common']/div[1]//input").clear()
        driver.find_element_by_xpath("//div[@class='UDBSdkLgn-common']/div[1]//input").send_keys(k)
        driver.find_element_by_xpath("//div[@class='UDBSdkLgn-common']/div[2]//input").clear()
        driver.find_element_by_xpath("//div[@class='UDBSdkLgn-common']/div[2]//input").send_keys(v)
        driver.find_element_by_xpath('//div[@class="UDBSdkLgn-mt10"]//input').click()
        time.sleep(3)
        driver.find_element_by_xpath("//div[@class='UDBSdkLgn-mt20 clearfix']/a").click()
        try:
            driver.find_element_by_xpath("/html/body/div[6]/div[2]/i").click()
        except:
            pass
        driver.refresh()


browser_control()




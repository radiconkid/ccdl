import logging
import os
import platform
import sys
import time
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from ccdl import (Binb2, ComicAction, ComicEarthstar, ComicLinkInfo,
                  ComicWalker, Ganma)
from ccdl.utils import RqProxy, SiteReaderLoader, get_windwos_proxy

if not os.path.exists("log"):
    os.makedirs("log")

log_file_path = "log/{}.log".format(time.strftime("%Y-%m-%d"))
fh = logging.FileHandler(filename=log_file_path, encoding="UTF-8")
logging.basicConfig(
    level=logging.INFO,
    handlers=[fh],
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("CCDL")

if 'Linux' in platform.platform().split('-'):
    executable_path = './chromedriver'
elif 'Windows' in platform.platform().split('-'):
    executable_path = './chromedriver.exe'
    proxy_server = get_windwos_proxy()
    if proxy_server:
        logger.info("Proxy Server Address (Enabled): {}".format(proxy_server))
        RqProxy.set_proxy(proxy_server, proxy_server)
    del proxy_server
else:
    logger.error("platform not win or linux, may failed")
    executable_path = './chromedriver'
    # raise ValueError("os")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches",
                                       ["enable-automation", "enable-logging"])

if __name__ == "__main__":
    driver = None
    is_exist = os.path.exists(executable_path)
    print("\nソースコード: https://github.com/radiconkid/ccdl")
    if is_exist:
        print("\nログイン（*を含む）が必要な場合は、プログラムが起動するブラウザで事前にログインし、対象のURL（任意のタブ）を読み込んでください。！\n")
        try:
            driver = webdriver.Chrome(options=chrome_options,
                                      executable_path=executable_path)
        except Exception as e:
            logger.error(traceback.format_exc())
            print("Chrome を起動できませんでした。Chrome と chromedriver のバージョンを確認してください\n" +
                  traceback.format_exc())
            print("使用できます http://npm.taobao.org/mirrors/chromedriver/ or https://chromedriver.chromium.org/downloads ダウンロード\n")

            driver = None
            if input("Do you want to continue? （y/n）") in ('y', 'Y', 'YES'):
                pass
            else:
                time.sleep(0.8)
                print("Bye~")
                time.sleep(0.8)

                sys.exit()
    else:
        print("\nプログラムが配置されているディレクトリに chromedriver が見つからないため、一部の Selenium ベースのコレクション サイトは利用できません。")
        print("使用できます http://npm.taobao.org/mirrors/chromedriver/ or https://chromedriver.chromium.org/downloads ダウンロード\n")

    print("\n>>>>>>>>exit<<<<<<<<\n")

    while True:
        url = input("url: ")

        if url == 'exit':
            print('Bye~')
            time.sleep(0.5)
            if driver:
                driver.quit()
            sys.exit()

        try:
            link_info = ComicLinkInfo(url)
        except Exception as e:
            logger.error("url: {}".format(url))
            logging.error(e)
            print("unsupported url: '{}'".format(url))
            continue
        reader = SiteReaderLoader(link_info, driver)
        if reader is not None:
            try:
                reader.downloader()
            except Exception as e:
                logger.error(traceback.format_exc())
                print("ダウンロード失敗! \n" + traceback.format_exc())
        else:
            print("not supported")
            continue

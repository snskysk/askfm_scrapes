from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import numpy as np
import unicodedata
import emoji
import random
from bs4 import BeautifulSoup
from PIL import Image
import cv2
import glob
import os.path

#import getpass
#import matplotlib.pyplot as plt
#import matplotlib.cm as cm
# -*- coding: utf-8 -*-


def main():

    #URL="http://localhost:8888/notebooks/Desktop/%E9%80%B2%E8%A1%8C%E4%B8%AD/%E3%83%86%E3%82%B9%E3%83%88%E9%96%A2%E9%80%A3/kankyou.ipynb"#askFMのURL
    #URL = 'https://ask.fm/'
    URL = 'https://grade-visualizer101.herokuapp.com/gv/hp/'


    print("---Chromeを起動---")
    driver = webdriver.Chrome()
    time.sleep(3)

    driver.get(URL)
    time.sleep(3)


    #一番上の質問文と答えを取得
    scroll = 1
    #for i in range(300):#　　最大スクロール回数を指定
    
    #スクロール前のスクリーンショット
    driver.save_screenshot("shot.png")
    time.sleep(2)    
    # スクロール
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #----------  end  -----------                
    time.sleep(2)
    
    #スクロール後のスクリーンショット
    driver.save_screenshot("shot2.png")
    imaf = "shot2.png"
    #----------  end  -----------      



if __name__ == "__main__":
    #URL = str(input("Please input URL:"))
    main()



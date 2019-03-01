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


#文字列に日本語が含まれているかどうか判定する関数
def is_japanese(string):
    for ch in string:
        name = unicodedata.name(ch) 
        if "CJK UNIFIED" in name or "HIRAGANA" in name or "KATAKANA" in name:
            return True
    return False

# 絵文字や改行を消し去るための関数。
# ただし対応できないものもある。
def remove_emoji(src_str):
    if "\n" in src_str:
        src_str = src_str.replace("\n","。")
    return ''.join(c for c in src_str if c not in emoji.UNICODE_EMOJI)

# スクロールを終了していいか見極めるための関数。
# スクロール前とスクロール後のスクリーンショットの一致率を返す
def pic_rate(before_scroll,after_scroll):
    IMG_SIZE = (200, 200)
    target_img = cv2.imread("{}".format(before_scroll))
    target_img = cv2.resize(target_img, IMG_SIZE)
    target_hist = cv2.calcHist([target_img], [0], None, [256], [0, 256])
    comparing_img = cv2.imread("{}".format(after_scroll))
    comparing_img = cv2.resize(comparing_img, IMG_SIZE)
    comparing_hist = cv2.calcHist([comparing_img], [0], None, [256], [0, 256])
    ret = cv2.compareHist(target_hist, comparing_hist, 0)
    return ret


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,(img_height - crop_height) // 2,(img_width + crop_width) // 2,(img_height + crop_height) // 2))


# 各IDを保存してあるtextファイル内を読みこみ、重複を見極めるための関数。Trueなら新たなユーザー
# textファイルは、利用できた、利用できなかった、たくさんのデータがとれた、の三つに分かれている
def id_checker(got_user_id):
    try:
        f = open('available_user_id.txt',encoding="utf-8")
        available = f.read()
        f.close()
        f = open('not_available_user_id.txt',encoding="utf-8")
        not_available = f.read()
        f.close()
        f = open('data_abandant_user_id.txt',encoding="utf-8")
        data_abandant = f.read()
        f.close()
        if got_user_id not in available and got_user_id not in not_available and got_user_id not in data_abandant:
            return True
        else:
            return False
    except:
        make_f = "new_file"
        f = open('available_user_id.txt','a',encoding="utf-8")
        f.write(make_f)
        f.close()
        f = open('not_available_user_id.txt','a',encoding="utf-8")
        f.write(make_f)
        f.close()
        f = open('data_abandant_user_id.txt','a',encoding="utf-8")
        f.write(make_f)
        f.close()
        f = open('available_user_id.txt',encoding="utf-8")
        available = f.read()
        f.close()
        f = open('not_available_user_id.txt',encoding="utf-8")
        not_available = f.read()
        f.close()
        f = open('data_abandant_user_id.txt',encoding="utf-8")
        data_abandant = f.read()
        f.close()
        if got_user_id not in available and got_user_id not in not_available and got_user_id not in data_abandant:
            return True
        else:
            return False




# ファイルの結合
def join_file(filePath):
    fileList = create_filelist(filePath)
    with open(filePath, 'wb') as saveFile:
        for f in fileList:
            data = open(f, "rb").read()
            saveFile.write(data)
            saveFile.flush()

# 連番ファイルのリスト作成
def create_filelist(filePath):
    pathList = []
    for index in range(100000):
        filename = file_indexed(filePath, index)
        # ファイルが存在しなければ終了
        if not os.path.exists(filename):
            break
        else:
            pathList.append(filename)
    return pathList

# ファイル名に指定のindex値をふる
def file_indexed(filePath, index):
    name, ext = os.path.splitext(filePath)
    return "{0}_{1}{2}".format(name, index, ext)

def main():
    n=0#開発時の確認指標
    id_list = []#useridを格納する空リスト
    bid_list = []#使い物にならなかったuseridを格納する空リスト
    gid_list = []#データを多くとれた有料ユーザーのIDを格納するリスト
    q_list = []#questionを格納する空リスト
    a_list = []#answerを格納する空リスト

    URL="https://ask.fm"#askFMのURL

    #
    #セット繰り返しの始まりでリストをリセットするかしないか問題
    #
    set_count = 0
    for v in range(howmany_set):
        print("---Chromeを起動---")
        driver = webdriver.Chrome()
        time.sleep(3)
        print("---https://ask.fmにアクセス---")
        ########## １セットごとのインターバル、適当な時間待つ 
        interval = random.randint(3,10)*25
        set_count += 1
        #interval = 10
        if set_count > 1:
            time.sleep(interval)

        for i in range(howmany_people):
            driver.get(URL)
            time.sleep(3)

            #トップページ下のアイコン一番左
            driver.find_element_by_css_selector("body > main > footer > div > nav.faces.rsp-gte-tablet > a:nth-child(1)").click()
            time.sleep(1)

            #投稿数を取得
            #post_count = driver.find_element_by_css_selector("#contentArea > section > ul > li:nth-child(1) > div.profileStats_number.profileTabAnswerCount")
            #print(post_count.text)


            try:
                #ユーザーIDを取得
                userid = driver.find_element_by_css_selector("#contentArea > section > header > div > a.profileBox_name > span:nth-child(1)")
                gotid = userid.text
                if id_checker(gotid) == False:#一度処理を行ったユーザーの場合はパス
                    pass
            except:
                print("unclear error")
                pass
            try:
                #一番上の質問文と答えを取得
                question = driver.find_element_by_css_selector("#contentArea > div.main-content.util-clearfix > div > section:nth-child(3) > div.item-pager > div > article:nth-child(1) > header > h2")
                top_q = question.text
                ans = driver.find_element_by_css_selector("#contentArea > div.main-content.util-clearfix > div > section:nth-child(3) > div.item-pager > div > article:nth-child(1) > div.streamItem_content")
                top_ans = ans.text
                if is_japanese(top_ans)== False:#一番上のQ&Aに日本語が含まれていなかった場合
                    if is_japanese(top_p) == False:
                        bid_list.append(gotid)#list append
                        print("judged")
                        #driver.get(URL)
                        n+=1
                        pass
                else:
                    id_list.append(gotid)#list append
                    ########################################################
                    ################
                    ################

                    scroll = 1
                    for i in range(300):#　　最大スクロール回数を指定
                        
                        #スクロール前のスクリーンショット
                        driver.save_screenshot("before.png")
                        imbe = "before.png"
                        #----------  end  -----------
                        time.sleep(2)
                        
                        # スクロール
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        #----------  end  -----------                
                        time.sleep(2)
                        
                        #スクロール後のスクリーンショット
                        driver.save_screenshot("after.png")
                        imaf = "after.png"
                        #----------  end  -----------      


                        #-----  画像の一致率を比較  -----
                        equal_rate = pic_rate(imbe,imaf)
                        if equal_rate<0.999999:
                            scroll+=1

                        else:#  画像が一致したら繰り返しを終了
                            break

                    soup = BeautifulSoup(driver.page_source, "html5lib")
                    elems_q = soup.select('.streamItem_header h2')
                    elems_a = soup.select('.streamItem_content')
                    for i in range(len(elems_q)):
                        elq = elems_q[i]
                        ela = elems_a[i]
                        elq = elq.getText()
                        q_list.append(elq)
                        if "View more" in ela.getText():
                            ela = ela.getText().replace("View more","")
                        a_list.append(ela)

                    #######################################################
                    ################
                    ################

                    gid_list.append(gotid)


            except:
                n+=1
                driver.get(URL)
                try:
                    if len(gotid)>0:
                        bid_list.append(gotid)#list append
                    else:
                        print("no gotid")
                except:
                    pass
            
        try:
            driver.close()
        except:
            pass
        #print("クエスチョンリスト：{}".format(len(q_list)))
        #print("アンサーリスト：{}".format(len(a_list)))
        #print("利用できたID：{}".format(id_list))
        #print("利用できなかったID：{}".format(bid_list))
        #print("データが豊富なID：{}".format(gid_list))

        #
        #ファイルの書き込みを繰り返しに入れるか入れないか問題
        #


        #URL="https://qiita.com/Hironsan/items/2466fe0f344115aff177"
        #driver = webdriver.Chrome()
        #driver.get(URL)

        textdata = []
        if len(q_list)>0:
            for k in range(len(q_list)):
                picked_q = remove_emoji(q_list[k])
                picked_a = remove_emoji(a_list[k])
                string = "Q：{0}\nA：{1}\n\n".format(picked_q,picked_a)
                textdata.append(string)
            file = open(your_filename + "_" + str(set_count-1) +'.txt', 'a', encoding="utf-8")
            try:
                file.writelines(textdata)
            finally:
                file.close()



        ##########利用可、利用不可、優良ID保存
        if len(id_list)>0:
            iddata = []
            for p in range(len(id_list)):
                strid = "{}\n".format(id_list[p])
                iddata.append(strid)
            file = open('available_user_id.txt','a',encoding="utf-8")
            try:
                file.writelines(iddata)
            finally:
                file.close()
        else:
            pass

        if len(bid_list)>0:
            iddata = []
            for p in range(len(bid_list)):
                strid = "{}\n".format(bid_list[p])
                iddata.append(strid)
            file = open('not_available_user_id.txt','a',encoding="utf-8")
            try:
                file.writelines(iddata)
            finally:
                file.close()
        else:
            pass

        if len(gid_list)>0:
            iddata = []
            for p in range(len(gid_list)):
                strid = "{}\n".format(gid_list[p])
                iddata.append(strid)
            file = open('data_abandant_user_id.txt','a',encoding="utf-8")
            try:
                file.writelines(iddata)
            finally:
                file.close()
        else:
            pass
    print("--- process completed ---")

if __name__ == "__main__":
    howmany_set = int(input("How many sets do you want to repeat?(何セット繰り返すか):"))
    howmany_people = int(input("How many people do you want to search at one time?(1セットにつき何人に検索をかけるか)"))
    your_filename = str(input("Please input filename(~here~.txt):"))
    main()
    join_file("{}.txt".format(your_filename))


#h2s = driver.find_element_by_tag_name('h2')
#print(h2s.text)
#element = driver.find_element_by_css_selector("#contentArea > div.main-content.util-clearfix > div > section:nth-child(3) > div.item-pager > div > article:nth-child(1) > header > h")
#element = driver.find_element_by_class_name("streamItem_heade")

#やることリスト
#ファイル名指定
#繰り返し回数指定set and count
#せっかくとったID（使ったのもつかわなかったのも）保存するかしないか？
#ファイル書き込み中にエラッた時の対処！！！！！！！！！！！！！！！
#ようは例外処理
#textfileに追記型にするとか
#✔　一人あたりから取るデータ量を増やす
#✔　￥nを除外する
#keyboardQイベントで終了する設計にする


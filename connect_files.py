import glob
import os.path

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

if __name__ == "__main__":
    input("<--このソフトではテキストファイルを結合することができます。--> Push enter>>>")
    input("<--結合したいいくつかのファイルを、「filename_0」に習いリネームして、「filename」にあたる部分を入力してください。--> Push enter>>>")
    your_filename = str(input("Please input filename what you want to concat(~here~.txt):"))
    join_file("{}.txt".format(your_filename))

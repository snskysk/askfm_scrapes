def main():
    f = open('{0}.txt'.format(filename),encoding="utf-8")
    print(len(f.readlines()))
    f.close()

if __name__ == "__main__":
    input("<--このソフトではテキストファイルの行数を数えることができます。--> Push enter>>>")
    filename = str(input("Please input filename what you want to count(~here~.txt):"))
    main()

from MiniReadability import MiniReadability


# url = "https://lifehacker.ru/2014/11/27/kursy-ot-google/"
print("Write URL")
url = input()
t = MiniReadability(url)
print("\n" + t.text())

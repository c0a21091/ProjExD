import random
def shutudai():
    print(f"対象文字{taishoumoji}")
    print(f"表示文字{hyoujimoji}")

def kaitou():
    a1 = int(input("欠損文字はいくつあるでしょうか？："))
    for i in range(kesson):
        if a1 == kesson:
            print("正解です。それでは、具体的に欠損文字を１つずつ入力してください")
            for f in range(kesson):
                a2 = input(f"{f+1}つ目の文字を入力してください：")
            if a2 not in kessonmoji:
                print("不正解です")
                break
            elif a2 in kessonmoji:
                print("正解です")
                break
        else:
            print("不正解です。またチャレンジしてください")
            break
if  __name__ == "__main__":
    moji = [chr(i)for i in range(ord("a"),ord("z")-1)]
    random.shuffle(moji)
    kesson = random.randint(1,9)
    hyouji=10-kesson
    taishoumoji = moji[:10]
    hyoujimoji = moji[:10]
    for i in range(kesson):
        kessonmoji = random.choice(hyoujimoji)
        hyoujimoji.remove(kessonmoji)
    random.shuffle(hyoujimoji)
    shutudai()
    kaitou()
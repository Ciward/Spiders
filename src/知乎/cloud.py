import wordcloud
from matplotlib import pyplot as plt
def cloud(n):
    stopwords = set()
    stopwords={'热门话题','热点话题','新闻','热点新闻','热门新闻'}
    w=wordcloud.WordCloud(width=2000,
                          font_path=r'C:\Windows\Fonts\simfang.ttf',
                          height=1400,
                          stopwords=stopwords,
                          background_color="white")
    with open('./outcome/text'+n+'.txt', 'r', encoding="utf-8") as f:
        txt=f.read()
        print(txt)
        w.generate(txt)
        w.to_file('./outcome/pywcloud'+n+'.png')
    plt.imshow(w)  # 用plt显示图片
    plt.axis('off')  # 不显示坐标轴
    plt.show()  # 显示图片
#cloud(1)
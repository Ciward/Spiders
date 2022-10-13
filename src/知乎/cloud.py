import wordcloud,os
stopwords = set()
stopwords.add("热点话题")
w=wordcloud.WordCloud(width=1000,
                      font_path=r'C:\Windows\Fonts\simfang.ttf',
                      height=700,
                      stopwords=stopwords,
                      background_color="white")
with open('text.txt', 'r', encoding="utf-8") as f:
    txt=f.read()
    #print(txt)
    w.generate(txt)
    w.to_file("pywcloud.png")
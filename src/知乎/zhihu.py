
from bs4 import BeautifulSoup           #网页解析，获取数据
import re,requests,os,time,difflib,xlwt            #正则表达式，进行文字匹配     #指定URL，获取网页数据#进行excel操作
from cloud import cloud
class File():
    fp = None
    # 词云图的txt
def main():

#     1. 获取网页
    baseurl = "https://www.zhihu.com/billboard"
#     2. 获取和解析数据
        # 词云图的txt
    if not os.path.exists("./outcome"):
        os.makedirs("./outcome")
    File.fp=open(os.path.join("./outcome/", 'text'+time.strftime('%Y-%m-%d-%H')+'.txt', ), 'a', encoding="utf-8")
    datalist = getData(baseurl)
#     3. 保存数据
    print(datalist)
    savepath = "./outcome/hot"+time.strftime('%Y-%m-%d-%H')+".xls"
    saveData(datalist,savepath,0)
    File.fp.close()
    cloud(time.strftime('%Y-%m-%d-%H'))


def getData(baseurl):
    datalist = []
    html = askURL(baseurl)
    # print(html)
    soup = BeautifulSoup(html, "html.parser")  # 形成树形结构对象
    #求title和热度
    for item in soup.find_all(name="div",class_="HotList-itemBody"):
        item=str(item)

        #print(item)
        data=[0 for i in range(4)]
        title = re.findall(r'HotList-itemTitle">(.*?)</div>',item,re.S)
        for i in title:
            data[0]=i.replace(' ','')
            hot=re.findall(r'HotList-itemMetrics">(.*?) 万热度</div>', item,re.S)

            if hot==[]:data.append('广告')
            else:
                for i in hot:data[3]=int(i)

        datalist.append(data)
    #print(datalist)
    #在总html里求link特征编号列表
    link_data_list=re.findall(r'"cardId":"Q_(.*?)"',html,re.S)
    #print(link_data_list)

    #根据link求topic
    #依次进入各link，gettopic（）
    di=0  #偏移量
    for i in range(len(datalist)):

        iurl='https://www.zhihu.com/question/'+link_data_list[i+di]+'?utm_division=hot_list_page'
        a=gettopic(iurl,i)
        print(a[1])
        #以下判断是否有link，不然会错位
        #痛，太痛了！
        if difflib.SequenceMatcher(None,a[1].replace(' ',''), datalist[i][0]).quick_ratio()>0.6:
            datalist[i][1]=iurl
            datalist[i][2]=a[0]
        else:
            datalist[i][1]='暂无'
            datalist[i][2]='可能是直播或讨论'
            di-=1
        #time.sleep((0.4))
    return datalist

def gettopic(url,i):
    html = askURL(url)
    title=re.findall(r'<title data-rh="true">(.*?) - 知乎', html, re.S)[0]
    #print(html)
    res=''
    soup = BeautifulSoup(html, "html.parser")  # 形成树形结构对象
    for item in soup.find_all(name="div", class_="css-1gomreu"):
        #print(item)
        item=str(item)
        try:
            # 去除汉字之外的字符
            res += re.sub(r'[^\u4e00-\u9fa5]','',re.findall(r'class="css-1gomreu">(.*?)</div>', item, re.S)[0]).replace(' ','') + ' '
        except:pass

    if i<3: # 榜前三名进行加重写入使词云图更加客观
        File.fp.write(res*(6-2*i))
    else:File.fp.write(res)
    #print(res)
    return (res,title)

def saveData(datalist,savepath,n):
    if n==0:
        book = xlwt.Workbook(encoding="utf-8")
        sheet = book.add_sheet("知乎热榜",cell_overwrite_ok=True)
        col = ["序号","名字","链接","话题",'热度']
        for i in range(0,5):
            sheet.write(0,i,col[i])
        sheet.col(1).width = 20000
        sheet.col(2).width=10000
        sheet.col(3).width =18000
        for i in range(0,len(datalist)):
            data = datalist[i]
            sheet.write(i+1,0,i+1)
            # print(data)
            for j in range(0,4):
                sheet.write(i+1,j+1,data[j])
    book.save(savepath)  # 保存数据表


def askURL(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}

    response = requests.get(url, headers=headers)
    html = response.text

    return html

if __name__ == "__main__":
    main()
    print("爬取完毕！")

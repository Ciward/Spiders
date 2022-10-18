from bs4 import BeautifulSoup
import re,requests,os,time,xlwt
import tkinter.messagebox
class D():
    datalist=[]
    i=0
def askURL(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42"}
    response = requests.get(url, headers=headers)
    html = response.text

    return html

def getData(baseurl):
    html = askURL(baseurl)
    #print(html)
    soup = BeautifulSoup(html, "html.parser")  # 形成树形结构对象
    for item in soup.find_all(name="div",style = "float:left"):
        data = [0 for i in range(3)]
        item = str(item)
        # 1.get title
        title = re.findall(r'title="(.*?)</a></div>', item, re.S)
        for i in title:data[0]=i
        # 2.get link
        link=re.findall(r'<a href="(.*?)" ', item, re.S)[0].replace('amp;','')# remove 'amp;'
        if link[0:5]!='https':# format the link
            link='https://www.bkjx.sdu.edu.cn/'+link
        data[1]=link
        D.datalist.append(data)


    for s in re.findall(r'style="float:right;">(.*?)</div>',html,re.S):
        D.datalist[D.i][2]=s[1:11]
        if int(time.strftime('%d'))-int(D.datalist[D.i][2][8:10])<6 and D.i<6:
            tkinter.messagebox.showinfo('您有近5天的新通知，请注意查收',D.datalist[D.i][0]+D.datalist[D.i][2])
        D.i+=1

def main():
    #     1. 获取网页,只获取前两页
    for page in range(1,3):
        baseurl = "https://www.bkjx.sdu.edu.cn/sanji_list.jsp?totalpage=300&PAGENUM="+str(page)+"&urltype=tree.TreeTempUrl&wbtreeid=1010"
    #     2. 获取和解析数据
        getData(baseurl)
        print('please wait...')
        if not os.path.exists("./outcome1"):
            os.makedirs("./outcome1")
        saveData(D.datalist,"./outcome1/notice"+time.strftime('%Y-%m-%d-%H')+".xls")
        time.sleep(1)

def saveData(datalist,savepath):
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("山大通知",cell_overwrite_ok=True)
    col = ["序号","标题","链接","时间"]
    for i in range(0,4):
        sheet.write(0,i,col[i])
    sheet.col(1).width = 20000
    sheet.col(2).width=18000
    sheet.col(3).width =5000
    for i in range(0,len(datalist)):
        data = datalist[i]
        sheet.write(i+1,0,i+1)
        # print(data)
        for j in range(0,3):
            sheet.write(i+1,j+1,data[j])
    book.save(savepath)  # 保存数据表
if __name__ == "__main__":
    main()
    print("爬取完毕！")
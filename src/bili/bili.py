
import requests,os,time,json,xlwt # json解析

def get_html(url):  # 向网站发送请求，代码格式固定
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'}
    cookie = {'Cookie': "buvid3=FCB0C82A-B50C-436D-7DBE-FA69BCB7E1A250084infoc; i-wanna-go-back=-1; _uuid=48BF3681-A46F-2EF1-21AF-2B10F241AAC1E50394infoc; buvid_fp=9480fc90bdaf876c705667024889254f; buvid4=F8278018-39CF-C856-32B2-86D571E8BAD151634-022072911-HmLv33rFB9b4JI1IpmPJnQ%3D%3D; rpdid=|(u|k|YRl~Yl0J'uYlm|YlY~J; DedeUserID=2120384597; DedeUserID__ckMd5=12062b6da4c6910f; SESSDATA=a6c55526%2C1676183718%2C62ed3*81; bili_jct=3ee3cdb518f2aea8458afab1edbc3b14; b_ut=5; is-2022-channel=1; b_nut=100; LIVE_BUVID=AUTO6416628067661990; nostalgia_conf=-1; CURRENT_QUALITY=64; PVID=1; bsource=search_bing; sid=80ngxfj0; fingerprint=92f658ec09a627b90b07246f25d43db1; CURRENT_FNVAL=4048; bp_video_offset_2120384597=719468070935986200; b_lsid=4D5CC2D4_183FACA89E6; innersign=1"}
    r = requests.get(url=url, headers=headers, cookies=cookie)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r.content.decode()

def get_information(id):  # 得到页面信息
    datalist = [id]
    for page in range(1,6):
        url = "https://api.bilibili.com/x/relation/followings?vmid=" + id + "&pn=%d&ps=20&&jsonp=jsonp" % page
        html = get_html(url)  # 得到json
        value = json.loads(html)  # 加载json
        datas=value.get("data")
        if(datas==None):
            # if value.get("message")=='请求错误':
            break

        datas=datas.get('list')
        for i in range(len(datas)):
            data=[]
            mid=datas[i].get("mid")
            data.append(str(mid))
            data.append(datas[i].get("uname"))
            list1=get_level(mid)
            data.append(list1[0])
            data.append(list1[1])
            datalist.append(data)
            time.sleep(0.1)
    return datalist # 返回信息
def get_level(mid):
    url = "https://api.bilibili.com/x/web-interface/card?mid=%d&jsonp=jsonp&article=true" % mid
    html = get_html(url)
    value = json.loads(html)
    level = value.get("data").get("card").get("level_info").get("current_level")
    fans = value.get("data").get("card").get("fans")
    return  (level, fans)
def saveData(datalist,savepath,id1,id2):

    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet(id1+'和'+id2+'的关注列表交集',cell_overwrite_ok=True)
    col = ["序号","id","名字","等级",'粉丝数']
    for i in range(0,5):
        sheet.write(0,i,col[i])
    sheet.col(1).width = 8000
    sheet.col(2).width = 8000
    for i in range(0,len(datalist)):
        data = datalist[i]
        sheet.write(i+1,0,i+1)
        # print(data)
        for j in range(0,4):
            sheet.write(i+1,j+1,data[j])
    book.save(savepath)
    # 保存数据表

#print(get_html(url))
def compare(datalist1,datalist2):
    res=[]
    for a in datalist1:
        for b in datalist2:
            if a[0]==b[0]:
                res.append(a)
    return res
def main():
    mid1 = '12449656'
    mid2='484591211'
    '''mid1 = input()
    mid2 = input()'''
    #     2. 获取和解析数据
    print('please wait...')
    datalist1=get_information(mid1)
    datalist2=get_information(mid2)
    if datalist1==[] or datalist2==[]:
        print('用户已设置隐私，无法查看')
        return -1
    print('爬取完毕，正在写入！！！')
    if not os.path.exists("./outcome2"):
        os.makedirs("./outcome2")
    saveData(compare(datalist1,datalist2),"./outcome2/u_list"+time.strftime('%Y-%m-%d-%H')+".xls",mid1,mid2)
    time.sleep(1)
main()
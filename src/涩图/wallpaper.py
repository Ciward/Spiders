import requests,os,re,time
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE/10.0.2287.0'} # 添加用户代理

for i in range(1,10):
    url = 'https://wallhaven.cc/toplist?page='+str(i)

    response = requests.get(url, headers=headers)
    html=response.text

    data_list = re.findall(r'data-wallpaper-id="(.*?)"', html, re.S)
    print(data_list)
    save_dir='picture'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for data in data_list:
        image_url='https://w.wallhaven.cc/full/'+data[0]+data[1]+'/wallhaven-'+data+'.jpg'
        image_data = requests.get(url=image_url, headers=headers).content
        with open(os.path.join(save_dir,data+'.jpg'), 'wb') as fp:
            fp.write(image_data)
        time.sleep(1)
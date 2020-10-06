'''
Created on 2018/03/11

@author: Zizhu Zhang
'''
eight_url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&pc=50&smk=&po1=25&po2=99&tc=0401303&tc=0401304&shkr1=03&shkr2=03&shkr3=03&shkr4=03&ta=13&cb=0.0&ct=8.0&co=3&co=4&md=01&md=02&md=03&md=04&et=9999999&mb=0&mt=9999999&cn=9999999&fw2=&pn='
import requests

def getHomeInfo(homeinfo):
    homedetail = homeinfo.find('div',class_='cassetteitem-detail-body')
    
    hometype= homedetail.find('span',class_='ui-pct--util1');
    hometitle =homedetail.find('div',class_='cassetteitem_content-title').text;
    homeaddress=homedetail.find('li',class_='cassetteitem_detail-col1').text;
   
    home_bus_list   =homedetail.find('div',class_='cassetteitem_detail-text');
    
    home_bus_str = ''
    for bus in home_bus_list:        
        home_bus_str+=bus+','
    
    home_date_list = homedetail.find_all('li',class_='cassetteitem_detail-col3')
    home_date_str = ''    
    for _date in home_date_list:
        home_date_str +=_date.find('div').text+','
   
        
    home_money_info = homeinfo.find('div',class_='cassetteitem-item')
    home_money_body =home_money_info.find_all('tbody')
    for home_money in home_money_body:        
        home_td=home_money.find_all('td')
        
        home_label =home_td[0].text.strip();
        
        home_floor =(home_td[1].find_all('td'))
        print(home_floor)
        home_fee   =home_td[2].text;
        home_manage_fee =home_td[3].text;
        home_other_fee  = home_td[4].text;
        
        home_zoom  = home_td[5].text;
        home_size  = home_td[6].text;
        home_link   = home_money_body.find('a',limit=1).attr['href']
    
    
    print(hometype.text)

def getEachUrlContents(url):
    r       = requests.get(url)
    r.encoding=r.apparent_encoding
    demo    =r.content
    from bs4 import BeautifulSoup
    soup            = BeautifulSoup(demo,"html.parser")
    homeinfo        = soup.find_all('div',class_='cassetteitem');
    for item in homeinfo:
        getHomeInfo(item)
        break;
getEachUrlContents(eight_url)




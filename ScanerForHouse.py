# -*- coding: utf-8 -*-
import scrapy
from suumo import SUUMO
from _io import open

class ScanerforhouseSpider(scrapy.Spider):
    name = 'ScanerForHouse'
    allowed_domains = ['suumo.jp']
    paramter        = 'ar=030&bs=040&pc=50&smk=&po1=25&po2=99&tc=0401303&tc=0401304&shkr1=03&shkr2=03&shkr3=03&shkr4=03&ta=13&cb=0.0&ct=8.0&co=3&co=4&md=01&md=02&md=03&md=04&et=9999999&mb=0&mt=9999999&cn=9999999&fw2=&pn='
    start_urls      = ['https://suumo.jp/jj/chintai/ichiran/FR301FC001/?%s'%paramter]
    orign_url       = 'https://suumo.jp/'

    def parse(self, response):       
      
        homelist = response.css('#js-bukkenList .cassetteitem')
#         SUUMO.connectmysql(self);
        for home in homelist:
            room        =home.css('.cassetteitem-item .cassetteitem_other tbody')
            name        =home.css('div.cassetteitem-detail .cassetteitem_content-title::text').extract_first()
#             name        =self.filterhtml(name)
            
            address     =home.css('div.cassetteitem-detail .cassetteitem_content-body .cassetteitem_detail .cassetteitem_detail-col1::text').extract_first(),
            address     =self.filterhtml(address)
            
            station     =self.getStationInfo(home.css('div.cassetteitem-detail .cassetteitem_content-body .cassetteitem_detail .cassetteitem_detail-col2 div')),
            
            built_year  =home.css('div.cassetteitem-detail .cassetteitem_content-body .cassetteitem_detail .cassetteitem_detail-col3 div')[0].css('::text').extract_first(),
            built_year  =self.filterhtml(built_year)
            
            total_floor =home.css('div.cassetteitem-detail .cassetteitem_content-body .cassetteitem_detail .cassetteitem_detail-col3 div')[1].css('::text').extract_first(),
            total_floor =self.filterhtml(total_floor)
            
            detail      =self.getRoomInfo(room)
            suumoinfo   =SUUMO(name,address,built_year,total_floor,detail,station)
            suumoinfo.action();

#             yield item
            #nextpage
            
          
            nexturl =self.orign_url+response.css('.pagination_set .pagination_set-nav p.pagination-parts a')[-1].css('::attr(href)').extract_first()
            yield scrapy.Request(url=nexturl,callback=self.parse)
       
    def getStationInfo(self, stationlist):        
        result ={}
        for i in range(len(stationlist)): 
            #self.log(self.cleanhtml(buildinglist[i].css('div').extract_first()))           
            result.update({
                i:stationlist[i].css('::text').extract_first()
                }
            )
        return result
    
    def getRoomInfo(self,roominfolist):
        result={}
        #with open('log.txt','w') as f:
            #f.write('floor:'.join((roominfolist[0].css('tr td'))[4].css('li span')[0].css('::text').extract_first()))
            
        for i in range(len(roominfolist)):
            roominfo=roominfolist[i].css('tr td')
            roomdetail ={
                'floor'             :roominfo[2].css('::text').extract_first(),
                'rent_fee'          :roominfo[3].css('li span::text').extract_first(),
                'manage_fee'        :roominfo[3].css('li span')[1].css('::text').extract_first(),
                'other_fee_siki'    :roominfo[4].css('li span')[0].css('::text').extract_first(),
                'other_fee_present' :roominfo[4].css('li span')[1].css('::text').extract_first(),
                'room_shape'        :roominfo[5].css('li span::text').extract_first(),
                'room_size'         :roominfo[5].css('li span')[1].css('::text').extract_first(),
                }
            
            result.update({
                i:roomdetail,
                })
        return result
    def filterhtml(self,text):      
        return text[0];
    

  
        

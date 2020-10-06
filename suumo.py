'''
Created on 2018/06/02

@author: Zizhu Zhang
'''
import MySQLdb 
class SUUMO(object):
    cur         =''
    conn        =''
    
    name        =''
    address     =''
    built_year  =''
    total_floor =''
    detail      ={}
    station     ={}
    
    def __init__(self,_name,_address,_built_year,_total_floor,_detail,_station):
        self.name        =''.join(_name).strip()
        self.address     =''.join(_address).strip()
        self.built_year  =''.join(_built_year).strip()
        self.total_floor =''.join(_total_floor).strip()
        self.detail      =_detail
        self.station     =_station
        self.connectmysql()
    
    def action(self):
        #start 
        if self.validate():
            if  not self.isExsitsBuilding():                
                self.InsertDB()
                print('success')
        else:
            print('fail')               
       
#         self.closemysql()
    
    
    def connectmysql(self):
        conn = MySQLdb.connect(host="localhost",    
                         user="root",         
                         passwd="",  
                         db="suumo")
        conn.set_character_set('utf8')
        self.conn=conn
        self.cur = conn.cursor()        
    
    def isExsitsBuilding(self):
        _flag = False
        self.cur.execute("SELECT name FROM scrapy_building where name='%s'"%self.name)
        
        for row in self.cur.fetchall():
            
            if row[0] == self.name:
                _flag= True
                break
            else:
                continue        
        return _flag                   
         
       
            
    def closemysql(self):
        self.conn.close()
        
    def validate(self):        
        if self.name is None:
            return  False
        elif self.address is None:
            return  False
        elif self.built_year is None:
            return  False
        elif self.total_floor is None:
            return  False        
        else:
            return True
        
    def InsertDB(self):
              
        self.cur.execute('insert into scrapy_building(name,address,built_year,total_floor)values("{0}","{1}","{2}","{3}")'.format(self.name,self.address,self.built_year,self.total_floor))
        
        if self.detail is not None:
            build_id=self.conn.insert_id()  
                   
            for i in range(len(self.detail)):
                room =self.detail[i] 
                    
                if self.validateroom(room):                                      
                    self.cur.execute('insert into scrapy_room(building_id,floor,rent_fee,manage_fee,other_fee_siki,other_fee_present,room_shape,room_size)values("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}")'.format(build_id,"".join(room['floor']).strip(),"".join(room['rent_fee']).strip(),"".join(room['manage_fee']).strip(),"".join(room['other_fee_siki']).strip(),"".join(room['other_fee_present']).strip(),"".join(room['room_shape']).strip(),"".join(room['room_size']).strip()))
                else:
                    continue;
                
#         if self.station is not None: 
# #             print(len(self.station[0]))
#             for i in range(len(self.station[0])):                
#                 station=self.station[0]
# #                 print(station[i])
#                 if self.validatestation(station):                    
#                     self.cur.execute("insert into scrapy_station(building_id,station_info)values('{0}','{1}')".format(build_id,station[i]))
#                 else:
#                     continue;
         
        self.conn.commit()
#         self.closemysql()
        
    def validateroom(self,room):
        
        if room['floor'] is None:
            return False
        if room['rent_fee'] is None:
            return False
        if room['room_shape'] is None:
            return False
        if room['room_size'] is None:
            return False
        else:
            return True
    
    def validatestation(self,station):
        if station is None:
            return False        
        else:
            return True
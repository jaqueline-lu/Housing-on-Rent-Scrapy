import requests
import numpy as np
import re
import geonamescache
import csv
import pandas as pd

base_URL='https://www.rent.com/'
base_postfix = '/apartments_condos_houses_townhouses'
properties_list = []

def get_headers():
    # Creating headers.
    headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'accept-encoding': 'gzip, deflate, sdch, br',
               'accept-language': 'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
               'cache-control': 'max-age=0',
               'upgrade-insecure-requests': '1',
               'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    return headers

def save_to_csv(property,city_name,PATH):
    housing = pd.DataFrame(columns=['name','beds','baths','type of house','price','rating','num of rating','address','url'],
                 data=property)
    try:
        housing.to_csv(PATH + city_name+'.csv',encoding='utf-8')
    except:
        print("[ERROR]: PATH is not correct...")
    
    print("Saved to CSV file successfully!")
    
def Get_house_info(city_url,page_num,house_num):
    print("getting info...")
    count=0
    
    #loop over the pages
    city_url_raw = city_url + '?page='
    for i in range(page_num):
    
        city_url = city_url_raw + str(i+1)   
        
        html = requests.get(city_url,headers=get_headers())    
        if html.status_code != 200:
            print("[ERROR]: site cannot be opened or city name is wrong...")
    
        soup = BeautifulSoup(html.text,'lxml')
        all_blocks = soup.find_all('div',{'data-tid':'listing-section'})
        
        #save each part of information
        for each_house in all_blocks:
            count+=1
            
            #price of the house
            price = each_house.find_all('div',{'class':'_3e12V','data-tid':'price'}) 
            each_price = ' '.join(map(str,[p.text for p in price])) 

            #rating and number of people rating
            rating = each_house.find_all('div',{'class':'_1J1DR'}) 
            each_rating = ' '.join(map(str,[r['style'].replace("width:","") for r in rating]))
            num_rating = each_house.find_all('div',{'class':'_2ti3Q hnGZw _3XmXI _2z-p_ _2LCM5 _3NBE2 K_C0q'}) 
            each_num_rating = ' '.join(map(str,[n.text.replace("(","").replace(")","") for n in num_rating ]))
        
            #address
            address = each_house.find_all('div',{'data-tid':'listing-info-address'})
            each_address = ' '.join(map(str,[a.text for a in address])) #TODO: need to deal with the street and city address
        
            #name of the house and url
            name = each_house.find_all('a',{'data-tag_item':'property_title'})
            each_name = ' '.join(map(str,[n.text for n in name]))
            each_url_raw = ' '.join(map(str,[n['href'] for n in name]))
            each_url = base_URL+each_url_raw
            
            #number of beds and baths, and the type of house
            info = each_house.find_all('div',{'data-tid':'beds-baths'})
            each_info_raw = ' '.join(map(str,[e.text for e in info]))
            each_house_info = ' '.join(map(str,['' if each_info_raw.find('Studio') else 'Studio' ]))
            
            if each_info_raw != '':
                try:
                    each_bath_num = each_info_raw.split('•')[1].replace(" Bath","").replace(" ","").replace("s","").replace("–Bath","").replace("–","~")
                except: each_bath_num = ''
                try:
                    each_bed_num = each_info_raw.split('•')[0].replace("Studio–","").replace("Studio","").replace(" Beds","").replace(" Bed","").replace("–","~")
                except: each_bed_num = ''
            else:
                each_bath_num,each_bed_num = '',''
                
            #save the data to output
            data = {'name':each_name,
                'beds': each_bed_num,
                'baths': each_bath_num,
                'type of house':each_house_info,
                'price': each_price,
                'rating':each_rating,
                'num of rating':each_num_rating,
                'address': each_address,
                'url': each_url
                }
            properties_list.append(data)

            #num of houses reached, just stop the loop
            if count == house_num:
                return properties_list
              
    return properties_list

#def state_name(city_name):
    
def isNumber(s) :
    for i in range(len(s)) : 
        if s[i].isdigit() != True : 
            return False
    return True
    
def main():
    
    #get city name from input
    city_name = input('Input the city name or ZIP: ')
    city_name = city_name.replace(" ", "-")

    if isNumber(city_name):
        city_url = base_URL + 'zip-' + city_name + base_postfix
    else:
        try:
            city_url = base_URL + 'california/' + city_name + base_postfix 
            #print(city_url)
        except:
            print("[ERROR]: city name error or information not available...")
            return
   
    #get house number from input
    house_num = input('Input the number of houses information wanted: ')
    try:
        page_num = (int(house_num) // 30) +1
    except:
        print("[ERROR]: page number not an integer... ")
        return
    
    #get path from input
    PATH = input('Input where you want to save the file: (hit Enter for currect directory) ')
    
    property = Get_house_info(city_url,int(page_num),int(house_num))
    save_to_csv(property,city_name,PATH)

if __name__ == '__main__':
    #while true:
    main()

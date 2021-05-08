from requests import get
from bs4 import BeautifulSoup


def check_pages_amount(city):
    URL = f'https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/{city}'
    try:
        page_links = BeautifulSoup(get(URL).content, 'html.parser').find('div', class_ = 'pager').find_all('span', class_ = 'fleft')
        amount_pages = int(page_links[len(page_links)-1].find('span').string)
    except:
        amount_pages = 1

    return amount_pages



def import_data(city):
    """Zwraca listę mieszkań na sprzedaż w serwisie OLX w wybranym mieście"""
    
    
    amount_pages = check_pages_amount(city)

    all_offers_list = []

    for i in range(1, amount_pages+1):
        URL = f'https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/{city}/?page={i}'
        page = get(URL).content 
        bs = BeautifulSoup(page, 'html.parser') #zamienia stronę na BS
        
        oferts_list = bs.find(id="offers_table").find_all(class_="offer-wrapper") #lista z ofertami
        
        for ofert in oferts_list:
            price = float(ofert.find('p', class_="price").find('strong').string.replace(' ', '').replace('zł', '').replace(',', '.'))
            name = ofert.find('td', class_ = 'title-cell').find('strong').string
            link = ofert.find('td', class_ = 'title-cell').find('a').get('href')
            
            meters, year, rooms, market, storey = '', '', '', '', ''
            
            if (link[12:15] == 'oto'): #jesli ogloszenie z otodom
                page_content = BeautifulSoup(get(link).content, 'html.parser')
                table_data = page_content.find(class_ = 'egzohkh2').find_all('div')
                for data in table_data:
                    name_label = data.get('aria-label')
                    if(name_label == 'Powierzchnia'):
                        meters = float(data.find(class_ = 'ev4i3ak0').string.replace('m²', '').replace(' ', '').replace(',', '.'))

                    elif(name_label == 'Rok budowy'):
                        year = int(data.find(class_ = 'ev4i3ak0').string)

                    elif(name_label == 'Liczba pokoi'):
                        rooms = int(data.find(class_ = 'ev4i3ak0').string.replace(' ', ''))
                    elif(name_label == 'Rynek'):
                        market = data.find(class_ = 'ev4i3ak0').string.replace(' ', '')  
                        
                    elif(name_label == 'Piętro'):
                        storey = data.find(class_ = 'ev4i3ak0').string
                        if (storey == 'parter'):
                            storey = 0
                        elif(storey == 'suterena'):
                            storey = -1
                                
            elif (link[12:15] == 'olx'):
                info_list = BeautifulSoup(get(link).content, 'html.parser').find('ul', class_ = ('css-sfcl1s')).find_all('p')
                for info in info_list:
                    if((info.string).startswith('Powierzchnia')):
                        meters = float(info.string.replace('Powierzchnia:', '').replace('m²', '').replace(' ', '').replace(',', '.'))
                    elif((info.string).startswith('Rynek')):
                        market = info.string.replace('Rynek:', '').replace(' ', '')
                    elif((info.string).startswith('Poziom')):
                        storey = info.string.replace('Poziom:', '').replace(' ', '')
                        if (storey == 'parter'):
                            storey = 0
                        elif(storey == 'suterena'):
                            storey = -1

                    elif((info.string).startswith('Liczba pokoi')):
                        rooms = int(info.string.replace('Liczba pokoi:', '').replace('pokoje', '').replace(' ', '').replace('iwięcej', '').replace('pokój', ''))
            dictionary = {
                'name': name,
                'price': price,
                'meters': meters,
                'rooms': rooms,
                'storey': storey,
                'year': year,
                'market': market,
                'link': link
            }
            
            all_offers_list.append(dictionary)
        print(f'PAGE {i}/{amount_pages} ENDED')
    return all_offers_list


def count_medium_price(all_offers_list, min_meters, max_meters):
    offers_ammount = 0
    price_sum = 0
    meters_sum = 0
    match_offerts_list = []
    for offer in all_offers_list:
        if(offer['meters']>=min_meters and offer['meters']<=max_meters):
            price_sum = price_sum + offer['price']
            meters_sum = meters_sum + offer['meters']
            offers_ammount += 1
            match_offerts_list.append(offer)
    if (len(match_offerts_list)>0):
        average_price = round(price_sum/offers_ammount, 2)
        average_meter_price = round(price_sum/meters_sum, 2)
        return average_meter_price
              